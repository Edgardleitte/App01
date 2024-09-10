from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.logger import Logger

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        Logger.info("MainScreen: Tela principal inicializada")
        
        layout = BoxLayout(orientation='vertical')
        
        btn_pescar = Button(text='Pesquei um Peixe', size_hint=(1, 0.2))
        btn_pescar.bind(on_press=self.on_pescar)
        layout.add_widget(btn_pescar)

        btn_local = Button(text='Vou Pescar', size_hint=(1, 0.2))
        btn_local.bind(on_press=self.on_local_pesca)
        layout.add_widget(btn_local)

        self.add_widget(layout)

    def on_pescar(self, instance):
        Logger.info("MainScreen: Navegando para formulário de pesca")
        self.manager.current = 'formulario'

    def on_local_pesca(self, instance):
        Logger.info("MainScreen: Navegando para local de pesca")
        self.manager.current = 'localpesca'

