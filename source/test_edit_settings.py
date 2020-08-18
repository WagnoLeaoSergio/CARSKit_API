import os
import pytest
from edit_settings import Settings_Editor

@pytest.fixture
def sample_settings_editor():
    return Settings_Editor()

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
        "gcslim_mcs"
    ]

""" Setters """

@pytest.mark.parametrize("dataset_path, expected_result", [
    (12, False),
    ("", False),
    ("dawdwfw", False),
    ("./source/datasets/ratings.txt", True),
    (os.path.abspath("./source/datasets/ratings.txt"), True)
])
def test_set_dataset_path(sample_settings_editor, dataset_path, expected_result):
    assert sample_settings_editor.set_dataset_path(dataset_path) == expected_result

@pytest.mark.parametrize("results_path, expected_result", [
    (12, False),
    ("", False),
    ("dawdwfw", False),
    ("./source/datasets/results/", True),
    (os.path.abspath("./source/datasets/results/"), True)
])
def test_set_results_path(sample_settings_editor, results_path, expected_result):
    assert sample_settings_editor.set_results_path(results_path) == expected_result


@pytest.mark.parametrize("algorithm, expected_result", [
    (41231, False),
    ("", False),
    ("goieoawpd", False),
    ("fdp", False),
    ("CAMF_CU", True),
    ("camf_cu", True)
])
def test_set_algorithm(sample_settings_editor, algorithm, expected_result):
    assert sample_settings_editor.set_algorithm(algorithm) == expected_result


@pytest.mark.parametrize("parameter_key, parameter_value,expected_result", [
    ("topN", 20, True),
    ("k_folds", 3, True),
    ("random_seed", 2, True),
    ("num_factors", 12, True),
    ("num_max_iterations", 200, True),
    ("learning_rate", 2e-3, True),
    ("reg_lambda", 0.0004, True),
    ("num_neighboors", 5, True),
    ("similarity", "cos", True)
])
def test_set_parameter(sample_settings_editor, parameter_key, parameter_value, expected_result):
    assert sample_settings_editor.set_parameter(parameter_key, parameter_value) == expected_result
""" Getters """

def test_get_dataset_path(sample_settings_editor):
    sample_settings_editor.set_dataset_path(os.path.abspath("./source/datasets/ratings.txt"))
    assert sample_settings_editor.get_dataset_path() == os.path.abspath("./source/datasets/ratings.txt")

def test_get_results_path(sample_settings_editor):
    sample_settings_editor.set_results_path(os.path.abspath("./source/datasets/results/"))
    assert sample_settings_editor.get_results_path() == os.path.abspath("./source/datasets/results/")

def test_get_algorithm(sample_settings_editor, available_algorithms):
    assert sample_settings_editor.get_algorithm() in available_algorithms


@pytest.mark.parametrize("parameter_key, expected_result", [
    ("topN", 10),
    ("k_folds", 5),
    ("random_seed", 1),
    ("num_factors", 10),
    ("num_max_iterations", 100),
    ("learning_rate", 2e-2),
    ("reg_lambda", 0.0001),
    ("num_neighboors", 10),
    ("similarity", "pcc")
])
def test_get_parameters(sample_settings_editor, parameter_key, expected_result):
    assert sample_settings_editor.get_parameter(parameter_key) == expected_result

################

def test_load_settings(sample_settings_editor):
    ok_messages = [
        "no previous settings, DB initialized",
        "settings loaded"
    ]
    assert sample_settings_editor.load_settings() in ok_messages

def test_save_settings(sample_settings_editor):
    assert sample_settings_editor.save_settings() == True

def test_generate_file(sample_settings_editor):
    sample_settings_editor.set_dataset_path(os.path.abspath("./source/datasets/ratings.txt"))
    ok_message = "The file was generated!"
    assert sample_settings_editor.generate_file() == ok_message