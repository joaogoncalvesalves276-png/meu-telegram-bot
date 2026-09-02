async def main():
    await client.connect()
    if not await client.is_user_authorized():
        # Deixamos sem o 'code' para forçar o Telegram a gerar e enviar um novo para você
        await client.send_code_request('+5574981222350')
        print("⚠️ Código solicitado! Verifique seu app do Telegram.")
        await asyncio.sleep(300) # Mantém o servidor esperando você pegar o código
    else:
        print("✅ Autenticação realizada com sucesso!")
        await executar_envios()
        
