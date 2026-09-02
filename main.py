import os
import asyncio
from telethon import TelegramClient

# Configurações básicas do seu bot
api_id = 26553805  # Seu API ID de ontem
api_hash = '8ec7d031bf3bb7904ba01e149ef7b629'  # Seu API Hash de ontem
phone = '+5574981222350'

client = TelegramClient('sessao_bot', api_id, api_hash)

async def main():
    # Novo comando automático que pede o código nos logs do Render
    await client.start(phone=phone)
    print("Bot conectado com sucesso!")
    
    # Aqui abaixo fica a automação de envio que estruturamos ontem
    while True:
        try:
            # Envia a mensagem para o grupo (coloque o link ou ID do seu grupo aqui)
            await client.send_message('NOME_DO_SEU_GRUPO', 'Sua mensagem automática aqui')
            print("Mensagem enviada!")
        except Exception as e:
            print(f"Erro ao enviar: {e}")
        
        # Espera 5 minutos (300 segundos) antes de mandar a próxima
        await asyncio.sleep(300)

with client:
    client.loop.run_until_complete(main())
  
