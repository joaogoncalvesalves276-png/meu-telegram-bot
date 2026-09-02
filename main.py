import asyncio
import random
import os
import sys
import threading
from datetime import datetime
from collections import deque
from flask import Flask
from telethon import TelegramClient
import google.generativeai as genai

app = Flask('')

@app.route('/')
def home():
    return "Bot vivo!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

API_ID = 37153836
API_HASH = "b13ec4b1dbc5f9feee1a94a67940e2"
LINK_DO_GRUPO = "interlinkIDchat"
ID_DO_TOPICO = 37433
TEMPO_ESPERA_SEGUNDOS = 180

# Sua chave oficial gerada no Google AI Studio aplicada com sucesso
CHAVE_GEMINI_REAL = "AQ.Ab8RN6IKiWjQjT0pgl5YfMQn1yLaFRWcQz9_O8KnqErlooYFPg"

genai.configure(api_key=CHAVE_GEMINI_REAL)
model = genai.GenerativeModel('gemini-pro')

client = TelegramClient('sessao_celular', API_ID, API_HASH)
historico_mensagens = deque(maxlen=200)

MENSAGENS_RESERVA = [
    "Bom dia pessoal, focados nas melhores oportunidades hoje.",
    "A constância supera qualquer obstáculo por aqui.",
    "Bora para cima que a semana promete muita produtividade.",
    "O segredo é manter a disciplina e o gerenciamento sempre.",
    "Excelente dia para fechar novas parcerias e conexões."
]

async def gerar_frase_ia():
    try:
        estilos = [
            "um insight rápido sobre mentalidade de negócios de forma sutil.",
            "uma dica madura sobre disciplina, consistência e rotina profissional.",
            "uma pergunta curta e inteligente para fazer as pessoas pensarem e interagirem no grupo.",
            "um pensamento direto focado em superação e foco no longo prazo, sem clichês."
        ]
        estilo_da_vez = random.choice(estilos)
        
        prompt = (
            f"Escreva de forma totalmente inédita e autoral {estilo_da_vez} "
            "Regras: Mínimo 4 palavras, máximo 12 palavras. Responda apenas em português do Brasil. "
            "Não use NENHUM emoji, nenhuma hashtag, links ou aspas. Apenas o texto puro."
        )
        response = model.generate_content(prompt)
        text = response.text.strip().replace('"', '')
        palavras = len(text.split())
        
        if 3 <= palavras <= 15 and text not in historico_mensagens:
            return text
    except Exception as e:
        print(f"Erro na IA (usando frase de segurança): {e}", file=sys.stderr)
    
    return random.choice(MENSAGENS_RESERVA)

async def executar_envios():
    print("🚀 Loop de envios com IA ativado!")
    primeiro_envio = True
    
    while True:
        try:
            if not primeiro_envio:
                await asyncio.sleep(TEMPO_ESPERA_SEGUNDOS)
            
            primeiro_envio = False
            frase_escolhida = await gerar_frase_ia()
            
            await client.send_message(LINK_DO_GRUPO, frase_escolhida, reply_to=ID_DO_TOPICO)
            historico_mensagens.append(frase_escolhida)
            
            horario = datetime.now().strftime('%H:%M:%S')
            print(f"[{horario}] Enviada: {frase_escolhida}")
        except Exception as e:
            print(f"⚠️ Erro no envio: {e}", file=sys.stderr)
            await asyncio.sleep(15)

async def main():
    # CORREÇÃO DO TIMEOUT: Inicialização envelopada em gerenciador assíncrono oficial
    async with client:
        print("✅ Conectado com sucesso usando a sessão permanente!")
        await executar_envios()

if __name__ == '__main__':
    t_web = threading.Thread(target=run_web_server)
    t_web.daemon = True
    t_web.start()
    
    # Executa o loop principal corrigido
    asyncio.run(main())
    
