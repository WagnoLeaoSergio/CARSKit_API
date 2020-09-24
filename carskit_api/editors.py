import os
import sys
import pathlib as pl
import subprocess
import pickledb


class Settings_Editor(object):
    """
    Class that manage all the parameters needed to
    generate the configuration file (setting.conf) for the engine.
    The configuration file path need to be specified.
    """

    def __init__(self, file_path: str):

        self.__op_system = sys.platform
        self.file_path = os.path.abspath(file_path)

        # self.db = pickledb.load("./carskit_api/settings_data.json", True)
        self.db = pickledb.load(
            os.path.join(
                pl.Path(self.file_path).parent,
                "settings_data.json"),
            True
        )

        self.__dataset_path = "None"

        # Talvez isso deixe de ser um path e vire só o nome da pasta
        # self.__results_foldername = os.path.join(
        #    pl.Path(self.file_path).parent.parent, "dataset/results/")
        self.__results_foldername = "results"

        self.__algorithm = "camf_cu"

        """
        Para as configurações de algoritmos específicos talvez seja necessário o uso de expressões regulares
        """

        self.__parameters = {
            "file_path": self.file_path,
            "dataset_path": self.__dataset_path,
            "results_foldername": self.__results_foldername,
            "algorithm": self.__algorithm,
            "topN": 10,
            "k_folds": 5,
            "random_seed": 1,
            "num_factors": 10,
            "num_max_iterations": 100,
            "learning_rate": 2e-2,
            "reg_lambda": 0.0001,
            "num_neighboors": 10,
            "similarity": "pcc",  # availables: pcc, cos, cos-binary, msd, cpc
        }

        self.__available_algorithms = [
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

        if not self.db.get("parameters"):
            self.save_settings()
        self.load_settings()

    def set_dataset_path(self, path: str) -> str:
        """
        Define and validate the path to the dataset that is going
        to be used and returns a message about the operation's success.
        """

        if isinstance(path, str) and os.path.exists(path):
            self.__dataset_path = os.path.abspath(path)
            self.__parameters["dataset_path"] = self.__dataset_path

            return self.__dataset_path
        return "ERROR! Path Invalid."

    def get_dataset_path(self) -> str:
        return self.__dataset_path

    def set_results_foldername(self, name: str) -> str:
        """
        Define and validate the name for the results that the engine will generate
        and returns a message about the operation's success.
        """
        if isinstance(name, str):
            self.__results_foldername = name
            self.__parameters["results_foldername"] = self.__results_foldername

            return self.__results_foldername
        return "ERROR! Path Invalid."

    def get_results_foldername(self) -> str:
        return self.__results_foldername

    def set_algorithm(self, algo: str) -> str:
        """
        Define and validate the algorithm that is going
        to be used and returns a message about the operation's success.
        """

        if isinstance(algo, str) and algo != "":
            if algo.lower() in self.__available_algorithms:
                self.__algorithm = algo.lower()
                self.__parameters["algorithm"] = self.__algorithm

                return self.__algorithm
        return "ERROR! Algorithm not available."

    def get_algorithm(self) -> str:
        return self.__algorithm

    def set_parameter(self, key: str, value: str) -> str:
        """
        Define and validate a parameter for the next engine's execution
        and returns a message about the operation's success.
        """
        if key == "dataset_path":
            return self.set_dataset_path(value)
        elif key == "results_foldername":
            return self.set_results_foldername(value)
        elif key == "algorithm":
            return self.set_algorithm(value)
        else:
            if isinstance(key, str) and key in self.__parameters:
                self.__parameters[key] = value
                return "configuration setted"
            else:
                return "ERROR! operation invalid."

    def get_parameter(self, key: str) -> dict:
        if isinstance(key, str) and key in self.__parameters:
            return self.__parameters[key]
        else:
            return "ERROR! operation invalid."

    def load_settings(self) -> str:
        """
        Try to load the settings configuration from the file 'settings_data.db'
        and return an operation message.
        """
        if not self.db:
            return "ERROR! No Database connected!"

        self.__parameters = self.db.get("parameters")

        self.__file_path = self.__parameters["file_path"]
        self.__dataset_path = self.__parameters["dataset_path"]
        self.__results_foldername = self.__parameters["results_foldername"]
        self.__algorithm = self.__parameters["algorithm"]

        return "settings loaded"

    def save_settings(self) -> str:
        """
        Saves the current settings to the file 'settings_data.json'
        and returns a message about the operation's success.
        """

        status = self.db.set("parameters", self.__parameters)
        if status:
            self.db.dump()
        return "settings saved" if status else "saving error"

    def generate_file(self) -> str:
        """
        Generates the file 'settings.conf' with the current configuration
        and saves in the specified path.
        """

        if not os.path.exists(self.file_path):
            return "ERROR! Settings file's path do not exist!"
        if self.__dataset_path == "":
            return "ERROR! No dataset selected!"

        try:
            settings_file = open(self.file_path, "w")
        except FileNotFoundError:
            return "ERROR! The settings file path was not founded!"

        # VER NO GUIA DA ENGINE SE ELA CONSEGUE IDENTIFICAR O SISTEMA OPERACIONAL
        if settings_file.writable():
            settings_str = [
                f"dataset.ratings.wins={self.__parameters['dataset_path']}\n",
                f"dataset.ratings.lins={self.__parameters['dataset_path']}\n",
                "dataset.social.wins=-1\n",
                "dataset.social.lins=-1\n",
                "# options: -columns: (user, item, [rating, [timestamp]]) columns of rating data; -threshold: to binary ratings;\n",
                "# --time-unit [DAYS, HOURS, MICROSECONDS, MILLISECONDS, MINUTES, NANOSECONDS, SECONDS]\n",
                "ratings.setup=-threshold -1 -datatransformation 1 -fullstat -1\n",
                "# recommender=usersplitting -traditional biasedmf -minlenu 2 -minleni 2\n",
                f"recommender={self.__algorithm}\n",
                "# main option: 1. test-set -f test-file-path; 2. cv (cross validation) -k k-folds [-p on, off]\n",
                "# 3. leave-one-out; 4. given-ratio -r ratio;\n",
                "# other options:  [--rand-seed n] [--test-view all] [--early-stop loss, MAE, RMSE]\n",
                "# evaluation.setup=cv -k 5 -p on --rand-seed 1 --test-view all --early-stop RMSE\n",
                "# evaluation.setup=given-ratio -r 0.8 -target r --test-view all --rand-seed 1\n",
                "# main option: is ranking prediction\n",
                "# other options: -ignore NumOfPopularItems\n",
                f"evaluation.setup=cv -k {self.__parameters['k_folds']} -p on --rand-seed {self.__parameters['random_seed']} --test-view all\n",
                f"item.ranking=on -topN {self.__parameters['topN']}\n",
                f"output.setup=-folder {self.__parameters['results_foldername']} -verbose on, off --to-file results_all.txt\n",
                "# Guava cache configuration\n",
                "guava.cache.spec=maximumSize=200,expireAfterAccess=2m\n",
                "########################### Model-based Methods ############################\n"
                f"num.factors={self.__parameters['num_factors']}\n",
                f"num.max.iter={self.__parameters['num_max_iterations']}\n",
                "# options: -bold-driver, -decay ratio, -moment value\n",
                f"learn.rate={self.__parameters['learning_rate']} -max -1 -bold-driver\n",
                f"reg.lambda={self.__parameters['reg_lambda']} -c 0.001\n",
                "#reg.lambda=10 -u 0.001 -i 0.001 -b 0.001 -s 0.001 -c 0.001\n",
                "# probabilistic graphic models\n",
                "pgm.setup=-alpha 2 -beta 0.5 -burn-in 300 -sample-lag 10 -interval 100\n",
                "########################### Memory-based Methods ##########################\n"
                "# similarity method: PCC, COS, COS-Binary, MSD, CPC, exJaccard; -1 to disable shrinking;\n",
                f"similarity={self.__parameters['similarity']}\n",
                "num.shrinkage=-1\n",
                "# neighborhood size; -1 to use as many as possible.\n",
                f"num.neighbors={self.__parameters['num_neighboors']}\n",
                "########################## Method-specific Settings ########################\n"
                "AoBPR=-lambda 0.3\n",
                "BUCM=-gamma 0.5\n",
                "BHfree=-k 10 -l 10 -gamma 0.2 -sigma 0.01\n",
                "FISM=-rho 100 -alpha 0.4\n",
                "Hybrid=-lambda 0.5\n",
                "LDCC=-ku 20 -kv 19 -au 1 -av 1 -beta 1\n",
                "PD=-sigma 2.5\n",
                "PRankD=-alpha 20\n",
                "RankALS=-sw on\n",
                "RSTE=-alpha 0.4\n",
                "DCR=-wt 0.9 -wd 0.4 -p 5 -lp 2.05 -lg 2.05\n",
                "DCW=-wt 0.9 -wd 0.4 -p 5 -lp 2.05 -lg 2.05 -th 0.8\n",
                "SPF=-i 0 -b 5 -th 0.9 -f 10 -t 100 -l 0.02 -r 0.001\n",
                "SLIM=-l1 1 -l2 1 -k 1\n",
                "CAMF_LCS=-f 10\n",
                "CSLIM_C=-lw1 1 -lw2 5 -lc1 1 -lc2 5 -k 3 -als 0\n",
                "CSLIM_CI=-lw1 1 -lw2 5 -lc1 1 -lc2 1 -k 1 -als 0\n",
                "CSLIM_CU=-lw1 1 -lw2 0 -lc1 1 -lc2 5 -k 10 -als 0\n",
                "CSLIM_CUCI=-lw1 1 -lw2 5 -lc1 1 -lc2 5 10 -1 -als 0\n",
                "GCSLIM_CC=-lw1 1 -lw2 5 -lc1 1 -lc2 5 -k -1 -als 0\n",
                "CSLIM_ICS=-lw1 1 -lw2 5 -k 1 -als 0\n",
                "CSLIM_LCS=-lw1 1 -lw2 5 -k 1 -als 0\n",
                "CSLIM_MCS=-lw1 -20000 -lw2 100 -k 3 -als 0\n",
                "GCSLIM_ICS=-lw1 1 -lw2 5 -k 10 -als 0\n",
                "GCSLIM_LCS=-lw1 1 -lw2 5 -k -1 -als 0\n",
                "GCSLIM_MCS=-lw1 1 -lw2 5 -k -1 -als 0\n",
                "FM=-lw 0.01 -lf 0.02\n"
            ]
            for i in range(len(settings_str)):
                settings_file.write(settings_str[i])

            settings_file.close()
            # print("#########")
            # print(f"File name: { os.path.basename(self.file_path) }")
            # print("#########")
            return "The settings file was generated!"
        else:
            return "ERROR! The file is not readable!"

    def __del__(self):
        """
        Saves the settings when the class is dealocated.
        """
        self.save_settings()
