import pytest
from data_manager import Model_Statistics_Manager, Recommendations_Manager

@pytest.fixture
def sample_Model_Statistics_Manager():
    return Model_Statistics_Manager()

@pytest.fixture
def sample_Recommendations_Manager():
    return Recommendations_Manager()

@pytest.fixture
def sample_stats_file():
    stats_file = open("./source/datasets/results/sample@statistics.txt")
    return stats_file

@pytest.fixture
def sample_recommendations_file():
    rec_file = open("./source/datasets/results/sample_recommendations.txt")
    return rec_file

"""
##############################
Model_Statistics_Manager Tests
##############################
"""

def non_formatted_valid_stats_data():
    return {
        'average_ratings': '3,328892',
        'context_conditions': '10(time:3,location:3,companion:4)',
        'context_dimensions': '3(time,location,companion)',
        'context_situations': '13',
        'data_density': '1,8230%',
        'item_mount': '79',
        'median_ratings': '4,000000',
        'mode_ratings': '5,000000',
        'rate_amount': '5035',
        'scale_distributions': '[1.0x829,2.0x625,4.0x1209,5.0x1367,3.0x1005]',
        'standard_deviation_ratings': '1,414777',
        'user_amount': '97'
    }

def non_formated_invalid_stats_data():
    return {
        'average_ratings': '3,328892',
        'context_conditions': '10(time:3,location:3,companion:4)',
        'context_dimensions': '3(time,location,companion)',
        'context_situations': '13',
        'data_density': '1,8230%',
        'item_mount': '79',
        'mode_ratings': '5,000000',
        'rate_amount': '5035',
        'scale_distributions': '[1.0x829,2.0x625,4.0x1209,5.0x1367,3.0x1005]',
        'user_amount': '97'
    }

########## format_stats(self, stats_data)


@pytest.mark.parametrize("stats_data, expected_result", [
    (
        non_formatted_valid_stats_data(),
        "statistics data successfully formatted!"
    ),
    (
        non_formated_invalid_stats_data(),
        "ERROR! statistics data dict not supported"
    )
])
def test_format_stats(sample_Model_Statistics_Manager, stats_data, expected_result):
    assert sample_Model_Statistics_Manager.format_stats(stats_data) == expected_result


########## generate_statistic_data(self, statistic_file):


def test_generate_statistic_data(sample_Model_Statistics_Manager, sample_stats_file):
    assert sample_Model_Statistics_Manager.generate_statistic_data(sample_stats_file) == non_formatted_valid_stats_data()


########## save_statistics(self):
@pytest.mark.parametrize("file_path, expected_result",[
    ("./source/datasets/results/sample@statistics.txt",
    "The file execution_statistics.json was successfully created!"),
    ("./source/datasets/results/avbnbqd.txt",
    "ERROR! The file ./source/datasets/results/avbnbqd.txt could not be opened.")
])
def test_save_statistics(sample_Model_Statistics_Manager, file_path, expected_result):
    assert sample_Model_Statistics_Manager.save_statistics(file_path) == expected_result


"""
##############################
Recommendations_Manager Tests
##############################
"""


########## save_recommendations(self):

@pytest.mark.parametrize("results_file, expected_result", [
    (
        "./source/datasets/results/sample_recommendations.txt",
    "The file sample_recommendations.json was successfully created!"
    ),
    (
        "./source/datasets/results/edcveadw.txt",
        "ERROR! The file ./source/datasets/results/edcveadw.txt could not be opened."
    )
])
@pytest.mark.data_writing
def test_save_recommendations(sample_Recommendations_Manager, results_file, expected_result):
    assert sample_Recommendations_Manager.save_recommendations(results_file) == expected_result