[app]
# Nome do aplicativo
title = PescaCiaApp

# Nome do pacote (único no dispositivo)
package.name = pescacia

# Domínio do pacote
package.domain = org.meuapp

# Versão do aplicativo
version = 1.02

# Diretório de origem do aplicativo
source.dir = .

# Orientação do aplicativo (retrato)
orientation = portrait

# Extensões de arquivo a serem incluídas no APK
source.include_exts = py,png,jpg,kv,atlas,json

# Extensões de arquivo a serem excluídas do APK
source.exclude_exts = spec

# Padrões de inclusão de arquivos (adicionar o arquivo .json explicitamente)
source.include_patterns = assets/*,images/*,*.py,projetofaculdade-c05bb-firebase-adminsdk-zm28v-16554f2ec7.json

# Padrões de exclusão de arquivos
source.exclude_patterns = tests/*,docs/*

# Bibliotecas e dependências Python necessárias para o aplicativo
requirements = python3,kivy==2.0.0,firebase_admin,google-auth==1.24.0

# Permissões necessárias para o aplicativo Android
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE

# Caminho para o Android SDK
android.sdk_path = /home/edgard/.buildozer/android/platform/android-sdk

# Caminho para o Android NDK
android.ndk_path = /home/edgard/.buildozer/android/platform/android-ndk-r25b

# Versão mínima do NDK API
android.ndk_api = 21

# Versão da API do Android a ser usada para construir
android.api = 31

# Versão do NDK recomendada
android.ndk_version = 25b

# Arquivo de ícone do aplicativo
icon.filename = %(source.dir)s/icon.png

# (Opcional) Arquivo de presplash (imagem de carregamento) do aplicativo
# presplash.filename = %(source.dir)s/presplash.png
