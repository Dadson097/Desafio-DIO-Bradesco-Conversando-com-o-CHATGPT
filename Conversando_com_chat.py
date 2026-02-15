import os
import whisper
import pyaudio
import wave
import tempfile
from openai import OpenAI
from gtts import gTTS

# Interface do Chat
print("="*60)
print("🎤 ASSISTENTE DE VOZ COM CHATGPT")
print("="*60)
print("\n🔑 Configure sua chave da OpenAI para começar")
print("(Obtenha em: https://platform.openai.com/api-keys)")
print("-"*60)

# Adicione sua API_KEY
API_KEY = input("Cole sua chave OpenAI (começa com sk-): ").strip()

if not API_KEY.startswith('sk-'):
    print("\n❌ Chave inválida! Deve começar com 'sk-'")
    print("🔄 Execute o programa novamente com uma chave válida")
    exit()

try:
    cliente = OpenAI(api_key=API_KEY)
    cliente.models.list()
    print("✅ Chave configurada com sucesso!\n")
except Exception as e:
    print(f"\n❌ Erro na chave: {e}")
    print("🔄 Verifique sua chave e tente novamente")
    exit()

def gravar_audio(duracao=3):
    """Grava áudio do microfone"""
    try:
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000,
                       input=True, frames_per_buffer=1024)
        print(f"🎤 Gravando {duracao}s... Fale agora!")
        frames = [stream.read(1024) for _ in range(int(16000/1024*duracao))]
        stream.stop_stream(); stream.close(); p.terminate()
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            wf = wave.open(f.name, 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(16000)
            wf.writeframes(b''.join(frames))
            wf.close()
            return f.name
    except Exception as e:
        print(f"❌ Erro na gravação: {e}")
        return None

def transcrever_com_whisper(arquivo):
    """Usa Whisper para transcrever áudio"""
    try:
        print("🧠 Carregando Whisper...")
        modelo = whisper.load_model("base")
        print("📝 Transcrevendo...")
        resultado = modelo.transcribe(arquivo, language='pt', fp16=False)
        return resultado['text'].strip()
    except Exception as e:
        print(f"❌ Erro no Whisper: {e}")
        return None

def perguntar_chatgpt(pergunta):
    """Pergunta ao ChatGPT"""
    try:
        print("🤔 Pensando...")
        resposta = cliente.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente útil em português."},
                {"role": "user", "content": pergunta}
            ],
            max_tokens=300
        )
        return resposta.choices[0].message.content
    except Exception as e:
        return f"❌ Erro no ChatGPT: {e}"

def falar(texto):
    """Converte texto em voz"""
    try:
        tts = gTTS(texto, lang='pt-br')
        arquivo = "resposta.mp3"
        tts.save(arquivo)
        print(f"🔊 Áudio salvo: {arquivo}")
        os.system(f'start {arquivo}')
    except Exception as e:
        print(f"❌ Erro no áudio: {e}")

def processar_audio(caminho):
    """Processa arquivo de áudio"""
    if not os.path.exists(caminho):
        return None, "❌ Arquivo não encontrado"
    texto = transcrever_com_whisper(caminho)
    return texto, None

# PROGRAMA PRINCIPAL
while True:
    print("\n" + "="*60)
    print("MENU PRINCIPAL")
    print("="*60)
    print("1. 🎤 Gravar e perguntar (microfone)")
    print("2. 📁 Usar arquivo de áudio")
    print("3. ✏️  Digitar texto")
    print("4. 🚪 Sair")
    print("-"*60)
    
    op = input("Opção: ").strip()
    
    if op == "4":
        print("\n👋 Até logo!")
        break
    
    # Opção 1: Microfone
    if op == "1":
        arquivo = gravar_audio(3)
        if not arquivo:
            continue
        pergunta = transcrever_com_whisper(arquivo)
        os.unlink(arquivo)
    
    # Opção 2: Arquivo de áudio
    elif op == "2":
        caminho = input("Caminho do arquivo: ").strip().strip('"').strip("'")
        pergunta, erro = processar_audio(caminho)
        if erro:
            print(erro)
            continue
    
    # Opção 3: Digitar texto
    elif op == "3":
        pergunta = input("Digite sua pergunta: ").strip()
        if not pergunta:
            print("❌ Pergunta vazia")
            continue
    
    # Caminho direto
    elif os.path.exists(op):
        pergunta, erro = processar_audio(op)
        if erro:
            print(erro)
            continue
    
    else:
        print("❌ Opção inválida")
        continue
    
    # Processando pergunta
    if pergunta:
        print(f"\n📝 Você: {pergunta}")
        resposta = perguntar_chatgpt(pergunta)
        print(f"\n💬 Assistente: {resposta}")
        
        if not resposta.startswith("❌"):
            falar(resposta)
    
    input("\n⏎ Enter para continuar...")