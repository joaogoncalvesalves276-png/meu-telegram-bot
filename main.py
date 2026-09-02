import os
import asyncio
import threading
from flask import Flask
from telethon import TelegramClient

app = Flask('')
@app.route('/')
def home(): return "Bot vivo!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Seus dados oficiais e novos de agora
API_ID = 37153836
API_HASH = "b13ec4b1dbc5f9feee1a94a67940e2"
phone = '+5574981222350'

client = TelegramClient('sessao_celular', API_ID, API_HASH)

async def main():
    await client.connect()
    # Força o Telegram a mandar o código de 5 dígitos correto para o seu app
    await client.send_code_request(phone)
    print("CÓDIGO ENVIADO COM SUCESSO! VEJA SEU APLICATIVO DO TELEGRAM.")

if __name__ == '__main__':
    t_web = threading.Thread(target=run_web_server)
    t_web.daemon = True
    t_web.start()
    import nest_asyncio
    nest_asyncio.apply()
    client.loop.run_until_complete(main())
    
