
"""
Dictionary_const :
  - key : 용어명(str)
  - value : list(str) -> [용어영문명(str), 영문약어명(str), 정의(str)]

In/Output_format_columns :
 ㅇ 용어_sheet
  - 용어명
  - 단어단위명
  - 용어영문명
  - 영문약어명
  - 정의
 ㅇ 단어_sheet
  - 단어
  - 단어영문명
  - 단어영문약어명

"""


import json
import os
import numpy as np
import mxnet as mx
from AMVN_alpha.utils import option

opt = option.Options()

def getCtx(gpu_count) :
    if gpu_count == 0 :
        return mx.cpu(0)
    else :
        return(mx.gpu(i) for i in range(gpu_count))

# directory_path end check (if use '/')
def dirEnd_check(path) :
    if path[-1] != '/' :
        path += '/'
    return path

# getModelWeights
def getModelWeights(path) :
    weights_list = os.listdir(path)
    # get_recently_weights
    return path+weights_list[-1]

# make_directorys
def mkdirs_(output_path) :
    try :
        if not os.path.exists(output_path) :
            os.mkdir(output_path)
    except :
        print('Error : '+ output_path)

def load_vocab(path):
    with open(path, 'r') as f:
        data = json.loads(f.read())
        word2idx = data
        idx2word = dict([(v, k) for (k, v) in data.items()])

    return word2idx, idx2word

def string2spacingChar(input_):
    # 빈칸을 '^'로 변환하기
    chars = input_.strip().replace(' ', '^')

    # SOS : «, EOS : »
    tagged_chars = "«" + chars + "»"

    char_list = ' '.join(list(tagged_chars))

    return char_list

def pre_processing(input_):
    ch_list = []

    for cl in input_:
        ch_list.append(string2spacingChar(cl).replace(' ', ''))

    return ch_list


def load_embedding(embeddings_file):
    return (np.load(embeddings_file))


def replaceEx(input_):
    # 이상한 글자제거
    res = []
    for str_ in input_:
        res.append(str_.replace('::', '').replace('{', '').replace('-', ''))
    return res