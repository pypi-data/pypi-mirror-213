import inspect
import os
import sys

import pandas as pd
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import milliman_sensi.io as sio
import milliman_sensi.syntax as syn

TEST_DIR = os.path.dirname(inspect.getfile(inspect.currentframe())).replace("\\", "/")


def test_extract_value_from_equal_without_equal():
    param_string = "file::eco[GBP].driver[IR].data.swaptions.mkt[*,1] (+100)"

    with pytest.raises(syn.SensiSyntaxError):
        syn.extract_value_from_equal(param_string)


def test_extract_value_from_equal_with_equal():
    param_string = "file::eco[GBP].driver[IR].data.swaptions.mkt[*,1]=(+100)"

    assert(syn.extract_value_from_equal(param_string) == ("file::eco[GBP].driver[IR].data.swaptions.mkt[*,1]", "(+100)"))


def test_extract_target_column_incorrect():
    param_string = "file::eco[GBP].driver[IR].data.swaptions.mkt[3,3"

    with pytest.raises(syn.SensiSyntaxError):
        syn.extract_target_column(param_string)


def test_extract_target_column_correct():
    param_string = "file::eco[GBP].driver[IR].data.swaptions.mkt[3,3]"

    assert(syn.extract_target_column(param_string) == ("file::eco[GBP].driver[IR].data.swaptions.mkt", "3,3"))


def test_parse_param_without_file():
    param_string = "eco[GBP].driver[IR].data.swaptions.mkt['COL3']=500"
    syntax = syn.parse_param(param_string)
    assert(syntax.expression == "eco[GBP].driver[IR].data.swaptions.mkt['COL3']")
    assert(syntax.col == "")
    assert(syntax.condition == "")
    assert(syntax.value == "500")


def test_parse_param_without_where():
    param_string = '''"file::eco[GBP].driver[IR].data.swaptions.mkt['ROW3','COL3']"=100'''
    syntax = syn.parse_param(param_string)
    assert(syntax.expression == "$..*[@.name is 'GBP']..*[@.name is 'IR'].data.swaptions.mkt.filename")
    assert(syntax.col == "'ROW3','COL3'")
    assert(syntax.condition == "")
    assert(syntax.value == "100")


def test_parse_param_without_a_condition():
    param_string = '''"file::eco[GBP].driver[IR].data.swaptions.mkt['COL3'].where()"=(+100)'''
    syntax = syn.parse_param(param_string)
    assert(syntax.expression == "$..*[@.name is 'GBP']..*[@.name is 'IR'].data.swaptions.mkt.filename")
    assert(syntax.col == "'COL3'")
    assert(syntax.condition == "()")
    assert(syntax.value == "(+100)")


def test_parse_param_without_col():

    param_string = '''"file::eco[GBP].driver[IR].data.swaptions.mkt.where('COL1'==0,10,20 && 'COL2'>0 || 'COL4'<0)"=(+100)'''
    with pytest.raises(syn.SensiSyntaxError):
        syn.parse_param(param_string)


def test_parse_param_without_brackets():
    param_string = '''"file::eco_1.driver_1.data.swaptions.mkt['COL3', 1]"=(+100)'''
    syntax = syn.parse_param(param_string)
    assert(syntax.expression == "$..*['eco_1']..*['driver_1'].data.swaptions.mkt.filename")
    assert(syntax.col == "'COL3', 1")
    assert(syntax.condition == "")
    assert(syntax.value == "(+100)")


def test_parse_param_mixed():
    param_string = '''"file::eco[GBP].driver_1.data.swaptions.mkt['COL3', 1]"=(+100)'''
    syntax = syn.parse_param(param_string)
    assert(syntax.expression == "$..*[@.name is 'GBP']..*['driver_1'].data.swaptions.mkt.filename")
    assert(syntax.col == "'COL3', 1")
    assert(syntax.condition == "")
    assert(syntax.value == "(+100)")    


def test_parse_param_invert_order():
    param_string = '''"file::driver_1.eco_1.data.swaptions.mkt['COL3', 1]"=(+100)'''
    syntax = syn.parse_param(param_string)
    assert(syntax.expression == "$..*['eco_1']..*['driver_1'].data.swaptions.mkt.filename")
    assert(syntax.col == "'COL3', 1")
    assert(syntax.condition == "")
    assert(syntax.value == "(+100)")


def test_parse_param():
    param_string = '''"file::eco[GBP].driver[IR].data.swaptions.mkt['COL3'].where('COL1'==0,10,20 && 'COL2'>0 || 'COL4'<0)"=(+100)'''
    syntax = syn.parse_param(param_string)
    assert(syntax.expression == "$..*[@.name is 'GBP']..*[@.name is 'IR'].data.swaptions.mkt.filename")
    assert(syntax.col == "'COL3'")
    assert(syntax.condition == "('COL1'==0,10,20 && 'COL2'>0 || 'COL4'<0)")
    assert(syntax.value == "(+100)")


def test_query_None_data():
    data = None
    expression = ".."

    with pytest.raises(syn.SensiSyntaxError):
        syn.query(data, expression)


def test_query_wrong_expression():
    data = sio.read_json_file(f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/settings.json")
    expression = ".."
    assert(syn.query(data, expression) == [])


def test_query_zero_result():
    data = sio.read_json_file(f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/settings.json")
    expression = "$..*[@.name is 'GBP']..*[@.name is 'RI'].data.swaptions.mkt.filename"
    assert(syn.query(data, expression) == [])


def test_query_one_result():
    data = sio.read_json_file(f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/settings.json")
    expression = "$..*[@.name is 'GBP']..*[@.name is 'IR'].data.swaptions.mkt.filename"
    assert(syn.query(data, expression) == ['GBP_Mkt_Swaptions_Vols.csv'])


def test_query_more_than_one_result():
    data = sio.read_json_file(f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/settings.json")
    expression = "$..init_curve.mkt.filename"
    assert(syn.query(data, expression) == ['GBP_Mkt_Nominal_ZC_Rates_Curve.csv',
                                           'GBP_Mkt_BEIR_Curve.csv',
                                           'EUR_Mkt_Nominal_ZC_Rates_Curve.csv',
                                           'EUR_Mkt_BEIR_Curve.csv'])


def test_get_input_file_path_file_exists():
    data = sio.read_json_file(f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/settings.json")
    expression = "$..*[@.name is 'GBP']..*[@.name is 'IR'].data.swaptions.mkt.filename"
    env_dir = f'{TEST_DIR}/Central_RN_Simulation_20201218_152857'

    assert(syn.get_input_file_path(data, expression, env_dir) == f'{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/Central/RN_inputs/ceF89BNhvJRc9WHMS/Nominal_rates/GBP_Mkt_Swaptions_Vols.csv')


def test_get_input_file_path_file_inexistant():
    data = sio.read_json_file(f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/settings.json")
    expression = "$..*[@.name is 'GBP']..*[@.name is 'IR'].data.option.tkm.filename"
    env_dir = f'{TEST_DIR}/Central_RN_Simulation_20201218_152857'

    with pytest.raises(syn.SensiSyntaxError):
        syn.get_input_file_path(data, expression, env_dir)


def test_get_input_file_path_with_wrong_field():
    data = sio.read_json_file(f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/settings.json")
    expression = "$..*[@.name is 'GBP']..*[@.name is 'IR'].data.swaptions.mkt.namefile"
    env_dir = f'{TEST_DIR}/Central_RN_Simulation_20201218_152857'

    with pytest.raises(syn.SensiSyntaxError):
        syn.get_input_file_path(data, expression, env_dir)


def test_get_input_file_path_expression_with_only_brackets():
    data = sio.read_json_file(f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/settings.json")
    expression = "$..*['eco_1']..*['driver_1'].data.swaptions.mkt.filename"
    env_dir = f'{TEST_DIR}/Central_RN_Simulation_20201218_152857'

    assert(syn.get_input_file_path(data, expression, env_dir) == f'{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/Central/RN_inputs/ceF89BNhvJRc9WHMS/Nominal_rates/GBP_Mkt_Swaptions_Vols.csv')


def test_get_input_file_inverted_order_of_driver_and_eco_in_expression():
    data = sio.read_json_file(f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/settings.json")
    expression = "$..*[@.name is 'IR']..*['eco_1'].data.swaptions.mkt.filename"
    env_dir = f'{TEST_DIR}/Central_RN_Simulation_20201218_152857'

    with pytest.raises(syn.SensiSyntaxError):
        syn.get_input_file_path(data, expression, env_dir)


def test_get_input_file_driver_name_different_than_subclass():
    data = sio.read_json_file(f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/settings.json")
    expression = "$..*[@.name is 'GBP']..*[@.name is 'EQ_1'].data.options.mkt.filename"
    env_dir = f'{TEST_DIR}/Central_RN_Simulation_20201218_152857'

    assert(syn.get_input_file_path(data, expression, env_dir) == f'{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/Central/RN_inputs/ceF89BNhvJRc9WHMS/Equity/FTSE100_Mkt_Implied_Vols.csv')


def test_get_selection_from_dataframe_with_col_and_row_numbers():
    selection = "[3,3]"
    dataframe = pd.DataFrame({"Maturity": [1, 1, 2, 2, 20, 20, 25, 30, 50, 50],
                              "Tenor": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
                              "Volatility": [0.002121, 0.002833, 0.003342, 0.004941, 0.005789, 0.006, 0.006529, 0.005569, 0.003737, 0.004129],
                              "Strike": [0, 0, 0, -0.02, 0.015, -0.005, 0.01, 0.01, 0.02, -0.02],
                              "Weigth": [1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
                              "p_y": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})

    expected = pd.DataFrame({"Volatility": [0.003342]}).set_index([pd.Index([2])])
    assert(pd.concat([syn.get_selection_from_dataframe(selection, dataframe), expected]).drop_duplicates(keep=False).empty)


def test_get_selection_from_dataframe_with_col_star_and_row_number():
    selection = "[*, 1]"
    dataframe = pd.DataFrame({"Maturity": [1, 1, 2, 2, 20, 20, 25, 30, 50, 50],
                              "Tenor": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
                              "Volatility": [0.002121, 0.002833, 0.003342, 0.004941, 0.005789, 0.006, 0.006529, 0.005569, 0.003737, 0.004129],
                              "Strike": [0, 0, 0, -0.02, 0.015, -0.005, 0.01, 0.01, 0.02, -0.02],
                              "Weigth": [1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
                              "p_y": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})

    expected = pd.DataFrame({"Maturity": [1],
                             "Tenor": [1],
                             "Volatility": [0.002121],
                             "Strike": [0],
                             "Weigth": [1],
                             "p_y": [1]}).set_index([pd.Index([1])])
    assert(pd.concat([syn.get_selection_from_dataframe(selection, dataframe), expected]).drop_duplicates(keep=False).empty)


def test_get_selection_from_dataframe_with_col_number_row_star():
    selection = "[1, *]"
    dataframe = pd.DataFrame({"Maturity": [1, 1, 2, 2, 20, 20, 25, 30, 50, 50],
                              "Tenor": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
                              "Volatility": [0.002121, 0.002833, 0.003342, 0.004941, 0.005789, 0.006, 0.006529, 0.005569, 0.003737, 0.004129],
                              "Strike": [0, 0, 0, -0.02, 0.015, -0.005, 0.01, 0.01, 0.02, -0.02],
                              "Weigth": [1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
                              "p_y": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})

    expected = pd.DataFrame({"Maturity": [1, 1, 2, 2, 20, 20, 25, 30, 50, 50]}).set_index([pd.Index(range(10))])
    assert(pd.concat([syn.get_selection_from_dataframe(selection, dataframe), expected]).drop_duplicates(keep=False).empty)


def test_get_selection_from_dataframe_with_col_name_existant():
    selection = "['Weigth']"
    dataframe = pd.DataFrame({"Maturity": [1, 1, 2, 2, 20, 20, 25, 30, 50, 50],
                              "Tenor": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
                              "Volatility": [0.002121, 0.002833, 0.003342, 0.004941, 0.005789, 0.006, 0.006529, 0.005569, 0.003737, 0.004129],
                              "Strike": [0, 0, 0, -0.02, 0.015, -0.005, 0.01, 0.01, 0.02, -0.02],
                              "Weigth": [1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
                              "p_y": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})

    expected = pd.DataFrame({"Weigth": [1, 1, 0, 1, 1, 0, 0, 1, 0, 1]}).set_index([pd.Index(range(10))])
    assert(pd.concat([syn.get_selection_from_dataframe(selection, dataframe), expected]).drop_duplicates(keep=False).empty)


def test_get_selection_from_dataframe_with_col_name_inexistant():
    selection = "['Height']"
    dataframe = pd.DataFrame({"Maturity": [1, 1, 2, 2, 20, 20, 25, 30, 50, 50],
                              "Tenor": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
                              "Volatility": [0.002121, 0.002833, 0.003342, 0.004941, 0.005789, 0.006, 0.006529, 0.005569, 0.003737, 0.004129],
                              "Strike": [0, 0, 0, -0.02, 0.015, -0.005, 0.01, 0.01, 0.02, -0.02],
                              "Weigth": [1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
                              "p_y": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})

    with pytest.raises(syn.SensiSyntaxError):
        syn.get_selection_from_dataframe(selection, dataframe)


def test_get_selection_from_dataframe_with_row_name():
    selection = "['Tenor','ROW3']"
    dataframe = pd.DataFrame({"Maturity": [1, 1, 2, 2, 20, 20, 25, 30, 50, 50],
                              "Tenor": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
                              "Volatility": [0.002121, 0.002833, 0.003342, 0.004941, 0.005789, 0.006, 0.006529, 0.005569, 0.003737, 0.004129],
                              "Strike": [0, 0, 0, -0.02, 0.015, -0.005, 0.01, 0.01, 0.02, -0.02],
                              "Weigth": [1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
                              "p_y": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})

    with pytest.raises(syn.SensiSyntaxError):
        syn.get_selection_from_dataframe(selection, dataframe)


def test_get_selection_from_dataframe_with_high_col_number():
    selection = '[1000]'
    dataframe = pd.DataFrame({"Maturity": [1, 1, 2, 2, 20, 20, 25, 30, 50, 50],
                              "Tenor": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
                              "Volatility": [0.002121, 0.002833, 0.003342, 0.004941, 0.005789, 0.006, 0.006529, 0.005569, 0.003737, 0.004129],
                              "Strike": [0, 0, 0, -0.02, 0.015, -0.005, 0.01, 0.01, 0.02, -0.02],
                              "Weigth": [1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
                              "p_y": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})

    with pytest.raises(syn.SensiSyntaxError):
        syn.get_selection_from_dataframe(selection, dataframe)


def test_get_selection_from_dataframe_with_negative_col():
    selection = "[-2]"
    dataframe = pd.DataFrame({"Maturity": [1, 1, 2, 2, 20, 20, 25, 30, 50, 50],
                              "Tenor": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
                              "Volatility": [0.002121, 0.002833, 0.003342, 0.004941, 0.005789, 0.006, 0.006529, 0.005569, 0.003737, 0.004129],
                              "Strike": [0, 0, 0, -0.02, 0.015, -0.005, 0.01, 0.01, 0.02, -0.02],
                              "Weigth": [1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
                              "p_y": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})

    with pytest.raises(syn.SensiSyntaxError):
        syn.get_selection_from_dataframe(selection, dataframe)


def test_get_selection_from_dataframe_missing_row():
    selection = "['Tenor',]"
    dataframe = pd.DataFrame({"Maturity": [1, 1, 2, 2, 20, 20, 25, 30, 50, 50],
                              "Tenor": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
                              "Volatility": [0.002121, 0.002833, 0.003342, 0.004941, 0.005789, 0.006, 0.006529, 0.005569, 0.003737, 0.004129],
                              "Strike": [0, 0, 0, -0.02, 0.015, -0.005, 0.01, 0.01, 0.02, -0.02],
                              "Weigth": [1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
                              "p_y": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})

    expected = pd.DataFrame({"Tenor": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3]}).set_index([pd.Index(range(10))])
    assert(pd.concat([syn.get_selection_from_dataframe(selection, dataframe), expected]).drop_duplicates(keep=False).empty)


def test_get_selection_from_dataframe_missing_col():
    selection = "[,1]"
    dataframe = pd.DataFrame({"Maturity": [1, 1, 2, 2, 20, 20, 25, 30, 50, 50],
                              "Tenor": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
                              "Volatility": [0.002121, 0.002833, 0.003342, 0.004941, 0.005789, 0.006, 0.006529, 0.005569, 0.003737, 0.004129],
                              "Strike": [0, 0, 0, -0.02, 0.015, -0.005, 0.01, 0.01, 0.02, -0.02],
                              "Weigth": [1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
                              "p_y": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})

    expected = pd.DataFrame({"Maturity": [1],
                             "Tenor": [1],
                             "Volatility": [0.002121],
                             "Strike": [0],
                             "Weigth": [1],
                             "p_y": [1]}).set_index([pd.Index([1])])
    assert(pd.concat([syn.get_selection_from_dataframe(selection, dataframe), expected]).drop_duplicates(keep=False).empty)


def test_get_selection_from_dataframe_empty():
    selection = "[]"
    dataframe = pd.DataFrame({"Maturity": [1, 1, 2, 2, 20, 20, 25, 30, 50, 50],
                              "Tenor": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
                              "Volatility": [0.002121, 0.002833, 0.003342, 0.004941, 0.005789, 0.006, 0.006529, 0.005569, 0.003737, 0.004129],
                              "Strike": [0, 0, 0, -0.02, 0.015, -0.005, 0.01, 0.01, 0.02, -0.02],
                              "Weigth": [1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
                              "p_y": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})

    expected = dataframe
    assert(pd.concat([syn.get_selection_from_dataframe(selection, dataframe), expected]).drop_duplicates(keep=False).empty)


def test_get_selection_from_dataframe_extra_field():
    selection = "[1,2,3]"
    dataframe = pd.DataFrame({"Maturity": [1, 1, 2, 2, 20, 20, 25, 30, 50, 50],
                              "Tenor": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
                              "Volatility": [0.002121, 0.002833, 0.003342, 0.004941, 0.005789, 0.006, 0.006529, 0.005569, 0.003737, 0.004129],
                              "Strike": [0, 0, 0, -0.02, 0.015, -0.005, 0.01, 0.01, 0.02, -0.02],
                              "Weigth": [1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
                              "p_y": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})

    expected = dataframe
    assert(pd.concat([syn.get_selection_from_dataframe(selection, dataframe), expected]).drop_duplicates(keep=False).empty)


def test_select_from_dataframe_equal_single_value():
    condition = "'Maturity'==1"
    operation = "=="
    dataframe = pd.DataFrame({"Maturity": [1, 1, 2, 2, 20, 20, 25, 30, 50, 50],
                              "Tenor": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
                              "Volatility": [0.002121, 0.002833, 0.003342, 0.004941, 0.005789, 0.006, 0.006529, 0.005569, 0.003737, 0.004129],
                              "Strike": [0, 0, 0, -0.02, 0.015, -0.005, 0.01, 0.01, 0.02, -0.02],
                              "Weigth": [1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
                              "p_y": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})

    expected = pd.DataFrame({"Maturity": [1, 1],
                             "Tenor": [1, 2],
                             "Volatility": [0.002121, 0.002833],
                             "Strike": [0, 0],
                             "Weigth": [1, 1],
                             "p_y": [1, 1]})
    assert(pd.concat([syn.select_from_dataframe(condition, operation, dataframe), expected]).drop_duplicates(keep=False).empty)


def test_select_from_dataframe_equal_multi_values():
    condition = "'Maturity'==1,2"
    operation = "=="
    dataframe = pd.DataFrame({"Maturity": [1, 1, 2, 2, 20, 20, 25, 30, 50, 50],
                              "Tenor": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
                              "Volatility": [0.002121, 0.002833, 0.003342, 0.004941, 0.005789, 0.006, 0.006529, 0.005569, 0.003737, 0.004129],
                              "Strike": [0, 0, 0, -0.02, 0.015, -0.005, 0.01, 0.01, 0.02, -0.02],
                              "Weigth": [1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
                              "p_y": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})

    expected = pd.DataFrame({"Maturity": [1, 1, 2, 2],
                             "Tenor": [1, 2, 3, 4],
                             "Volatility": [0.002121, 0.002833, 0.003342, 0.004941],
                             "Strike": [0, 0, 0, -0.02],
                             "Weigth": [1, 1, 0, 1],
                             "p_y": [1, 1, 1, 1]})
    assert(pd.concat([syn.select_from_dataframe(condition, operation, dataframe), expected]).drop_duplicates(keep=False).empty)


def test_select_from_dataframe_equal_no_right_value():
    condition = "'Maturity'==,"
    operation = "=="
    dataframe = pd.DataFrame({"Maturity": [1, 1, 2, 2, 20, 20, 25, 30, 50, 50],
                              "Tenor": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
                              "Volatility": [0.002121, 0.002833, 0.003342, 0.004941, 0.005789, 0.006, 0.006529, 0.005569, 0.003737, 0.004129],
                              "Strike": [0, 0, 0, -0.02, 0.015, -0.005, 0.01, 0.01, 0.02, -0.02],
                              "Weigth": [1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
                              "p_y": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})

    expected = pd.DataFrame()
    assert(pd.concat([syn.select_from_dataframe(condition, operation, dataframe), expected]).drop_duplicates(keep=False).empty)


def test_select_from_dataframe_equal_no_left_value():
    condition = "==1"
    operation = "=="
    dataframe = pd.DataFrame({"Maturity": [1, 1, 2, 2, 20, 20, 25, 30, 50, 50],
                              "Tenor": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
                              "Volatility": [0.002121, 0.002833, 0.003342, 0.004941, 0.005789, 0.006, 0.006529, 0.005569, 0.003737, 0.004129],
                              "Strike": [0, 0, 0, -0.02, 0.015, -0.005, 0.01, 0.01, 0.02, -0.02],
                              "Weigth": [1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
                              "p_y": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})

    with pytest.raises(syn.SensiSyntaxError):
        syn.select_from_dataframe(condition, operation, dataframe)


def test_select_from_dataframe_equal_different_types():
    condition = "'Maturity'=='Example'"
    operation = "=="
    dataframe = pd.DataFrame({"Maturity": [1, 1, 2, 2, 20, 20, 25, 30, 50, 50],
                              "Tenor": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
                              "Volatility": [0.002121, 0.002833, 0.003342, 0.004941, 0.005789, 0.006, 0.006529, 0.005569, 0.003737, 0.004129],
                              "Strike": [0, 0, 0, -0.02, 0.015, -0.005, 0.01, 0.01, 0.02, -0.02],
                              "Weigth": [1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
                              "p_y": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})

    expected = pd.DataFrame()
    assert(pd.concat([syn.select_from_dataframe(condition, operation, dataframe), expected]).drop_duplicates(keep=False).empty)


def test_select_from_dataframe_wrong_operation():
    condition = "'Maturity'!!1"
    operation = "!!"
    dataframe = pd.DataFrame({"Maturity": [1, 1, 2, 2, 20, 20, 25, 30, 50, 50],
                              "Tenor": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
                              "Volatility": [0.002121, 0.002833, 0.003342, 0.004941, 0.005789, 0.006, 0.006529, 0.005569, 0.003737, 0.004129],
                              "Strike": [0, 0, 0, -0.02, 0.015, -0.005, 0.01, 0.01, 0.02, -0.02],
                              "Weigth": [1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
                              "p_y": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})

    with pytest.raises(syn.SensiSyntaxError):
        syn.select_from_dataframe(condition, operation, dataframe)


def test_select_from_dataframe_equal_with_bools():
    condition = "'Maturity'==TRUE"
    operation = "=="
    dataframe = pd.DataFrame({"Maturity": [1, 1, 2, 2, 20, 20, 25, 30, 50, 50],
                              "Tenor": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
                              "Volatility": [0.002121, 0.002833, 0.003342, 0.004941, 0.005789, 0.006, 0.006529, 0.005569, 0.003737, 0.004129],
                              "Strike": [0, 0, 0, -0.02, 0.015, -0.005, 0.01, 0.01, 0.02, -0.02],
                              "Weigth": [1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
                              "p_y": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})

    expected = pd.DataFrame({"Maturity": [1, 1],
                             "Tenor": [1, 2],
                             "Volatility": [0.002121, 0.002833],
                             "Strike": [0, 0],
                             "Weigth": [1, 1],
                             "p_y": [1, 1]})
    assert(pd.concat([syn.select_from_dataframe(condition, operation, dataframe), expected]).drop_duplicates(keep=False).empty)


def test_select_from_dataframe_less_than():
    condition = "'Tenor'<3"
    operation = "<"
    dataframe = pd.DataFrame({"Maturity": [1, 1, 2, 2, 20, 20, 25, 30, 50, 50],
                              "Tenor": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
                              "Volatility": [0.002121, 0.002833, 0.003342, 0.004941, 0.005789, 0.006, 0.006529, 0.005569, 0.003737, 0.004129],
                              "Strike": [0, 0, 0, -0.02, 0.015, -0.005, 0.01, 0.01, 0.02, -0.02],
                              "Weigth": [1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
                              "p_y": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})

    expected = pd.DataFrame({"Maturity": [1, 1, 30, 50],
                             "Tenor": [1, 2, 1, 2],
                             "Volatility": [0.002121, 0.002833, 0.005569, 0.003737],
                             "Strike": [0, 0, 0.01, 0.02],
                             "Weigth": [1, 1, 1, 0],
                             "p_y": [1, 1, 1, 1]}).set_index([pd.Index([0, 1, 8, 9])])
    assert(pd.concat([syn.select_from_dataframe(condition, operation, dataframe), expected]).drop_duplicates(keep=False).empty)


def test_interpret_condition_equal():
    condition = "'Maturity'==1,2"
    dataframe = pd.DataFrame({"Maturity": [1, 1, 2, 2, 20, 20, 25, 30, 50, 50],
                              "Tenor": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
                              "Volatility": [0.002121, 0.002833, 0.003342, 0.004941, 0.005789, 0.006, 0.006529, 0.005569, 0.003737, 0.004129],
                              "Strike": [0, 0, 0, -0.02, 0.015, -0.005, 0.01, 0.01, 0.02, -0.02],
                              "Weigth": [1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
                              "p_y": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})

    expected = pd.DataFrame({"Maturity": [1, 1, 2, 2],
                             "Tenor": [1, 2, 3, 4],
                             "Volatility": [0.002121, 0.002833, 0.003342, 0.004941],
                             "Strike": [0, 0, 0, -0.02],
                             "Weigth": [1, 1, 0, 1],
                             "p_y": [1, 1, 1, 1]})
    assert(pd.concat([syn.interpret_condition(condition, dataframe), expected]).drop_duplicates(keep=False).empty)


def test_interpret_condition_different():
    condition = "'Maturity'!=1,2,20,30,50,50"
    dataframe = pd.DataFrame({"Maturity": [1, 1, 2, 2, 20, 20, 25, 30, 50, 50],
                              "Tenor": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
                              "Volatility": [0.002121, 0.002833, 0.003342, 0.004941, 0.005789, 0.006, 0.006529, 0.005569, 0.003737, 0.004129],
                              "Strike": [0, 0, 0, -0.02, 0.015, -0.005, 0.01, 0.01, 0.02, -0.02],
                              "Weigth": [1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
                              "p_y": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})

    expected = pd.DataFrame({"Maturity": [25],
                             "Tenor": [7],
                             "Volatility": [0.006529],
                             "Strike": [0.01],
                             "Weigth": [0],
                             "p_y": [1]})
    assert(pd.concat([syn.interpret_condition(condition, dataframe), expected]).drop_duplicates(keep=False).empty)


def test_interpret_condition_greater_or_equal():
    condition = "'Maturity'>=50"
    dataframe = pd.DataFrame({"Maturity": [1, 1, 2, 2, 20, 20, 25, 30, 50, 50],
                              "Tenor": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
                              "Volatility": [0.002121, 0.002833, 0.003342, 0.004941, 0.005789, 0.006, 0.006529, 0.005569, 0.003737, 0.004129],
                              "Strike": [0, 0, 0, -0.02, 0.015, -0.005, 0.01, 0.01, 0.02, -0.02],
                              "Weigth": [1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
                              "p_y": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})

    expected = pd.DataFrame({"Maturity": [50, 50],
                             "Tenor": [2, 3],
                             "Volatility": [0.003737, 0.004129],
                             "Strike": [0.02, -0.02],
                             "Weigth": [0, 1],
                             "p_y": [1, 1]})
    assert(pd.concat([syn.interpret_condition(condition, dataframe), expected]).drop_duplicates(keep=False).empty)


def test_interpret_condition_greater():
    condition = "'Maturity'>30"
    dataframe = pd.DataFrame({"Maturity": [1, 1, 2, 2, 20, 20, 25, 30, 50, 50],
                              "Tenor": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
                              "Volatility": [0.002121, 0.002833, 0.003342, 0.004941, 0.005789, 0.006, 0.006529, 0.005569, 0.003737, 0.004129],
                              "Strike": [0, 0, 0, -0.02, 0.015, -0.005, 0.01, 0.01, 0.02, -0.02],
                              "Weigth": [1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
                              "p_y": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})

    expected = pd.DataFrame({"Maturity": [50, 50],
                             "Tenor": [2, 3],
                             "Volatility": [0.003737, 0.004129],
                             "Strike": [0.02, -0.02],
                             "Weigth": [0, 1],
                             "p_y": [1, 1]})
    assert(pd.concat([syn.interpret_condition(condition, dataframe), expected]).drop_duplicates(keep=False).empty)


def test_interpret_condition_less_or_equal():
    condition = "'Maturity'<=1"
    dataframe = pd.DataFrame({"Maturity": [1, 1, 2, 2, 20, 20, 25, 30, 50, 50],
                              "Tenor": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
                              "Volatility": [0.002121, 0.002833, 0.003342, 0.004941, 0.005789, 0.006, 0.006529, 0.005569, 0.003737, 0.004129],
                              "Strike": [0, 0, 0, -0.02, 0.015, -0.005, 0.01, 0.01, 0.02, -0.02],
                              "Weigth": [1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
                              "p_y": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})

    expected = pd.DataFrame({"Maturity": [1, 1],
                             "Tenor": [1, 2],
                             "Volatility": [0.002121, 0.002833],
                             "Strike": [0, 0],
                             "Weigth": [1, 1],
                             "p_y": [1, 1]})
    assert(pd.concat([syn.interpret_condition(condition, dataframe), expected]).drop_duplicates(keep=False).empty)


def test_interpret_condition_less():
    condition = "'Maturity'<2"
    dataframe = pd.DataFrame({"Maturity": [1, 1, 2, 2, 20, 20, 25, 30, 50, 50],
                              "Tenor": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
                              "Volatility": [0.002121, 0.002833, 0.003342, 0.004941, 0.005789, 0.006, 0.006529, 0.005569, 0.003737, 0.004129],
                              "Strike": [0, 0, 0, -0.02, 0.015, -0.005, 0.01, 0.01, 0.02, -0.02],
                              "Weigth": [1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
                              "p_y": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})

    expected = pd.DataFrame({"Maturity": [1, 1],
                             "Tenor": [1, 2],
                             "Volatility": [0.002121, 0.002833],
                             "Strike": [0, 0],
                             "Weigth": [1, 1],
                             "p_y": [1, 1]})
    assert(pd.concat([syn.interpret_condition(condition, dataframe), expected]).drop_duplicates(keep=False).empty)


def test_interpret_condition_invalid():
    condition = "'Maturity'!!1"
    dataframe = pd.DataFrame({"Maturity": [1, 1, 2, 2, 20, 20, 25, 30, 50, 50],
                              "Tenor": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
                              "Volatility": [0.002121, 0.002833, 0.003342, 0.004941, 0.005789, 0.006, 0.006529, 0.005569, 0.003737, 0.004129],
                              "Strike": [0, 0, 0, -0.02, 0.015, -0.005, 0.01, 0.01, 0.02, -0.02],
                              "Weigth": [1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
                              "p_y": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})

    with pytest.raises(syn.SensiSyntaxError):
        syn.interpret_condition(condition, dataframe)


def test_apply_value_to_selection_add():
    value = "(+100)"
    selected_dict = {'Maturity': {1: 1}}

    expected = {'Maturity': {1: '101.0'}}
    assert(syn.apply_value_to_selection(value, selected_dict) == expected)


def test_apply_value_to_selection_sub():
    value = "(-200)"
    selected_dict = {'Maturity': {1: 1}}

    expected = {'Maturity': {1: '-199.0'}}
    assert(syn.apply_value_to_selection(value, selected_dict) == expected)


def test_apply_value_to_selection_multiply():
    value = "(*0.000000000005)"
    selected_dict = {'Maturity': {1: 1}}

    expected = {'Maturity': {1: '5.0e-12'}}
    assert(syn.apply_value_to_selection(value, selected_dict) == expected)


def test_apply_value_to_selection_div():
    value = "(/4.0000001)"
    selected_dict = {'Maturity': {1: 1}}

    expected = {'Maturity': {1: '0.24999999375'}}
    assert(syn.apply_value_to_selection(value, selected_dict) == expected)


def test_apply_value_to_selection_string():
    value = "MIN(33.3)"
    selected_dict = {'Maturity': {1: 1}}

    expected = {'Maturity': {1: 'MIN(33.3)'}}
    assert(syn.apply_value_to_selection(value, selected_dict) == expected)


def test_apply_value_to_selection_wrong_types():
    value = "(+100)"
    selected_dict = {'Maturity': {1: "MIN(33.3)"}}

    with pytest.raises(syn.SensiSyntaxError):
        syn.apply_value_to_selection(value, selected_dict)


def test_apply_value_to_selection_scientific_notation():
    value = "(-5,000001E-04)"
    selected_dict = {'Maturity': {1: 1}}

    expected = {'Maturity': {1: '0.9994999999'}}
    assert(syn.apply_value_to_selection(value, selected_dict) == expected)


def test_apply_value_to_selection_decimal_with_comma():
    value = "(+0,00247)"
    selected_dict = {'Maturity': {1: 1}}

    expected = {'Maturity': {1: '1.00247'}}
    assert(syn.apply_value_to_selection(value, selected_dict) == expected)
    

def test_apply_value_to_selection_single_parantheses():
    value = "(-100"
    selected_dict = {'Maturity': {1: '1'}}

    expected = {'Maturity': {1: '(-100'}}
    assert(syn.apply_value_to_selection(value, selected_dict) == expected)


def test_apply_value_to_selection_empty_value():
    value = ""
    selected_dict = {'Maturity': {1: 1}}

    assert(syn.apply_value_to_selection(value, selected_dict) == selected_dict)


def test_apply_value_to_selection_empty_value_in_dict():
    value = "(+100)"
    selected_dict = {'Maturity': {1: ''}}

    with pytest.raises(syn.SensiSyntaxError):
        syn.apply_value_to_selection(value, selected_dict)


def test_apply_value_to_selection_null_value():
    value = "(- )"
    selected_dict = {'Maturity': {1: 1}}

    with pytest.raises(syn.SensiSyntaxError):
        syn.apply_value_to_selection(value, selected_dict)


def test_apply_value_to_selection_multiple_whitespaces():
    value = "(+ 100   )"
    selected_dict = {'Maturity': {1: 1}}

    expected = {'Maturity': {1: '101.0'}}
    assert(syn.apply_value_to_selection(value, selected_dict) == expected)


def test_apply_value_to_selection_bool_value():
    value = "True"
    selected_dict = {'Maturity': {1: '1'}}

    expected = {'Maturity': {1: True}}
    assert(syn.apply_value_to_selection(value, selected_dict) == expected)


def test_apply_value_to_selection_replace_value():
    value = "-100"
    selected_dict = {'Maturity': {1: '1'}}

    expected = {'Maturity': {1: '-100.0'}}
    assert(syn.apply_value_to_selection(value, selected_dict) == expected)


def test_apply_value_to_selection_apply_with_string():
    value = "(+test)"
    selected_dict = {'Maturity': {1: '1'}}

    with pytest.raises(syn.SensiSyntaxError):
        syn.apply_value_to_selection(value, selected_dict)


def test_apply_value_to_selection_apply_with_no_operation():
    value = "(10)"
    selected_dict = {'Maturity': {1: '1'}}

    expected = {'Maturity': {1: "11.0"}}
    assert(syn.apply_value_to_selection(value, selected_dict) == expected)


def test_apply_value_to_selection_replace_with_string():
    value = "test"
    selected_dict = {'Maturity': {1: '1'}}

    expected = {'Maturity': {1: "test"}}
    assert(syn.apply_value_to_selection(value, selected_dict) == expected)


@pytest.mark.parametrize("value, expected", [
    ('+0.99999998', '10.99999998'),
    ('+0.99999999', '10.99999999'),
    ('+1.00000000', '11.0'),
    ('+1.00000001', '11.00000001'),
    ('+1.00000002', '11.00000002'),
    ('-0.99999998', '9.00000002'),
    ('-0.99999999', '9.00000001'),
    ('-1.00000000', '9.0'),
    ('-1.00000001', '8.99999999'),
    ('-1.00000002', '8.99999998')
])
def test_apply_value_to_selection_with_precision(value, expected):
    value = f"({value})"

    selected_dict = {'Maturity': {1: '10'}}
    expected = {'Maturity': {1: expected}}

    assert(syn.apply_value_to_selection(value, selected_dict) == expected)


def test_apply_value_to_selection_precision_with_int():
    value = "(-50)"
    selected_dict = {'Maturity': {1: '148.2092901'}}

    expected = {'Maturity': {1: '98.2092901'}}
    assert(syn.apply_value_to_selection(value, selected_dict) == expected)


def test_apply_value_to_selection_precision_with_float():
    value = "(-49.99999999991)"
    selected_dict = {'Maturity': {1: '148.2092901'}}

    expected = {'Maturity': {1: '98.20929010009'}}
    assert(syn.apply_value_to_selection(value, selected_dict) == expected)


def test_apply_syntax_to_file():
    input_path = f'{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/Central/RN_inputs/ceF89BNhvJRc9WHMS/Nominal_rates/GBP_Mkt_Swaptions_Vols.csv'
    syntax = syn.Syntax("$..*[@.name is 'GBP']..*[@.name is 'IR'].data.swaptions.mkt.filename", "*,1", "", "(+0)")
    settings_json = sio.read_json_file(f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/settings.json")

    assert(syn.apply_syntax_to_file(input_path, syntax, settings_json) is True)
