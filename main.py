import os
import asyncio
from telethon import TelegramClient

api_id = 26553805
api_hash = '8ec7d031bf3bb7904ba01e149ef7b629'
phone = '+5574981222350'

client = TelegramClient('sessao_bot', api_id, api_hash)

async def main():
    # Isso vai forçar o Telegram a enviar o código para o seu app agora
    await client.send_code_request(phone)
    print("CÓDIGO ENVIADO! DEVE CHEGAR NO SEU TELEGRAM EM SEGUNDOS.")

with client:
    client.loop.run_until_complete(main())
    
