# 🎤 Assistente de Voz com ChatGPT

Um assistente simples de terminal que permite conversar com ChatGPT usando voz, arquivos de áudio ou texto.

## ✨ Funcionalidades

- 🎤 **Gravação por microfone** - Fale diretamente
- 📁 **Upload de arquivos** - Processe áudios existentes
- ✏️ **Entrada de texto** - Alternativa sem microfone
- 🧠 **Reconhecimento de fala** - Usando Whisper
- 💬 **Integração ChatGPT** - Respostas inteligentes
- 🔊 **Síntese de voz** - Respostas em áudio

## 📋 Pré-requisitos

- Windows 10/11
- Python 3.8 - 3.12
- Microfone (opcional)
- Chave da API OpenAI

## 🚀 Instalação Rápida

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/assistente-voz-chatgpt.git
cd assistente-voz-chatgpt

# 2. Instale as dependências
pip install -r requirements.txt
pip install pipwin
pipwin install pyaudio

# 3. Instale o FFmpeg (OBRIGATÓRIO)
# Baixe de: https://www.gyan.dev/ffmpeg/builds/
# Extraia para C:\ffmpeg
# Adicione C:\ffmpeg\bin ao PATH do sistema

# 4. Execute o programa
python assistente.py
