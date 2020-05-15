"""

embedding
 - make word_to_dictionary, embedding model



"""


import numpy as np
import os
import pandas as pd
from utils.option import Options

from utils.util import mkdirs_, string2spacingChar




class MySentenceGenerator(object):

    def __init__(self, fname):
        self.fname = fname

    def __iter__(self):

        base_path =  Options().base_dictionary_path

        df_origin = pd.read_csv(base_path + 'dataset/spacing.csv').origin
        for idx in range(len(df_origin)):
            yield string2spacingChar(df_origin[idx].strip()).split(' ')

def create_embedding(data_dir, model_file, embeddings_file, vocab_file, splitc=' ' ,**params) :
    import json
    from gensim.models import Word2Vec

    class SentenceGenerator(object) :
        def __init__(self, dirname) :
            self.dirname = dirname
        def __iter__(self) :
            for fname in os.listdir(self.dirname) :
                print("Processing~ '{}'".format(fname))
                with open(self.dirname +fname ,'r' ,encoding='utf8') as f :
                    for line in f.readlines() :
                        yield string2spacingChar(line.strip()).split(splitc)

    mkdirs_(data_dir)
    sentences = SentenceGenerator(data_dir)

    model = Word2Vec(sentences ,**params)

    model.save(model_file)

    weights = model.wv.syn0
    default_vec = np.mean(weights, axis=0, keepdims = True)
    padding_vec = np.zeros((1 ,weights.shape[1]))

    weights_default = np.concatenate([weights, default_vec, padding_vec], axis=0)

    np.save(open(embeddings_file, 'wb'), weights_default)

    vocab = dict([(k,v.index) for k ,v in model.wv.vocab.items()])
    vocab['__ETC__'] = weights_default.shape[0] -2
    vocab['__PAD__'] = weights_default.shape[0] - 1

    with open(vocab_file, 'w') as f:
        f.write(json.dumps(vocab))

def pad_sequences(sequences,maxlen=None,dtype='int32',padding='pre',truncating='pre',value=0.):

    if not hasattr(sequences, '__len__'):
        raise ValueError('`sequences` must be iterable.')
    lengths = []
    for x in sequences:
        if not hasattr(x, '__len__'):
            raise ValueError('`sequences` must be a list of iterables. '
                             'Found non-iterable: ' + str(x))
        lengths.append(len(x))

    num_samples = len(sequences)
    if maxlen is None:
        maxlen = np.max(lengths)

    # take the sample shape from the first non empty sequence
    # checking for consistency in the main loop below.
    sample_shape = tuple()
    for s in sequences:
        if len(s) > 0:
            sample_shape = np.asarray(s).shape[1:]
            break

    x = (np.ones((num_samples, maxlen) + sample_shape) * value).astype(dtype)
    for idx, s in enumerate(sequences):
        if not len(s):
            continue  # empty list/array was found
        if truncating == 'pre':
            trunc = s[-maxlen:]
        elif truncating == 'post':
            trunc = s[:maxlen]
        else:
            raise ValueError('Truncating type "%s" not understood' %truncating)

        # check `trunc` has expected shape
        trunc = np.asarray(trunc, dtype=dtype)
        if trunc.shape[1:] != sample_shape:
            raise ValueError(
                'Shape of sample %s of sequence at position %s is different from expected shape %s'
                % (trunc.shape[1:], idx, sample_shape))

        if padding == 'post':
            x[idx, :len(trunc)] = trunc
        elif padding == 'pre':
            x[idx, -len(trunc):] = trunc
        else:
            raise ValueError('Padding type "%s" not understood' % padding)
    return x


def encoding_and_padding(word2idx_dic, sequences,**params) :
    seq_idx = [[word2idx_dic.get(a,word2idx_dic['__ETC__']) for a in i] for i in sequences]
    params['value'] = word2idx_dic['__PAD__']
    return pad_sequences(seq_idx, **params)


def get_transDtype(x, y, batch_size):
    from mxnet import gluon
    tr_set = gluon.data.ArrayDataset(x, y.astype('float32'))
    tr_data_iterator = gluon.data.DataLoader(tr_set, batch_size=batch_size)
    return tr_data_iterator


def y_encoding(n_grams, maxlen=50):
    init_mat = np.zeros(shape=(len(n_grams), maxlen), dtype=np.int8)
    for i in range(len(n_grams)):
        init_mat[i, np.cumsum([len(j) for j in n_grams[i]]) - 1] = 1
    return init_mat

