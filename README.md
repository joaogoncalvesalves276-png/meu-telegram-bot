# 🤖 Robô de Envios Automáticos com IA (100% pelo Celular)

Este é um projeto pronto para criar um **Userbot do Telegram** integrado com a **Inteligência Artificial do Gemini (Google)**. O robô roda de forma 100% gratuita direto na nuvem (servidor) e envia mensagens inéditas e criativas em grupos ou tópicos de 3 em 3 minutos, simulando uma conta real, funcionando no piloto automático por mais de 1 ano!

---

## 🚀 Como Clonar e Ter o Seu Próprio Bot (Passo a Passo)

Você fará toda a configuração usando apenas o navegador e o aplicativo do seu celular. Siga atentamente as 4 etapas abaixo:

### 1️⃣ Clonar este Projeto
1. Crie uma conta gratuita no site [GitHub.com](https://github.com).
2. Entre no link deste repositório e clique no botão **Fork** (Clonar) no topo da página. Isso criará uma cópia exata deste código na sua conta do GitHub instantaneamente.

### 2️⃣ Pegar suas Chaves Oficiais (Telegram e Google)
Você precisará de 3 chaves de segurança da sua própria conta:
* **API ID e API HASH (Telegram):** Acesse o site oficial [my.telegram.org](https://telegram.org), coloque seu número com `+55`, copie o código enviado no seu aplicativo do Telegram e clique em **API development tools**. Guarde os números do `App api_id` e `App api_hash`.
* **Chave do Gemini (IA da Google):** Acesse o site [aistudio.google.com](https://google.com), faça login com seu Gmail, clique no menu lateral (3 risquinhos ☰) -> ícone da **chavezinha 🔑** -> **Create API Key** -> **Create API Key in new project**. Copie a chave longa que começa com `AIzaSy`.

### 3️⃣ Criar o arquivo de Sessão Permanente no Celular
Como os servidores de hospedagem reiniciam constantemente, precisamos gerar um arquivo de autorização fixa para o bot não ficar pedindo código por SMS toda hora:
1. Baixe o aplicativo **Termux** na loja de apps **F-Droid** (A versão da Google Play Store está abandonada e com erro de internet, use o F-Droid!).
2. Abra o Termux (tela preta) e instale o Python colando este comando completo e dando Enter:
   ```bash
   pkg update -y && pkg install python -y && pip install telethon
   ```
3. Crie o gerador colando este comando completo e dando Enter:
   ```bash
   cat << 'EOF' > login.py
   import asyncio
   from telethon import TelegramClient
   API_ID = SEU_API_ID_AQUI
   API_HASH = "SEU_API_HASH_AQUI"
   phone = "+55..." # Seu número com DDD
   client = TelegramClient('sessao_celular', API_ID, API_HASH)
   async def main():
       await client.start(phone=phone)
       print("LOGADO COM SUCESSO!")
   with client:
       client.loop.run_until_complete(main())
   EOF
   ```
   *(Substitua os dados de exemplo do comando acima pelas suas chaves reais obtidas na Etapa 2 antes de dar Enter).*
4. Rode o script digitando: `python login.py`. O Termux pedirá seu número de telefone e o código de 5 dígitos que chegará no chat oficial do seu Telegram. Digite-os na tela.
5. Quando aparecer "LOGADO COM SUCESSO!", libere o acesso aos arquivos digitando `termux-setup-storage` (clique em permitir na tela) e envie o arquivo para a sua pasta de Downloads com o comando:
   ```bash
   cp sessao_celular.session /sdcard/Download/
   ```
6. Vá no seu **GitHub**, clique em **Add file** -> **Upload files**, entre na pasta de Downloads do seu celular e envie o arquivo `sessao_celular.session` para o seu repositório.

### 4️⃣ Atualizar o arquivo `main.py` e Hospedar no Render
1. No seu GitHub, abra o arquivo `main.py`, clique no **lápis** para editar e cole o código completo mudando os valores de `API_ID`, `API_HASH`, `CHAVE_GEMINI_REAL`, `LINK_DO_GRUPO` e `ID_DO_TOPICO` para os dados reais do grupo onde o bot vai postar. Salve clicando em **Commit changes...**.
2. Crie uma conta gratuita no site [Render.com](https://render.com) conectando o seu GitHub.
3. Clique em **New +** -> **Background Worker**.
4. Selecione o repositório do seu bot do Telegram, mude a região para a mais próxima e clique em **Deploy**.
5. Pronto! O servidor vai ler o arquivo de sessão, conectar direto na rede e colocar a IA do Gemini para gerar textos exclusivos a cada 3 minutos no grupo de destino!
6. 
