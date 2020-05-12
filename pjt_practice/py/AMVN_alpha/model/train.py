
"""
 train and getData functions


"""

import mxnet as mx
import numpy as np
import logging
import time
import os
from tqdm import tqdm
from mxnet import gluon
import mxnet.autograd as autograd

from AMVN_alpha.utils import option
from AMVN_alpha.utils.util import replaceEx,pre_processing,load_vocab,mkdirs_
from AMVN_alpha.model.embed import y_encoding,encoding_and_padding,get_transDtype


opt = option.Options()
logger = logging.getLogger()

def input_data(input_path, train_ratio=1, isMake_dif_set=False, max_seq_len=opt.max_seq_len,
               vocab_path=opt.vocab_path , batch_size=opt.max_seq_len):


    # get_rawData
    dir_list = [txt for txt in os.listdir(input_path) if txt.endswith(".txt")]

    X_origin = []
    for txt in dir_list:
        with open(input_path + txt, 'r', encoding='utf8') as f:
            X_origin.extend(f.readlines())

    # del '::','{', etc..
    X_origin = replaceEx(X_origin)
    # add <SoS>, <EoS>, replace(' ','^')
    processed_seq_ = pre_processing(X_origin)
    # del blank_list
    processed_seq_ = list(filter(lambda x: x != "«»", processed_seq_))
    # shuffle sequence list
    samp_idx = np.random.choice(range(len(processed_seq_)), int(len(processed_seq_) * train_ratio), replace=False)

    processed_seq = [processed_seq_[i] for i in samp_idx]
    sp_sents = [i.split('^') for i in processed_seq]

    # 8어절로 나눠서 테스트
    if isMake_dif_set is True:
        n_gram = [[k, v, z, a, c, d, e, f] for sent in sp_sents for k, v, z, a, c, d, e, f in
                  zip(sent, sent[1:], sent[2:],
                      sent[3:], sent[4:], sent[5:], sent[6:], sent[7:])]
    else:
        n_gram = sp_sents

    # make_target(space = 1, others = 0)
    n_gram_y = y_encoding(n_gram, max_seq_len)

    w2idx, idx2w = load_vocab(vocab_path)

    # input seq - del blank
    ngram_encoded_padded = encoding_and_padding(word2idx_dic=w2idx,
                                                sequences=[''.join(gram) for gram in n_gram], maxlen=max_seq_len,
                                                padding='post', truncating='post')

    if train_ratio < 1:
        # make train_set
        tr_idx, te_idx = split_train_set(ngram_encoded_padded, train_ratio)

        y_train = n_gram_y[tr_idx,]
        x_train = ngram_encoded_padded[tr_idx,]

        y_test = n_gram_y[te_idx,]
        x_test = ngram_encoded_padded[te_idx,]

        # train generator
        train_generator = get_transDtype(x_train, y_train, batch_size)
        valid_generator = get_transDtype(x_test, y_test, 500)
        return (train_generator, valid_generator)
    else:
        return get_transDtype(ngram_encoded_padded, n_gram_y, batch_size)


def split_train_set(x_train, p=0.98):

    train_idx = np.random.choice(range(x_train.shape[0]), int(x_train.shape[0] * p), replace=False)
    set_tr_idx = set(train_idx)
    test_index = [i for i in range(x_train.shape[0]) if i not in set_tr_idx]
    return ((train_idx, np.array(test_index)))

def evaluate_accuracy(data_iterator, net, pad_idx, ctx, n=5000):
    # 각 시퀀스의 길이만큼 순회하며 정확도 측정
    # 최적화되지 않음
    acc = mx.metric.Accuracy(axis=0)
    num_of_test = 0
    for i, (data, label) in enumerate(data_iterator):
        data = data.as_in_context(ctx)
        label = label.as_in_context(ctx)
        # get sentence length
        data_np = data.asnumpy()
        lengths = np.argmax(np.where(data_np == pad_idx, np.ones_like(data_np),
                                     np.zeros_like(data_np)),
                            axis=1)
        output = net(data)
        pred_label = output.squeeze(axis=2) > 0.5

        for i in range(data.shape[0]):
            num_of_test += data.shape[0]
            acc.update(preds=pred_label[i, :lengths[i]],
                       labels=label[i, :lengths[i]])
        if num_of_test > n:
            break
    return acc.get()[1]


def train(epochs, train_data, test_data, vali_data, model, loss, trainer, pad_idx, ctx, weight_path=opt.weight_path, decay=False,
          mdl_desc='spacing_model'):

    mkdirs_(weight_path)

    tot_test_acc = []
    tot_train_loss = []

    for e in range(epochs):
        tic = time.time()

        if e > 1 and decay:
            trainer.set_learning_rate(trainer.learning_rate * 0.7)

        train_loss = []

        iter_tqdm = tqdm(train_data, 'Batches')

        for i, (x_data, y_data) in enumerate(iter_tqdm):
            x_data_l = gluon.utils.split_and_load(x_data, ctx, even_split=False)
            y_data_l = gluon.utils.split_and_load(y_data, ctx, even_split=False)

            with autograd.record():
                losses = [loss(model(x), y) for x, y in zip(x_data_l, y_data_l)]

            for l in losses:
                l.backward()

            trainer.step(x_data.shape[0], ignore_stale_grad=True)
            curr_loss = np.mean([mx.nd.mean(l).asscalar() for l in losses])
            train_loss.append(curr_loss)
            iter_tqdm.set_description("loss {}".format(curr_loss))
            mx.nd.waitall()

        # caculate test loss
        test_acc = evaluate_accuracy(test_data, model, pad_idx,
                                     ctx=ctx[0] if isinstance(ctx, list) else mx.gpu(0))
        valid_acc = evaluate_accuracy(vali_data, model, pad_idx,
                                      ctx=ctx[0] if isinstance(ctx, list) else mx.gpu(0))
        logger.info('[Epoch %d] time cost: %f' % (e, time.time() - tic))
        logger.info("[Epoch %d] Train Loss: %f, Test acc : %f Valid acc : %f" %
                    (e, np.mean(train_loss), test_acc, valid_acc))
        tot_test_acc.append(test_acc)
        tot_train_loss.append(np.mean(train_loss))
        model.save_parameters(weight_path + '/' + "{}_sec_{}.params".format(mdl_desc, e + 1))
    return (tot_test_acc, tot_train_loss)