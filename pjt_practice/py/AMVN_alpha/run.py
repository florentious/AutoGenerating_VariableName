"""
select : predict or fit(train)

"""
from AMVN_alpha.utils import option
from AMVN_alpha.utils.util import load_embedding,getCtx,getModelWeights, load_vocab
from AMVN_alpha.model.model import auto_spacing
from AMVN_alpha.model.predict import pred_spacing

opt = option.Options()

vocab_path = opt.vocab_path
weights = load_embedding(opt.w2idx_embed)

vocab_size = weights.shape[0]
embed_dim = weights.shape[1]

max_seq_len = opt.max_seq_len
n_hidden = opt.n_hidden
batch_size = opt.batch_size
ctx = getCtx(opt.gpu_count)

w2idx, idx2w = load_vocab(vocab_path)


def predict(text) :
    model = auto_spacing(n_hidden, vocab_size, embed_dim, max_seq_len)
    model.load_parameters(getModelWeights(path=opt.weight_path), ctx=ctx)
    predictor = pred_spacing(model, w2idx)

    return predictor.get_spaced_sent(text)
