"""
convert_file

"""
from AMVN_alpha.utils import option
from AMVN_alpha.utils.convert import convert_File
from AMVN_alpha.model.predict import predict_test

opt = option.Options()

# convert_test

abs_path = 'C:/dev/workspace/AutoGenerating_VariableName/'
input_path = abs_path + 'pjt_practice/ipynb/input/input.xlsx'
output_path = abs_path + 'pjt_practice/ipynb/output/output_spacing.xlsx'

convert_File(input_path, output_path, useType='spacing')

# predict_test()