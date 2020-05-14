"""
predict - modeling


"""



from functools import lru_cache
import re
import mxnet as mx
import numpy as np

from AMVN_alpha.model.embed import encoding_and_padding
from AMVN_alpha.utils.option import Options
from AMVN_alpha.utils.util import load_embedding,getCtx,getModelWeights, load_vocab, delEscapeChar
from AMVN_alpha.model.model import auto_spacing

opt = Options()

vocab_path = opt.vocab_path
weights = load_embedding(opt.w2idx_embed)

vocab_size = weights.shape[0]
embed_dim = weights.shape[1]

max_seq_len = opt.max_seq_len
n_hidden = opt.n_hidden
batch_size = opt.batch_size
ctx = getCtx(opt.gpu_count)

w2idx, idx2w = load_vocab(vocab_path)


class pred_spacing:
    def __init__(self, model, w2idx):
        self.model = model
        self.w2idx = w2idx
        self.pattern = re.compile(r'\s+')

    @lru_cache(maxsize=None)
    def get_spaced_sent(self, raw_sent):
        raw_sent_ = "«" + raw_sent + "»"
        raw_sent_ = raw_sent_.replace(' ', '^')
        sents_in = [
            raw_sent_,
        ]
        mat_in = encoding_and_padding(word2idx_dic=self.w2idx, sequences=sents_in, maxlen=opt.max_seq_len,
                                      padding='post', truncating='post')
        mat_in = mx.nd.array(mat_in, ctx=mx.cpu(0))
        results = self.model(mat_in)
        mat_set = results[0,]
        preds = np.array(
            ['1' if i > 0.5 else '0' for i in mat_set[:len(raw_sent_)]])

        return self.make_pred_sents(raw_sent_, preds)

    def make_pred_sents(self, x_sents, y_pred):
        res_sent = []
        for i, j in zip(x_sents, y_pred):
            if j == '1':
                res_sent.append(i)
                res_sent.append(' ')
            else:
                res_sent.append(i)
        subs = re.sub(self.pattern, ' ', ''.join(res_sent).replace('^', ' '))
        subs = subs.replace('«', '')
        subs = subs.replace('»', '')
        return subs


def predict(text) :
    model = auto_spacing(n_hidden, vocab_size, embed_dim, max_seq_len)
    model.load_parameters(getModelWeights(path=opt.weight_path), ctx=ctx)
    predictor = pred_spacing(model, w2idx)

    tmp = predictor.get_spaced_sent(text).split(' ')

    return list(filter(lambda x : x != '', tmp))

def predict_test() :
    vocab_path = opt.vocab_path
    weights = load_embedding(opt.w2idx_embed)
    model_params = getModelWeights(opt.weight_path)

    vocab_size = weights.shape[0]
    embed_dim = weights.shape[1]

    max_seq_len = opt.max_seq_len
    n_hidden = opt.n_hidden
    ctx = getCtx(opt.gpu_count)

    w2idx, idx2w = load_vocab(vocab_path)

    model = auto_spacing(n_hidden, vocab_size, embed_dim, max_seq_len)
    model.load_parameters(model_params, ctx=ctx)
    predictor = pred_spacing(model, w2idx)

    while True:
        sent = input("sent (quit = 'q') > ")
        # print(sent)
        if sent.lower() == 'q' :
            break
        else :
            spaced = predictor.get_spaced_sent(sent)
            print(spaced)
