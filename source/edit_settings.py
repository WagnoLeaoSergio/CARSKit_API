import os
import subprocess

class Settings_Editor(object):
    def __init__(self):
        self.__dataset_path = ""
        self.__result_path = ""
        self.__algorithm = ""
        self.__parameters = []
        # parametros ...

    # getters e setters para os parametos...

    def set_dataset_path(self, path: str) -> bool:
        # FACIL: Checar se o caminho existe
        self.__dataset_path = path
        return True
    def get_dataset_path(self) -> str:
        return self.__dataset_path

    def set_results_path(self, path: str) -> bool:
        # FACIL: Checar se o caminho existe
        self.__results_path = path
        return True
    def get_results_path(self) -> str:
        return self.__results_path

    def set_algorithm(self, algo: str) -> bool:
        # MEDIO: Checar se o algoritmo recebido exite
        self.__algorithm = algo
        return True
    def get_algorithm(self) -> str:
        return  self.__algorithm
    
    def set_parameters(self, params: list) -> bool:
        # DIFICIL: checar se os parametros passados 'fazem sentido'
        self.__parameters = params
        return True
    def get_parameters(self) -> list:
        return self.__parameters
    """
    def load_parameters(self):
        1 - Carregar os parametros de algum BD

        2 - Inserir os parametros nos atributos da classe

    def save_parameters(self):
        1 - inserir e alterar os parametros do BD

    def generate_file(self, path):
        1 - abrir um novo arquivo de configurações

        2 - Criar uma cópia do arquivo setting.conf 
            e substituir os espaços onde ficam os parametros

        3 - Escrever a cópia alterada no arquivo e
            salva-lo no caminho especificado

        4 - fechar o arquivo

    SALVAR OS PARAMETROS NO BD QUANDO A CLASSE FOR DESTRUÍDA!
    """