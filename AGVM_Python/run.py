"""
convert_file

"""
from utils import option
from utils.convert import convert_File, getWordDict, select_spacing, convert_kor2abr
from model.predict import predict_test
from model.model import model_load
from utils.util import changeDirSperacte

model = model_load()
opt = option.Options()
input_path = opt.py2java_path + 'data\\upload\\테스트용한개.xlsx'
output_path = opt.py2java_path + 'data/convert'
# convert_test
#
# abs_path = 'C:/dev/workspace/AutoGenerating_VariableName/'
# input_path = abs_path + 'pjt_practice/ipynb/input/input.xlsx'
# output_path = abs_path + 'pjt_practice/ipynb/output/output_spacing.xlsx'
#
# isSuccess, output_path = convert_File(input_path, output_path, model, isUseDict=False, useType='self_product')

# predict_test()
