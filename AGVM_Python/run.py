"""
convert_file

"""
from utils import option
from utils.convert import convert_File
from model.predict import predict_test
from utils.util import changeDirSperacte

opt = option.Options()
input_path = opt.py2java_path + '../AGVN_Web/data/convert/data\\upload\\Input.xlsx'
output_path = opt.py2java_path + '../AGVN_Web/data/convert/data\\upload\\Input.xlsx'
# convert_test
#
# abs_path = 'C:/dev/workspace/AutoGenerating_VariableName/'
# input_path = abs_path + 'pjt_practice/ipynb/input/input.xlsx'
# output_path = abs_path + 'pjt_practice/ipynb/output/output_spacing.xlsx'
#
# convert_File(input_path, output_path, useType='spacing')

# predict_test()

print(changeDirSperacte("../AGVN_Web/data/convert/data\\upload\\Input.xlsx"))