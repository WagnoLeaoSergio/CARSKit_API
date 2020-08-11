import os
import subprocess
import pickledb

class Settings_Editor(object):
    def __init__(self, file_path="\\CARSKit\\setting.conf"):
        current_path = os.path.abspath(os.getcwd())
        self.file_path =  current_path + file_path
        self.__dataset_path = ""
        self.__result_path = ""
        self.__algorithm = ""
        self.__parameters = []
        self.db = pickledb.load("./settings_data.db", True)
        # parametros ...

    # getters e setters para os parametos...

    def set_dataset_path(self, path: str) -> bool:
        # FACIL: Checar se o caminho existe
        if not os.path.exists(path):
            return False
        self.__dataset_path = path
        return True

    def get_dataset_path(self) -> str:
        return self.__dataset_path

    def set_results_path(self, path: str) -> bool:
        # FACIL: Checar se o caminho existe
        if not os.path.exists(path):
            return False
        self.__results_path = path
        return True

    def get_results_path(self) -> str:
        return self.__results_path

    def set_algorithm(self, algo: str) -> bool:
        # MEDIO: Checar se o algoritmo recebido existe
        self.__algorithm = algo
        return True
    def get_algorithm(self) -> str:
        return  self.__algorithm
    
    def set_parameters(self, params: list) -> bool:
        # DIFICIL: validar os parametros
        self.__parameters = params
        return True
    def get_parameters(self) -> list:
        return self.__parameters

    def load_settings(self) -> bool:
        # 1 - Carregar os parametros de algum BD
        if not self.db.get("initialized"):
            self.db.set("dataset_path", self.__dataset_path)
            self.db.set("result_path", self.__result_path)
            self.db.set("algorithm", self.__algorithm)
            self.db.set("parameters", self.__parameters)
            self.db.set("initialized", True)
            return False
        
        self.__dataset_path = self.db.get("dataset_path")
        self.__result_path = self.db.get("result_path")
        self.__algorithm = self.db.get("algorithm")
        self.__parameters = self.db.get("parameters")
        return True

    def save_settings(self) -> bool:
        status = True
        status = status and self.db.set("dataset_path", self.__dataset_path)
        status = status and self.db.set("result_path", self.__result_path)
        status = status and self.db.set("algorithm", self.__algorithm)
        status = status and self.db.set("parameters", self.__parameters)
        status = status and self.db.dump()
        return status
        

    def generate_file(self) -> bool:
        settings_file = open(self.file_path, "x")
        if settings_file:
            settings_str = f"""
            dataset.ratings.wins=C:\\Users\\Waguinho\\Documents\\pesquisa\\CARSKit_Interface\\source\\datasets\\ratings.txt
            # dataset.ratings.lins=/users/yzheng/desktop/data/restaurant/ratings.txt

            dataset.social.wins=-1
            dataset.social.lins=-1

            # options: -columns: (user, item, [rating, [timestamp]]) columns of rating data; -threshold: to binary ratings;
            # --time-unit [DAYS, HOURS, MICROSECONDS, MILLISECONDS, MINUTES, NANOSECONDS, SECONDS]

            ratings.setup=-threshold -1 -datatransformation 1 -fullstat -1

            # recommender=usersplitting -traditional biasedmf -minlenu 2 -minleni 2

            recommender={self.__algorithm or "camf_cu"}

            # main option: 1. test-set -f test-file-path; 2. cv (cross validation) -k k-folds [-p on, off]
            # 3. leave-one-out; 4. given-ratio -r ratio;
            # other options:  [--rand-seed n] [--test-view all] [--early-stop loss, MAE, RMSE]
            # evaluation.setup=cv -k 5 -p on --rand-seed 1 --test-view all --early-stop RMSE
            # evaluation.setup=given-ratio -r 0.8 -target r --test-view all --rand-seed 1
            # main option: is ranking prediction
            # other options: -ignore NumOfPopularItems

            evaluation.setup=cv -k 5 -p on --rand-seed 1 --test-view all
            item.ranking=on -topN 10

            output.setup=-folder results -verbose on, off --to-file results_all.txt

            # Guava cache configuration
            guava.cache.spec=maximumSize=200,expireAfterAccess=2m

            num.factors=10
            num.max.iter=100

            # options: -bold-driver, -decay ratio, -moment value
            learn.rate=2e-2 -max -1 -bold-driver

            reg.lambda=0.0001 -c 0.001
            #reg.lambda=10 -u 0.001 -i 0.001 -b 0.001 -s 0.001 -c 0.001
            # probabilistic graphic models
            pgm.setup=-alpha 2 -beta 0.5 -burn-in 300 -sample-lag 10 -interval 100

            # similarity method: PCC, COS, COS-Binary, MSD, CPC, exJaccard; -1 to disable shrinking;
            similarity=pcc
            num.shrinkage=-1

            # neighborhood size; -1 to use as many as possible.
            num.neighbors=10

            AoBPR=-lambda 0.3
            BUCM=-gamma 0.5
            BHfree=-k 10 -l 10 -gamma 0.2 -sigma 0.01
            FISM=-rho 100 -alpha 0.4
            Hybrid=-lambda 0.5
            LDCC=-ku 20 -kv 19 -au 1 -av 1 -beta 1
            PD=-sigma 2.5
            PRankD=-alpha 20
            RankALS=-sw on
            RSTE=-alpha 0.4
            DCR=-wt 0.9 -wd 0.4 -p 5 -lp 2.05 -lg 2.05
            DCW=-wt 0.9 -wd 0.4 -p 5 -lp 2.05 -lg 2.05 -th 0.8
            SPF=-i 0 -b 5 -th 0.9 -f 10 -t 100 -l 0.02 -r 0.001
            SLIM=-l1 1 -l2 1 -k 1
            CAMF_LCS=-f 10
            CSLIM_C=-lw1 1 -lw2 5 -lc1 1 -lc2 5 -k 3 -als 0
            CSLIM_CI=-lw1 1 -lw2 5 -lc1 1 -lc2 1 -k 1 -als 0
            CSLIM_CU=-lw1 1 -lw2 0 -lc1 1 -lc2 5 -k 10 -als 0
            CSLIM_CUCI=-lw1 1 -lw2 5 -lc1 1 -lc2 5 10 -1 -als 0
            GCSLIM_CC=-lw1 1 -lw2 5 -lc1 1 -lc2 5 -k -1 -als 0
            CSLIM_ICS=-lw1 1 -lw2 5 -k 1 -als 0
            CSLIM_LCS=-lw1 1 -lw2 5 -k 1 -als 0
            CSLIM_MCS=-lw1 -20000 -lw2 100 -k 3 -als 0
            GCSLIM_ICS=-lw1 1 -lw2 5 -k 10 -als 0
            GCSLIM_LCS=-lw1 1 -lw2 5 -k -1 -als 0
            GCSLIM_MCS=-lw1 1 -lw2 5 -k -1 -als 0
            FM=-lw 0.01 -lf 0.02
            """

            settings_file.w
        return False
        #1 - abrir um novo arquivo de configurações

        #2 - Criar uma cópia do arquivo setting.conf 
            e substituir os espaços onde ficam os parametros

        #3 - Escrever a cópia alterada no arquivo e
            salva-lo no caminho especificado

        #4 - fechar o arquivo

    # SALVAR OS PARAMETROS NO BD QUANDO A CLASSE FOR DESTRUÍDA!