import os
import subprocess


class Runner(object):
    """
    Class that runs the CARSKit java file.
    It is only need the complete or relative path to the file to run it.
    """

    def __init__(self, javaFile_path: str):
        self.javaFile_path = javaFile_path
        self.current_path = os.path.abspath(os.getcwd())

    def run_engine(self) -> str:
        """
        Runs the Java file and return the output of the execution.
        """
        os.chdir(self.javaFile_path)
        output = subprocess.call(
            ['java', '-jar', 'CARSKit-v0.3.5.jar', '-c', 'setting.conf'])
        os.chdir(self.current_path)
        return output
