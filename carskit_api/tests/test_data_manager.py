import os
import pytest
from ..managers import Model_Statistics_Manager, Recommendations_Manager
from ..controllers.data_processing import get_app_path


def tests_path():
    return os.path.join(get_app_path(), "tests/")


@pytest.fixture
def sample_Model_Statistics_Manager():
    return Model_Statistics_Manager(output_folder="results")


@pytest.fixture
def sample_Recommendations_Manager():
    return Recommendations_Manager(output_folder="results")


@pytest.fixture
def sample_stats_file():
    stats_file = open(tests_path() + "sample_statistics.txt")
    return stats_file


@pytest.fixture
def sample_recommendations_file():
    rec_file = open(tests_path() + "/sample_recommendations.txt")
    return rec_file


"""
##############################
Model_Statistics_Manager Tests
##############################
"""


def formatted_valid_stats_data():
    return {
        "user_amount": "97",
        "item_mount": "79",
        "rate_amount": "5035",
        "context_dimensions": "3(time,location,companion)",
        "context_conditions": "10(time:3,location:3,companion:4)",
        "context_situations": "13",
        "data_density": "1.8230%",
        "scale_distributions": [
            "1.0x829",
            "2.0x625",
            "4.0x1209",
            "5.0x1367",
            "3.0x1005",
        ],
        "average_ratings": "3.328892",
        "standard_deviation_ratings": "1.414777",
        "mode_ratings": "5.000000",
        "median_ratings": "4.000000",
    }


def non_formatted_valid_stats_data():
    return {
        "user_amount": "97",
        "item_mount": "79",
        "rate_amount": "5035",
        "context_dimensions": "3(time,location,companion)",
        "context_conditions": "10(time:3,location:3,companion:4)",
        "context_situations": "13",
        "data_density": "1.8230%",
        "scale_distributions": "[1.0x829,2.0x625,4.0x1209,5.0x1367,3.0x1005]",
        "average_ratings": "3.328892",
        "standard_deviation_ratings": "1.414777",
        "mode_ratings": "5.000000",
        "median_ratings": "4.000000",
    }


def non_formated_invalid_stats_data():
    return {
        "average_ratings": "3,328892",
        "context_conditions": "10(time:3,location:3,companion:4)",
        "context_dimensions": "3(time,location,companion)",
        "context_situations": "13",
        "data_density": "1,8230%",
        "item_mount": "79",
        "mode_ratings": "5,000000",
        "rate_amount": "5035",
        "scale_distributions": "[1.0x829,2.0x625,4.0x1209,5.0x1367,3.0x1005]",
        "user_amount": "97",
    }


########## format_stats(self, stats_data)


@pytest.mark.parametrize(
    "stats_data, expected_result",
    [
        (non_formatted_valid_stats_data(), "statistics data successfully formatted!"),
        (
            non_formated_invalid_stats_data(),
            "ERROR! statistics data dict not supported",
        ),
    ],
)
def test_format_stats(sample_Model_Statistics_Manager, stats_data, expected_result):
    formating_status = sample_Model_Statistics_Manager.format_stats(stats_data)
    assert formating_status == expected_result


########## generate_statistic_data(self, statistic_file):


def test_generate_statistic_data(sample_Model_Statistics_Manager, sample_stats_file):
    generated_data = sample_Model_Statistics_Manager.generate_statistic_data(
        sample_stats_file
    )
    assert isinstance(generated_data, dict) and all(
        k in generated_data
        for k in (
            "user_amount",
            "item_mount",
            "rate_amount",
            "context_dimensions",
            "context_conditions",
            "context_situations",
            "data_density",
            "scale_distributions",
            "average_ratings",
            "standard_deviation_ratings",
            "mode_ratings",
            "median_ratings",
        )
    )


########## save_statistics(self):
@pytest.mark.parametrize(
    "file_path, expected_result",
    [
        (
            tests_path() + "sample@statistics.json",
            "The file sample@statistics.json was successfully created!",
        ),
    ],
)
def test_save_statistics(sample_Model_Statistics_Manager, file_path, expected_result):
    assert (
        sample_Model_Statistics_Manager.save_statistics(
            non_formatted_valid_stats_data(), file_path
        )
        == expected_result
    )


"""
##############################
Recommendations_Manager Tests
##############################
"""


########## save_recommendations(self):


@pytest.mark.parametrize(
    "results_filepath, expected_result",
    [
        (
            tests_path() + "sample@recommendations.json",
            "The file sample@recommendations.json was successfully created!",
        ),
    ],
)
@pytest.mark.data_writing
def test_save_recommendations(
    sample_Recommendations_Manager,
    sample_recommendations_file,
    results_filepath,
    expected_result,
):
    sample_recs = sample_Recommendations_Manager.generate_recommendations_data(
        sample_recommendations_file
    )
    assert (
        sample_Recommendations_Manager.save_recommendations(
            sample_recs, results_filepath
        )
        == expected_result
    )
