import os
from kivy.logger import Logger
from kivy.app import App
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
import firebase_admin
from firebase_admin import credentials, firestore

# Configuração do Kivy
Config.set('graphics', 'backend', 'auto')  # Ou 'gles2'

Logger.info("App: Inicializando o aplicativo")

# Verificar se o arquivo de credenciais Firebase existe
if not os.path.exists('projetofaculdade-c05bb-firebase-adminsdk-zm28v-16554f2ec7.json'):
    Logger.error("App: Arquivo de credenciais Firebase não encontrado")
else:
    try:
        Logger.info("App: Tentando inicializar Firebase")
        cred = credentials.Certificate('projetofaculdade-c05bb-firebase-adminsdk-zm28v-16554f2ec7.json')
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        Logger.info("App: Firebase inicializado com sucesso")
    except Exception as e:
        Logger.error(f"App: Erro ao inicializar Firebase - {e}")

# Inicialize o Firestore novamente de maneira explícita
try:
    db = firestore.client()
    Logger.info("App: Firestore cliente inicializado com sucesso")
except Exception as e:
    Logger.error(f"App: Erro ao inicializar Firestore - {e}")


class NavigationManager:
    def __init__(self, app):
        self.app = app
        self.stack = []  # Pilha de telas
        Logger.info("App: Gerenciador de navegação inicializado")

    def change_screen(self, new_screen):
        Logger.info(f"App: Tentando mudar para a nova tela {new_screen}")
        try:
            if self.app.main_layout.children:
                current_screen = self.app.main_layout.children[0]
                self.stack.append(current_screen)  # Empilha a tela atual antes de mudar
                self.app.main_layout.clear_widgets()

            self.app.main_layout.add_widget(new_screen)
            Logger.info(f"App: Tela {new_screen} carregada com sucesso")
        except Exception as e:
            Logger.error(f"App: Erro ao trocar a tela - {e}")

    def go_back(self):
        Logger.info("App: Voltando para a tela anterior")
        try:
            if self.stack:
                previous_screen = self.stack.pop()  # Desempilha a tela anterior
                self.app.main_layout.clear_widgets()
                self.app.main_layout.add_widget(previous_screen)
                Logger.info("App: Tela anterior carregada com sucesso")
            else:
                self.app.show_main_menu()  # Mostra o menu principal se não houver telas na pilha
                Logger.info("App: Mostrando o menu principal")
        except Exception as e:
            Logger.error(f"App: Erro ao voltar para a tela anterior - {e}")


class PescaCiaApp(App):
    def build(self):
        Logger.info("PescaCiaApp: Iniciando o aplicativo")
        self.main_layout = BoxLayout(orientation='vertical')
        self.navigation_manager = NavigationManager(self)
        self.show_main_menu()
        Logger.info("PescaCiaApp: Menu principal exibido")
        return self.main_layout

    def show_main_menu(self):
        Logger.info("App: Mostrando o menu principal")
        self.main_layout.clear_widgets()
        self.btn_pescar = Button(text='Pesquei um Peixe', size_hint=(1, 0.1))
        self.btn_pescar.bind(on_press=self.abrir_formulario_pesca)
        self.btn_vou_pescar = Button(text='Vou Pescar', size_hint=(1, 0.1))
        self.btn_vou_pescar.bind(on_press=self.abrir_local_pesca)
        self.main_layout.add_widget(self.btn_pescar)
        self.main_layout.add_widget(self.btn_vou_pescar)

    def abrir_formulario_pesca(self, instance):
        Logger.info("App: Abrindo formulário de pesca")
        self.navigation_manager.change_screen(FormularioPesca(self))

    def abrir_local_pesca(self, instance):
        Logger.info("App: Abrindo local de pesca")
        self.navigation_manager.change_screen(LocalPesca(self))


class FormularioPesca(BoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        Logger.info("App: Formulário de Pesca inicializado")
        self.app = app
        self.orientation = 'vertical'

        self.entries = {}
        labels = ["Espécie:", "Local:", "Peso:", "Forma de captura (isca, anzol etc...):"]

        for label in labels:
            lbl = Label(text=label, size_hint_y=None, height=30)
            self.add_widget(lbl)
            
            if label != "Forma de captura (isca, anzol etc...):":
                entry = TextInput(size_hint_y=None, height=30)
            else:
                entry = TextInput(size_hint_y=None, height=60, multiline=True)
            self.add_widget(entry)
            self.entries[label] = entry

        # Botões
        self.btn_voltar = Button(text="Voltar", size_hint_y=None, height=50)
        self.btn_voltar.bind(on_press=self.voltar_para_inicio)

        self.btn_salvar = Button(text="Salvar", size_hint_y=None, height=50)
        self.btn_salvar.bind(on_press=self.salvar)

        self.add_widget(self.btn_voltar)
        self.add_widget(self.btn_salvar)

    def voltar_para_inicio(self, instance):
        Logger.info("App: Voltando para o menu principal a partir do formulário")
        self.app.show_main_menu()

    def salvar(self, instance):
        Logger.info("App: Salvando informações de pesca")
        data = {label: entry.text.strip() for label, entry in list(self.entries.items())}
        if not all(data.values()):
            popup = Popup(title='Aviso', content=Label(text='Todos os campos devem ser preenchidos.'), size_hint=(0.8, 0.3))
            popup.open()
            return

        try:
            db.collection('pesca').add(data)
            Logger.info("App: Informações de pesca salvas com sucesso")
            popup = Popup(title='Sucesso', content=Label(text='Informações salvas com sucesso.'), size_hint=(0.8, 0.3))
            popup.open()
            self.voltar_para_inicio(instance)
        except Exception as e:
            Logger.error(f"App: Erro ao salvar informações de pesca - {e}")
            popup = Popup(title='Erro', content=Label(text=f'Ocorreu um erro ao salvar as informações: {e}'), size_hint=(0.8, 0.3))
            popup.open()


class LocalPesca(ScrollView):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app

        self.layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        self.load_buttons()
        self.add_widget(self.layout)

    def load_buttons(self):
        try:
            docs = db.collection('pesca').stream()
            for doc in docs:
                data = doc.to_dict()
                local = data.get('Local:', 'N/A')
                especie = data.get('Espécie:', 'N/A')
                peso = data.get('Peso:', 'N/A')

                peso_display = f"{peso} kg" if peso != 'N/A' else peso
                info_texto = f"{local} - {especie} - {peso_display}"

                button = Button(
                    text=info_texto,
                    size_hint=(1, None),
                    text_size=(None, None),
                    halign='center',
                    valign='middle',
                    padding=(10, 10)
                )
                button.bind(
                    size=self.adjust_button_text_size
                )
                button.bind(
                    on_press=lambda instance, data=data: self.app.navigation_manager.change_screen(RelatoPesca(self.app, data))
                )
                self.layout.add_widget(button)

            self.btn_voltar = Button(text="Voltar", size_hint_y=None, height=50)
            self.btn_voltar.bind(on_press=self.voltar_para_inicio)
            self.layout.add_widget(self.btn_voltar)

        except Exception as e:
            Logger.error(f"App: Erro ao carregar os dados de pesca - {e}")
            popup = Popup(title='Erro', content=Label(text=f'Ocorreu um erro ao carregar os dados: {e}'), size_hint=(0.8, 0.3))
            popup.open()

    def voltar_para_inicio(self, instance):
        self.app.show_main_menu()

    def adjust_button_text_size(self, instance, size):
        instance.text_size = (instance.width - 20, None)
        instance.height = max(50, instance.texture_size[1] + 20)


class RelatoPesca(BoxLayout):
    def __init__(self, app, data, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = 'vertical'

        for key, value in list(data.items()):
            if key == 'Peso:':
                value = f"{value} kg"
            button_text = f"{key}: {value}"

            button = Button(
                text=button_text,
                size_hint=(1, None),
                text_size=(None, None),
                halign='center',
                valign='middle',
                padding=(10, 10)
            )
            button.bind(
                size=self.adjust_button_text_size
            )
            button.bind(
                on_press=lambda instance, data=data: self.app.navigation_manager.change_screen(RelatoDetalhes(self.app, data))
            )
            self.add_widget(button)

        self.btn_voltar = Button(text="Voltar", size_hint_y=None, height=50)
        self.btn_voltar.bind(on_press=self.voltar_para_local_pesca)
        self.add_widget(self.btn_voltar)

    def adjust_button_text_size(self, instance, size):
        instance.text_size = (instance.width - 20, None)
        instance.height = max(50, instance.texture_size[1] + 20)

    def voltar_para_local_pesca(self, instance):
        self.app.navigation_manager.change_screen(LocalPesca(self.app))


class RelatoDetalhes(BoxLayout):
    def __init__(self, app, data, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = 'vertical'

        for key, value in list(data.items()):
            if key == 'Peso:':
                value = f"{value} kg"
            self.add_widget(Label(text=f"{key}: {value}", size_hint_y=None, height=30))

        self.btn_voltar = Button(text="Voltar", size_hint_y=None, height=50)
        self.btn_voltar.bind(on_press=self.voltar)
        self.add_widget(self.btn_voltar)

    def voltar(self, instance):
        self.app.navigation_manager.go_back()


if __name__ == "__main__":
    PescaCiaApp().run()
