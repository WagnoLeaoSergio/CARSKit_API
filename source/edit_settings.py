import os
import subprocess
import pickledb

class Settings_Editor(object):
    def __init__(self, file_path="./CARSKit/setting.conf"):
        self.file_path = file_path
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
        

    """

    def generate_file(self, path):
        1 - abrir um novo arquivo de configurações

        2 - Criar uma cópia do arquivo setting.conf 
            e substituir os espaços onde ficam os parametros

        3 - Escrever a cópia alterada no arquivo e
            salva-lo no caminho especificado

        4 - fechar o arquivo

    SALVAR OS PARAMETROS NO BD QUANDO A CLASSE FOR DESTRUÍDA!
    """