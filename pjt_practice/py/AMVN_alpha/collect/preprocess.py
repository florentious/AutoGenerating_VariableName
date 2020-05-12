

import os
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

from AMVN_alpha.utils.option import Options
from AMVN_alpha.utils.util import mkdirs_

opt = Options()


def removeAll(origin, fileName):
    origin = list(filter(lambda a: a[:len(fileName.split('.')[0])] == fileName.split('.')[0], origin))
    origin = list(filter(lambda a: a.split('\t')[1][0] != '<', origin))
    return origin

def preprocess_txt2df(dir_path=opt.pos_raw_path,out_path=opt.pos_data_path,all_path='dat/pos_df.csv') :
    mkdirs_(out_path)

    res_df = pd.DataFrame([])
    dir_list = [txt for txt in os.listdir(dir_path) if txt.endswith(".txt")]

    for txt_ in dir_list:

        with open(dir_path + txt_, 'r', encoding='utf-16') as f:

            txt_lines = f.readlines()

            tmp_df = pd.DataFrame([])

            tmp_idx = np.array([])
            tmp_ori = np.array([])
            tmp_res = np.array([])

            data = removeAll(txt_lines, txt_)

            for idx in range(len(data)):
                # del '\n'
                tmp_data = data[idx][:-1].split('\t')

                tmp_idx = np.append(tmp_idx, tmp_data[0])
                tmp_ori = np.append(tmp_ori, tmp_data[1])
                tmp_res = np.append(tmp_res, tmp_data[2])

            tmp_df['idx'] = tmp_idx
            tmp_df['origin'] = tmp_ori
            tmp_df['result'] = tmp_res

            res_df = res_df.append(tmp_df, ignore_index=True)
            tmp_df.to_csv(out_path + txt_.split('.')[0] + '_conv.csv')

    res_df = res_df.reset_index()

    res_df.to_csv(all_path)


def convert_raw(input_,output_) :
    dir_list = [txt for txt in os.listdir(input_) if txt.endswith(".txt")]
    mkdirs_(output_)

    for txt in dir_list:
        conv_txt = ""

        with open(input_ + txt, 'r', encoding='utf16') as fr:
            tmp = BeautifulSoup(fr.read(), 'html.parser')

            for idx in range(len(tmp.findAll('s'))):
                conv_txt += tmp.findAll('s')[idx].text + '\n'

        with open(output_ + txt, 'w', encoding='utf8') as fw:
            fw.write(conv_txt)