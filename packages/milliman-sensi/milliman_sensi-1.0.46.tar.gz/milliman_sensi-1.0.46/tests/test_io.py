import inspect
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest

import milliman_sensi.io as sio

TEST_DIR = os.path.dirname(inspect.getfile(inspect.currentframe())).replace("\\", "/")


def test_read_json_successful():
    data = sio.read_json_file(f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/settings.json")
    assert(data is not None)


def test_read_json_failed():
    with pytest.raises(FileNotFoundError):
        sio.read_json_file(f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/not_exists.json")


def test_find_file_in_directory_with_directory_inexistant():
    assert(sio.find_file_in_directory("searched_file.csv", "inexistant_directory") is None)


def test_find_file_in_directory_with_file_inexistant():
    assert(sio.find_file_in_directory("searched_file.csv", ".") is None)


def test_validate_sensi_config_with_incorrect_csv():
    sensi_config_bad_path = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_config_bad_csv.csv"
    assert(sio.validate_sensi_config(sensi_config_bad_path) == "Rows with additional columns are [1, 3]\nRows with fewer columns are [5]")


def test_validate_sensi_config_with_incorrect_header():
    sensi_config_bad_path = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_config_incorrect_header.csv"
    assert(sio.validate_sensi_config(
        sensi_config_bad_path) == "'Sensi_config.csv': 'Scenario_123' is incorrect, should be 'Scenario'\n'Sensi_config.csv': 'Stress name123' is incorrect, should be 'Stress name'")


def test_validate_sensi_config_with_missing_header():
    sensi_config_bad_path = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_config_missing_header.csv"
    assert(sio.validate_sensi_config(
        sensi_config_bad_path) == "'Sensi_config.csv': 'Apply stress' is missing\n'Sensi_config.csv': 'Stress name' is missing")


def test_validate_sensi_config_with_extra_header():
    sensi_config_bad_path = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_config_extra_header.csv"
    assert(sio.validate_sensi_config(
        sensi_config_bad_path) == "'Sensi_config.csv': 'Remove stress' is extra\n'Sensi_config.csv': 'Stress value' is extra")


def test_validate_sensi_config_with_incorrect_values_in_Apply_stress():
    sensi_config_bad_path = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_config_incorrect_values_in_Apply_stress.csv"
    assert(sio.validate_sensi_config(
        sensi_config_bad_path) == "'Sensi_config.csv': 'Apply stress' has incorrect entry at row(s) [1]")


def test_validate_sensi_config_with_empty_input_file():
    sensi_config_bad_path = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_config_empty.csv"
    assert(sio.validate_sensi_config(
        sensi_config_bad_path) == "Empty csv file passed. Check the input")


def test_validate_sensi_config_with_invalid_character():
    sensi_config_bad_path = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_config_with_invalid_char.csv"
    assert(sio.validate_sensi_config(
        sensi_config_bad_path) == "Failed to parse a csv file")   


def test_validate_sensi_config_with_invalid_separator():
    sensi_config_bad_path = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_config_with_invalid_sep.csv"
    assert(sio.validate_sensi_config(
        sensi_config_bad_path) == "The input csv contains the invalid separator '~'")    


def test_validate_sensi_param_with_incorrect_csv():
    sensi_param_bad_path = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_param_bad_csv.csv"
    assert(sio.validate_sensi_param(
        sensi_param_bad_path) == "Rows with additional columns are [1]\nRows with fewer columns are [2, 4, 6]")


def test_validate_sensi_param_without_Name():
    sensi_param_bad_path = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_param_missing_Name.csv"
    assert(sio.validate_sensi_param(
        sensi_param_bad_path) == "Missing column 'Name' in Sensi_param.csv")


def test_read_sensitivities():
    env_dir = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857"
    sensi_list, sensi_list_without_any_stress, param_map = sio.read_sensitivities(env_dir)
    assert(sensi_list == {'Sensi_1': ['Stress_vol_1']})

    assert(param_map == {'Stress_vol_1': ['param.n_s=500']})


def test_copy_dir_nested_files_and_subdirs():
    temp_dir = tempfile.mkdtemp()
    base_rsrc_dir = os.path.join(temp_dir, 'base_rsrc_dir')
    sensi_rsrc_dir = os.path.join(temp_dir, 'sensi_rsrc_dir')
    try:
        os.makedirs(base_rsrc_dir)
        temp_subdir1 = os.path.join(base_rsrc_dir, 'subdir1')
        temp_subdir2 = os.path.join(base_rsrc_dir, 'subdir2')
        os.makedirs(temp_subdir1)
        os.makedirs(temp_subdir2)
        temp_file1 = os.path.join(base_rsrc_dir, 'file1.txt')
        temp_file2 = os.path.join(temp_subdir1, 'file2.txt')
        with open(temp_file1, 'w') as f1, open(temp_file2, 'w') as f2:
            f1.write('File 1 contents')
            f2.write('File 2 contents')

        sio.copy_dir(base_rsrc_dir, sensi_rsrc_dir)

        assert os.path.exists(os.path.join(sensi_rsrc_dir, 'file1.txt'))
        assert os.path.exists(os.path.join(sensi_rsrc_dir, 'subdir1', 'file2.txt'))
        assert os.path.isfile(os.path.join(sensi_rsrc_dir, 'file1.txt'))
        assert os.path.isfile(os.path.join(sensi_rsrc_dir, 'subdir1', 'file2.txt'))
        assert os.path.isdir(os.path.join(sensi_rsrc_dir, 'subdir2'))
    finally:
        shutil.rmtree(temp_dir)

@pytest.mark.skipif(sys.platform != 'linux', reason='Symlinks only supported on Linux')
def test_copy_dir_symlink_point_to_dir():
    temp_dir = tempfile.mkdtemp()
    base_rsrc_dir = os.path.join(temp_dir, 'base_rsrc_dir')
    sensi_rsrc_dir = os.path.join(temp_dir, 'sensi_rsrc_dir')
    try:
        os.makedirs(base_rsrc_dir)
        temp_subdir = os.path.join(temp_dir, 'subdir')
        os.makedirs(temp_subdir)
        temp_file = os.path.join(temp_subdir, 'file1.txt')
        with open(temp_file, 'w') as f:
            f.write('File 1 contents')
        
        temp_link = os.path.join(base_rsrc_dir, 'symlink')
        os.symlink(temp_subdir, temp_link)
        
        sio.copy_dir(base_rsrc_dir, sensi_rsrc_dir)
        
        assert os.path.exists(os.path.join(sensi_rsrc_dir, 'symlink', 'file1.txt'))

    finally:
        shutil.rmtree(temp_dir)

@pytest.mark.skipif(sys.platform != 'linux', reason='Symlinks only supported on Linux')
def test_copy_dir_skip_dangling_symlink():
    temp_dir = tempfile.mkdtemp()
    base_rsrc_dir = os.path.join(temp_dir, 'base_rsrc_dir')
    sensi_rsrc_dir = os.path.join(temp_dir, 'sensi_rsrc_dir')    
    try:
        os.makedirs(base_rsrc_dir)
        temp_link = os.path.join(base_rsrc_dir, 'symlink')
        os.symlink('/path/to/nonexistent/target', temp_link)

        sio.copy_dir(base_rsrc_dir, sensi_rsrc_dir)

        assert not os.path.exists(os.path.join(sensi_rsrc_dir, 'symlink'))
    finally:
        shutil.rmtree(temp_dir)

def test_copy_dir_existing_destination():
    temp_dir = tempfile.mkdtemp()
    base_rsrc_dir = os.path.join(temp_dir, 'base_rsrc_dir')
    sensi_rsrc_dir = os.path.join(temp_dir, 'sensi_rsrc_dir')    
    try:
        os.makedirs(base_rsrc_dir)
        temp_file = os.path.join(base_rsrc_dir, 'file.txt')
        with open(temp_file, 'w') as f:
            f.write('File contents')

        # Create an existing directory in the destination path
        os.makedirs(os.path.join(sensi_rsrc_dir, 'existing_dir'))

        sio.copy_dir(base_rsrc_dir, sensi_rsrc_dir)

        assert os.path.isdir(os.path.join(sensi_rsrc_dir, 'existing_dir'))
        assert not os.path.isfile(os.path.join(sensi_rsrc_dir, 'existing_dir', 'file.txt'))
    finally:
        shutil.rmtree(temp_dir)


def test_create_dir_for_one_sensi_from_base_dir_doesnt_exist():
    sensi_name = "test_sensi"
    base_dir = "inexistant_directory"
    res = sio.create_dir_for_one_sensi_from_base(sensi_name, base_dir)
    if isinstance(res, sio.SensiIOError):
        assert(True)


def test_create_dir_for_one_sensi_from_sensi_path(tmpdir):
    sensi_name = "test_sensi"
    base_dir = f"{TEST_DIR}/LMMP_Up_31122020_RN_Simulation"

    tmpath = str(tmpdir.mkdir("test_sensi_path")).replace("\\", "/")
    sensi_path = f"{tmpath}/test_create_one_sensi_from_sensi_path"
    os.mkdir(sensi_path)

    base_dir_list = os.listdir(base_dir)
    path_to_sensi = sio.create_dir_for_one_sensi_from_base(sensi_name, base_dir, sensi_path)
    assert(path_to_sensi == sensi_path and os.path.exists(path_to_sensi) is True)

    path_to_sensi_list = os.listdir(path_to_sensi)
    print(path_to_sensi_list)
    number_files_in_sensi = len(path_to_sensi_list)
    assert(number_files_in_sensi == 1)


def test_get_stress_desc():
    env_dir = f"{TEST_DIR}/LMMP_Up_31122020_RN_Simulation"
    test_SensiConfig = sio.SensiConfig(env_dir)
    assert(test_SensiConfig.get_stress_desc("Sensi_2") == """file::eco[EUR].driver[RIR].data.init_curve.mkt['BEIR rate',1]=(-0.023933085882)>>file::eco[EUR].driver[RIR].data.init_curve.mkt['BEIR rate',2]=(-0.023933085882)>>file::eco[EUR].driver[RIR].data.init_curve.mkt['BEIR rate',3]=(-0.023933085882)>>file::eco[EUR].driver[RIR].data.init_curve.mkt['BEIR rate',4]=(-0.023863016373)>>file::eco[EUR].driver[RIR].data.init_curve.mkt['BEIR rate',5]=(-0.023574089337)""")


def test_create_tables(tmpdir):
    env_dir = f"{TEST_DIR}/LMMP_Up_31122020_RN_Simulation"
    test_SensiConfig = sio.SensiConfig(env_dir)

    tmpath = str(tmpdir.mkdir("test_create_tables")).replace("\\", "/")
    sensi_1_dir = f'{tmpath}/Sensi_1'
    os.mkdir(sensi_1_dir)
    sensi_dirs = {'Sensi_1': sensi_1_dir}

    assert(test_SensiConfig.create_tables(sensi_dirs) == sensi_dirs)


def test_apply(tmpdir):
    env_dir = f"{TEST_DIR}/LMMP_Up_31122020_RN_Simulation"
    test_SensiConfig = sio.SensiConfig(env_dir)

    test_sensi_path = str(tmpdir.mkdir("test_sensi_path")).replace("\\", "/")
    if os.path.exists(test_sensi_path):
        shutil.rmtree(test_sensi_path)

    shutil.copytree(f'{TEST_DIR}/test_apply_bnp_backup', test_sensi_path)

    sensi_dirs = {'Sensi_1': f'{test_sensi_path}/Sensi_1',
                  'Sensi_2': f'{test_sensi_path}/Sensi_2'}

    expected_apply = {'Sensi_1': 'Applied 11 modification(s) on Sensi_1',
                      'Sensi_2': 'Applied 5 modification(s) on Sensi_2'}
    res_apply = test_SensiConfig.apply(sensi_dirs)
    assert(res_apply == expected_apply)


def test_apply_only_settings_modif(tmpdir):
    env_dir = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857"
    test_SensiConfig = sio.SensiConfig(env_dir)

    test_sensi_path = str(tmpdir.mkdir("test_sensi_path")).replace("\\", "/")
    if os.path.exists(test_sensi_path):
        shutil.rmtree(test_sensi_path)

    shutil.copytree(f'{TEST_DIR}/test_apply_backup', test_sensi_path)

    sensi_dirs = {'Sensi_1': f'{test_sensi_path}/Sensi_1'}

    expected_apply = {'Sensi_1': 'Applied 1 modification(s) on Sensi_1'}

    res_apply = test_SensiConfig.apply(sensi_dirs)
    assert(res_apply == expected_apply)
