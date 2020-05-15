
"""
convert
 - convert to variableName(korean to english)

"""


import pandas as pd
import numpy as np
import re

from collections import defaultdict
from konlpy.tag import Okt
from utils.option import Options
from model.predict import predict
from utils.util import sumStrList, getSpacedKor, mkdirs_, delEscapeChar
from utils.translate_define import translate,define_word

opt = Options()


def getDefDict(path = opt.base_dictionary_path) :
    # convert dataframe_to_dictionary
    # key = 용어명, value = [용어영문명, 영문약어명, 정의]

    tmp = pd.read_excel(path, header=1, index_col=0)

    newDict = defaultdict(list)
    for idx in tmp.index :
        newDict[tmp.at[idx ,'용어명']] = [tmp.at[idx ,'용어영문명'] ,tmp.at[idx ,'영문약어명'] ,tmp.at[idx ,'정의'] ]

    return newDict

# already use dictionary
def getWordDict(path):

    tmp = pd.read_excel(path, sheet_name='단어')

    tmpDict = defaultdict(list)
    for idx in tmp.index:
        tmpDict[tmp.at[idx, '단어명']] = [tmp.at[idx, '영문명'], tmp.at[idx, '약어명'], tmp.at[idx, '정의']]

    return tmpDict

# origin<-addition // duplicate => use origin
def merge_defaultdicts(origin,addition):
    for k,v in addition.items():
        if not k in origin:
            origin[k] = addition[k]
    return origin


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
def select_spacing(input_,type_='konlpy') :
    if type_.lower() == 'konlpy' :
        return getNouns(input_)
    elif type_.lower() == 'spacing' :
        return predict(input_)
    else :
        raise print('we have only knolpy, spacing models')


# make abbreviation, return txt(upper)
def abbreviate(eng):
    # except first_charactor
    tmp = eng.lower()[1:]

    # del escape_char
    tmp = delEscapeChar(tmp)

    if len(tmp) > 2:
        # del vowel
        regex = re.compile('[^aeiou]')
        tmp_sec = ''.join(regex.findall(tmp))

        # del dupplicate_char
        for ch in tmp_sec:
            dup = ch + ch
            tmp_sec = re.sub(dup, ch, tmp_sec)

        # if del too much, backUp to origin
        if len(tmp_sec) > 2 :
            tmp = tmp_sec


    # del blank
    return (eng[0]+re.sub(' ', '', tmp)).upper()

# is word in dictionary_ return : boolean
def isInDict(word, dict_):
    isIn = False
    for l in dict_.values():
        if word.upper() == l[1]:
            isIn = True
            break

    return isIn


def convert_abbr(eng, kor, dict_):
    # abbreviate, isInDict

    tmp_abr = abbreviate(eng)

    for idx in range(3, len(tmp_abr) + 1):
        if not isInDict(tmp_abr[:idx], dict_):
            dict_[kor] = [eng, tmp_abr[:idx].upper(), define_word(kor)]
            return tmp_abr[:idx].upper(), dict_


    idx = 3
    tmp = delEscapeChar(eng).upper()
    while True:
        if idx != len(eng):
            for idx in range(3, len(eng) + 1):
                if not isInDict(eng[:idx], dict_):
                    dict_[kor] = [eng, eng[:idx].upper(), define_word(kor)]
                    return eng[:idx].upper(), dict_
        else:
            tmp += '_'
            if not isInDict(tmp, dict_):
                dict_[kor] = [eng, tmp.upper(), define_word(kor)]
                return tmp, dict_


def convert_kor2abr(input_, dict_):
    tmp_spacedAbr = ''
    tmp_spacedEng = ''

    if input_ != []:
        for idx in range(len(input_), 0, -1):
            tmpTxt = sumStrList(input_[:idx])
            if tmpTxt in dict_.keys():
                tmp_spacedEng += dict_[tmpTxt][0] + '_'
                tmp_spacedAbr += dict_[tmpTxt][1] + '_'
                if idx != len(input_):
                    sub_abr, sub_eng, dict_ = convert_kor2abr(input_[idx:], dict_)
                    tmp_spacedAbr += sub_abr
                    tmp_spacedEng += sub_eng
                break

            if idx == 1:
                tmp_eng = translate(tmpTxt)
                # 약어변경 함수(convert_abbr)
                tmp_abr, dict_ = convert_abbr(tmp_eng, tmpTxt, dict_)
                tmp_spacedAbr += tmp_abr + '_'
                tmp_spacedEng += tmp_eng.upper() + '_'

                if idx != len(input_):
                    sub_abr, sub_eng, dict_ = convert_kor2abr(input_[idx:], dict_)
                    tmp_spacedAbr += sub_abr
                    tmp_spacedEng += sub_eng

        if tmp_spacedAbr[-1] == '_':
            tmp_spacedAbr = tmp_spacedAbr[:-1]
            tmp_spacedEng = tmp_spacedEng[:-1]

    return tmp_spacedAbr, tmp_spacedEng, dict_


def dict2sheet(path, input_, dict_):
    # dict_col 단어명,영문명,약어명,정의

    tmp = pd.DataFrame([])
    wrd = np.array([])
    eng = np.array([])
    abr = np.array([])
    def_ = np.array([])

    for k in dict_.keys():
        wrd = np.append(wrd, k)
        eng = np.append(eng, dict_[k][0])
        abr = np.append(abr, dict_[k][1])
        def_ = np.append(def_, dict_[k][2])

    tmp['단어명'] = wrd
    tmp['영문명'] = eng
    tmp['약어명'] = abr
    tmp['정의'] = def_

    with pd.ExcelWriter(path, engine='xlsxwriter') as ew:
        tmp.to_excel(ew, sheet_name='단어', index=False)
        input_.to_excel(ew, sheet_name='용어', index=False)



def convert_File(input_path, output_path, isUseDict=True, useType='konlpy'):

    input_ = pd.read_excel(input_path, sheet_name='용어')
    if output_path[input_path.rfind('/'):].find('.') == -1:
        output_path += input_path[input_path.rfind('/'):]
    # np.NaN is float type
    input_ = input_.fillna("")

    # memory on dictionary
    dict_ = getWordDict(input_path)

    if isUseDict:
        defDict = getDefDict(opt.base_dictionary_path)
        dict_ = merge_defaultdicts(dict_, defDict)

    for idx in input_['약어명'].isnull().index:
        spaced_kor = select_spacing(input_.at[idx, '용어명'],useType)
        abr, eng, dict_ = convert_kor2abr(spaced_kor, dict_)
        input_.at[idx, '약어명'] = abr
        input_.at[idx, '한글단어별'] = getSpacedKor(spaced_kor)
        input_.at[idx, '영문단어별'] = eng

    # input, dict_to_sheet
    dict2sheet(output_path, input_, dict_)