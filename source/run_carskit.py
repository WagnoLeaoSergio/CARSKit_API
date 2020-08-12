import os
import subprocess

class Runner(object):
    def __init__(self, javaFile_path):
        self.javaFile_path = javaFile_path
        self.current_path = os.path.abspath(os.getcwd())

    def run_engine(self):
        #print('basename:    ', os.path.basename(__file__))
        #print('dirname:     ', os.path.dirname(__file__))
        #print('getcwd:      ', os.getcwd())
        #print('__file__:    ', __file__)

        #current_path = os.path.abspath(os.getcwd())
        #path = current_path + "\\CARSKit"
        os.chdir(self.javaFile_path)
        output = subprocess.call(['java', '-jar', 'CARSKit-v0.3.5.jar', 'setting.conf'])
        os.chdir(self.current_path)
        return output

