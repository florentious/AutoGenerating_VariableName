
"""
convert
 - convert to variableName(korean to english)

"""


import pandas as pd
from collections import defaultdict
from konlpy.tag import Okt
from AMVN_alpha.utils.option import Options
from AMVN_alpha.model.predict import predict

opt = Options()


def getDefDict(path = opt.base_dictionary_path) :
    # convert dataframe_to_dictionary
    # key = 용어명, value = [용어영문명, 영문약어명, 정의]

    tmp = pd.read_excel(path, header=1, index_col=0)

    newDict = defaultdict(list)
    for idx in tmp.index :
        newDict[tmp.at[idx ,'용어명']] = [tmp.at[idx ,'용어영문명'] ,tmp.at[idx ,'영문약어명'] ,tmp.at[idx ,'정의'] ]

    return newDict


# use konlpy package
def getNouns(input_):
    tl = Okt().pos(input_)
    rl = []
    tmp = ''
    for idx in range(len(tl)):
        if tl[idx][1] == 'Noun':
            if tmp != '':
                rl.append(tmp)
            rl.append(tl[idx][0])
            tmp = ''
        else:
            tmp += str(tl[idx][0])
    if tmp != '':
        rl.append(tmp)

    return rl

# select_spacing_model : konlpy, spacing(DL model)
def select_spacing(type_, input_) :
    if type_.lower() == 'konlpy' :
        return getNouns(input_)
    elif type_.lower() == 'spacing' :
        return predict(input_)
    else :
        raise print('we have only knolpy, spacing models')
