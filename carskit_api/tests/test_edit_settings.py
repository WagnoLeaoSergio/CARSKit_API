import os
import pytest
from ..editors import Settings_Editor
from ..controllers.data_processing import get_app_path


@pytest.fixture
def valid_dataset_path():
    return "/home/wagno/Documents/data_test/musicInCar.csv"


@pytest.fixture
def valid_settings_editor():
    app_path = get_app_path()
    return Settings_Editor(file_path=os.path.join(app_path, "carskit/setting.conf"))


@pytest.fixture
def available_algorithms():
    return [
        "itemknn",
        "userknn",
        "slopeone",
        "pmf",
        "bpmf",
        "biasedmf",
        "nmf",
        "svd++",
        "usersplitting",
        "itemsplitting",
        "uisplitting",
        "spf",
        "dcr",
        "dcw",
        "cptf",
        "camf_ci",
        "camf_cu",
        "camf_cuci",
        "cslim_ci",
        "cslim_cu",
        "cslim_cuci",
        "gcslim_cc",
        "cslim_ics",
        "cslim_lcs",
        "cslim_mcs",
        "gcslim_ics",
        "gcslim_lcs",
        "gcslim_mcs",
    ]


""" Setters """


@pytest.mark.parametrize(
    "dataset_path, expected_result",
    [
        (12, "ERROR! Path Invalid."),
        ("", "ERROR! Path Invalid."),
        ("dawdwfw", "ERROR! Path Invalid."),
        (
            "/home/wagno/Documents/data_test/musicInCar.csv",
            "/home/wagno/Documents/data_test/musicInCar.csv",
        ),
    ],
)
def test_set_dataset_path(valid_settings_editor, dataset_path, expected_result):
    assert valid_settings_editor.set_dataset_path(dataset_path) == expected_result


@pytest.mark.parametrize(
    "folder_name, expected_result",
    [
        (12, "ERROR! Name Invalid."),
        ("", "ERROR! The name is empty."),
        ("dawdwfw", "dawdwfw"),
        ("results", "results"),
    ],
)
def test_set_results_foldername(valid_settings_editor, folder_name, expected_result):
    assert valid_settings_editor.set_results_foldername(folder_name) == expected_result


@pytest.mark.parametrize(
    "algorithm, expected_result",
    [
        (41231, "ERROR! Algorithm not available."),
        ("", "ERROR! Algorithm not available."),
        ("goieoawpd", "ERROR! Algorithm not available."),
        ("fdp", "ERROR! Algorithm not available."),
        ("CAMF_CU", "camf_cu"),
        ("camf_cu", "camf_cu"),
    ],
)
def test_set_algorithm(valid_settings_editor, algorithm, expected_result):
    assert valid_settings_editor.set_algorithm(algorithm) == expected_result


@pytest.mark.parametrize(
    "parameter_key, parameter_value,expected_result",
    [
        ("dfsff", 123, "ERROR! operation invalid."),
        ("topN", 20, "configuration setted"),
        ("k_folds", 3, "configuration setted"),
        ("random_seed", 2, "configuration setted"),
        ("num_factors", 12, "configuration setted"),
        ("num_max_iterations", 200, "configuration setted"),
        ("learning_rate", 2e-3, "configuration setted"),
        ("reg_lambda", 0.0004, "configuration setted"),
        ("num_neighboors", 5, "configuration setted"),
        ("similarity", "cos", "configuration setted"),
    ],
)
def test_set_parameter(
    valid_settings_editor, parameter_key, parameter_value, expected_result
):
    assert (
        valid_settings_editor.set_parameter(parameter_key, parameter_value)
        == expected_result
    )


""" Getters """


def test_get_dataset_path(valid_settings_editor, valid_dataset_path):
    valid_settings_editor.set_dataset_path(valid_dataset_path)
    assert valid_settings_editor.get_dataset_path() == valid_dataset_path


@pytest.mark.parametrize(
    "folder_name, expected_result",
    [
        ("", "results"),
        ("outputs", "outputs"),
        ("12234", "outputs"),
    ],
)
def test_get_results_foldername(valid_settings_editor, folder_name, expected_result):
    valid_settings_editor.set_results_foldername(folder_name)
    assert valid_settings_editor.get_results_foldername() == expected_result


def test_get_algorithm(valid_settings_editor, available_algorithms):
    assert valid_settings_editor.get_algorithm() in available_algorithms


@pytest.mark.parametrize(
    "parameter_key, parameter_value, expected_result",
    [
        ("", "faeaew", "ERROR! operation invalid."),
        ("dgsaegf", "htysg", "ERROR! operation invalid."),
        ("topN", 10, 10),
        ("k_folds", 5, 5),
        ("random_seed", 1, 1),
        ("num_factors", 10, 10),
        ("num_max_iterations", 100, 100),
        ("learning_rate", 2e-2, 2e-2),
        ("reg_lambda", 0.0001, 0.0001),
        ("num_neighboors", 10, 10),
        ("similarity", "pcc", "pcc"),
    ],
)
def test_get_parameters(
    valid_settings_editor, parameter_key, parameter_value, expected_result
):
    set_status = valid_settings_editor.set_parameter(parameter_key, parameter_value)
    if set_status == "configuration setted":
        assert valid_settings_editor.get_parameter(parameter_key) == expected_result
    else:
        assert set_status == expected_result


################


def test_load_settings(valid_settings_editor):
    ok_messages = ["no previous settings, DB initialized", "settings loaded"]
    assert valid_settings_editor.load_settings() in ok_messages


def test_save_settings(valid_settings_editor):
    assert valid_settings_editor.save_settings() == "settings saved"


@pytest.mark.parametrize(
    "dataset_path, expected_result",
    [
        (
            "/home/wagno/Documents/data_test/musicInCar.csv",
            "The settings file was generated!",
        ),
    ],
)
def test_generate_file(valid_settings_editor, dataset_path, expected_result):
    valid_settings_editor.set_dataset_path(dataset_path)
    assert valid_settings_editor.generate_file() == expected_result