from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.logger import Logger

class FormularioPescaScreen(Screen):
    def __init__(self, **kwargs):
        super(FormularioPescaScreen, self).__init__(**kwargs)
        Logger.info("FormularioPescaScreen: Tela de formulário inicializada")
        
        layout = BoxLayout(orientation='vertical')

        # Campos do formulário
        self.especie = TextInput(hint_text='Espécie', size_hint=(1, 0.2))
        self.local = TextInput(hint_text='Local', size_hint=(1, 0.2))
        self.peso = TextInput(hint_text='Peso', size_hint=(1, 0.2))

        layout.add_widget(self.especie)
        layout.add_widget(self.local)
        layout.add_widget(self.peso)

        # Botões
        btn_salvar = Button(text='Salvar', size_hint=(1, 0.2))
        btn_salvar.bind(on_press=self.salvar_dados)
        layout.add_widget(btn_salvar)

        btn_voltar = Button(text='Voltar', size_hint=(1, 0.2))
        btn_voltar.bind(on_press=self.voltar)
        layout.add_widget(btn_voltar)

        self.add_widget(layout)

    def salvar_dados(self, instance):
        Logger.info(f"FormularioPescaScreen: Salvando dados da pesca - Espécie: {self.especie.text}, Local: {self.local.text}, Peso: {self.peso.text}")
        # Aqui você pode adicionar a lógica de salvar os dados no Firebase ou em um banco de dados local.

    def voltar(self, instance):
        Logger.info("FormularioPescaScreen: Voltando para o menu principal")
        self.manager.current = 'main'

