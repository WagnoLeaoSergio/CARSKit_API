import os
import pytest
from edit_settings import Settings_Editor

# @pytest.fixture
# def settings_editor_sample():
#     return Settings_Editor()

se = Settings_Editor()

""" Setters """

@pytest.mark.parametrize("dataset_path, expected_result", [
    (12, False),
    ("", False),
    ("dawdwfw", False),
    ("./source/datasets/ratings.txt", True),
    (os.path.abspath("./source/datasets/ratings.txt"), True)
])
def test_set_dataset_path(dataset_path, expected_result):
    assert se.set_dataset_path(dataset_path) == expected_result

@pytest.mark.parametrize("results_path, expected_result", [
    (12, False),
    ("", False),
    ("dawdwfw", False),
    ("./source/datasets/results/", True),
    (os.path.abspath("./source/datasets/results/"), True)
])
def test_set_results_path(results_path, expected_result):
    assert se.set_results_path(results_path) == expected_result


@pytest.mark.parametrize("algorithm, expected_result", [
    (41231, False),
    ("", False),
    ("goieoawpd", False),
    ("fdp", False),
    ("CAMF_CU", True),
    ("camf_cu", True)
])
def test_set_algorithm(algorithm, expected_result):
    assert se.set_algorithm(algorithm) == expected_result

# A averiguar...
def test_set_parameters():
    pass

""" Getters """

def test_get_dataset_path():
    se.set_dataset_path(os.path.abspath("./source/datasets/ratings.txt"))
    assert se.get_dataset_path() == os.path.abspath("./source/datasets/ratings.txt")

def test_get_results_path():
    se.set_results_path(os.path.abspath("./source/datasets/results/"))
    assert se.get_results_path() == os.path.abspath("./source/datasets/results/")

def test_get_algorithm():
    available_algorithms = [
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
    assert se.get_algorithm() in available_algorithms


# A averiguar...
def test_get_parameters():
    pass

################

def test_load_settings():
    ok_messages = [
        "no previous settings, DB initialized",
        "settings loaded"
    ]
    assert se.load_settings() in ok_messages

def test_save_settings():
    assert se.save_settings() == True

def test_generate_file():
    se.set_dataset_path(os.path.abspath("./source/datasets/ratings.txt"))
    ok_message = "The file was generated!"
    assert se.generate_file() == ok_message