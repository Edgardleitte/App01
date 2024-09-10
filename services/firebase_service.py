import firebase_admin
from firebase_admin import credentials, firestore
from kivy.logger import Logger

class FirebaseService:
    def __init__(self):
        Logger.info("FirebaseService: Inicializando conexão com o Firebase")
        try:
            cred = credentials.Certificate('projetofaculdade-c05bb-firebase-adminsdk-zm28v-16554f2ec7.json')
            firebase_admin.initialize_app(cred)
            self.db = firestore.client()
            Logger.info("FirebaseService: Firebase conectado com sucesso")
        except Exception as e:
            Logger.error(f"FirebaseService: Erro ao conectar ao Firebase - {e}")
            self.db = None

    def salvar_pesca(self, dados):
        Logger.info(f"FirebaseService: Salvando dados da pesca {dados}")
        try:
            if self.db:
                self.db.collection('pesca').add(dados)
                Logger.info("FirebaseService: Dados de pesca salvos com sucesso")
        except Exception as e:
            Logger.error(f"FirebaseService: Erro ao salvar dados no Firebase - {e}")

