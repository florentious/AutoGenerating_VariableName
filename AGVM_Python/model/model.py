
"""
modeling
 - need to input_shape(in_channels)

 - model_shape
    embedding -> conv2d * 5 -> concat -> bidirectional GRU
    -> dense('relu') -> dense('softmax')


"""


import mxnet as mx
from mxnet import gluon
from mxnet.gluon import nn, rnn
from utils.option import Options
from utils.util import getCtx, getModelWeights, load_embedding

opt = Options()


class auto_spacing(gluon.HybridBlock) :
    def __init__(self, n_hidden, vocab_size, embed_dim, max_seq_length ,**kwargs) :
        super(auto_spacing, self).__init__(**kwargs)

        self.in_seq_len = max_seq_length
        self.out_seq_len = max_seq_length
        self.n_hidden = n_hidden
        self.vocab_size = vocab_size
        self.max_seq_length = max_seq_length
        self.embed_dim = embed_dim

        with self.name_scope() :
            self.embedding = nn.Embedding(input_dim=self.vocab_size ,output_dim=self.embed_dim)

            self.conv_unigram = nn.Conv2D(channels=128 ,in_channels=1, kernel_size=(1, self.embed_dim))
            self.conv_bigram = nn.Conv2D(channels=256, in_channels=1, kernel_size=(2, self.embed_dim), padding=(1, 0))
            self.conv_trigram = nn.Conv2D(channels=128, in_channels=1, kernel_size=(3, self.embed_dim), padding=(1, 0))
            self.conv_forthgram = nn.Conv2D(channels=64, in_channels=1,  kernel_size=(4, self.embed_dim), padding=(2, 0))
            self.conv_fifthgram = nn.Conv2D(channels=32 ,in_channels=1,  kernel_size=(5, self.embed_dim), padding=(2, 0))

            self.bi_gru = rnn.GRU(hidden_size=self.n_hidden ,input_size=608, layout='NTC', bidirectional=True)
            self.dense_sh = nn.Dense(100, in_units=608, activation='relu', flatten=False)
            self.dense = nn.Dense(1 ,in_units=100, activation='sigmoid', flatten=False)

    def hybrid_forward(self, F, inputs) :
        embed = self.embedding(inputs)
        embed = F.expand_dims(embed, axis=1)

        unigram = self.conv_unigram(embed)
        bigram = self.conv_bigram(embed)
        trigram = self.conv_trigram(embed)
        forthgram = self.conv_forthgram(embed)
        fifthgram = self.conv_fifthgram(embed)

        grams = F.concat(unigram, F.slice_axis(bigram, axis=2, begin=0 ,end=self.max_seq_length),
                         trigram, F.slice_axis(forthgram, axis=2, begin=0 ,end=self.max_seq_length),
                         F.slice_axis(fifthgram, axis=2, begin=0 ,end=self.max_seq_length), dim=1)

        grams = F.transpose(grams, (0 ,2 ,3 ,1))
        grams = F.reshape(grams, (-1 ,self.max_seq_length ,-3))
        grmas = self.bi_gru(grams)
        fc1 = self.dense_sh(grams)
        return (self.dense(fc1))


def model_init(n_hidden ,vocab_size, embed_dim, max_seq_length, ctx, embed_weights) :
    model = auto_spacing(n_hidden, vocab_size, embed_dim, max_seq_length)

    model.collect_params().initialize(mx.init.Xavier(), ctx=ctx)
    model.embedding.weight.set_data(embed_weights)
    model.hybridize(static_alloc=True)

    model.embedding.collect_params().setattr('grad_req', 'null')
    trainer = gluon.Trainer(model.collect_params(), 'rmsprop')
    loss = gluon.loss.SigmoidBinaryCrossEntropyLoss(from_sigmoid=True)
    loss.hybridize(static_alloc=True)
    return (model, loss, trainer)

def model_load() :
    weights = load_embedding(opt.w2idx_embed)

    model = auto_spacing(opt.n_hidden, weights.shape[0], weights.shape[1], opt.max_seq_len)
    model.load_parameters(getModelWeights(path=opt.weight_path), ctx=getCtx(opt.gpu_count))
    print('model loaded..')

    return model