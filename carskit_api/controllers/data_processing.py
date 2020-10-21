import os
import glob
import datetime
import pathlib as pl

from cryptography.fernet import Fernet


def get_app_path():
    return pl.Path(os.path.dirname(os.path.abspath(__file__))).parent


def latest_execution_data(app_path, dataset_path, results_foldername):
    data_filenames = glob.glob(
        os.path.join(
            app_path,
            os.path.dirname(dataset_path),
            f"{results_foldername}/*",
        )
    )

    data_filenames.sort(key=os.path.getctime, reverse=True)
    # return list(map(os.path.basename, data_filenames))
    return data_filenames


def create_file_names():
    current_time = datetime.datetime.today().strftime("%Y-%m-%d-%H:%M:%S")
    stats_filename = f"execution@{current_time}"
    recs_filename = f"recomendations@{current_time}"
    return stats_filename, recs_filename


def extract_stat_data(stats_manager, stats_filepath):
    stats_file = open(stats_filepath)
    execution_stats = stats_manager.generate_statistic_data(stats_file)
    stats_file.close()

    return execution_stats


def extract_recommendations(recs_manager, recs_filepath):
    recommendations_file = open(recs_filepath)
    recommendations = recs_manager.generate_recommendations_data(recommendations_file)
    recommendations_file.close()

    return recommendations


def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)


def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)