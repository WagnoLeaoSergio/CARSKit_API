import os
import subprocess

def run_engine():
    current_path = os.path.abspath(os.getcwd())
    path = current_path + "\\CARSKit"
    os.chdir(path)
    subprocess.call(['java', '-jar', 'CARSKit-v0.3.5.jar', 'setting.conf'])

run_engine()
