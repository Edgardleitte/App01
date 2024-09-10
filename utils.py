import os
from kivy.logger import Logger

def check_and_create_directories(directories):
    Logger.info("Utilitários: Verificando e criando diretórios se necessário")
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            Logger.info(f"Diretório criado: {directory}")
        else:
            Logger.info(f"Diretório já existe: {directory}")

