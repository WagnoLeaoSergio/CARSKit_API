import os
import pytest
import pathlib as pl
from run_carskit import Runner

from ..controllers.data_processing import get_app_path


@pytest.fixture
def java_file_path():
    app_path = get_app_path()
    return os.path.join(app_path, "carskit/")


def test_run_engine(java_file_path):
    runner = Runner(java_file_path)
    OK_CODE = 0
    assert runner.run_engine() == OK_CODE