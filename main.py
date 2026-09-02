import os
import asyncio
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

api_id = 26553805
api_hash = '8ec7d031bf3bb7904ba01e149ef7b629'
phone = '+5574981222350'

client = TelegramClient('sessao_bot', api_id, api_hash)

async def main():
    print("Iniciando pedido de código oficial...")
    # Comando oficial para forçar o envio por SMS caso não esteja logado em outro app
    result = await client.send_code_request(phone, force_sms=True)
    print("MENSAGEM ENVIADA! Verifique suas mensagens SMS no chip do celular.")

with client:
    client.loop.run_until_complete(main())
    
