import asyncio
import random
import os
import sys
import threading
from datetime import datetime
from collections import deque
from flask import Flask
from telethon import TelegramClient
import http.client
import json

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

CHAVE_GEMINI_REAL = "AQ.Ab8RN6Knq2WB13jkyaJC9sTSg_yJ9VGMQOi_G88WACvtqh_wKA"

client = TelegramClient('sessao_celular', API_ID, API_HASH)
historico_mensagens = deque(maxlen=100)

MENSAGENS = [
    "Fala pessoal, dia de muita execução por aqui.", "Acompanhando os insights da comunidade hoje.", 
    "Foco total nos objetivos comerciais desta semana.", "O mercado atual exige agilidade e adaptação.", 
    "Sempre bom ver novos pontos de vista por aqui.", "Excelente jornada de trabalho para todos.", 
    "Mantenham a consistência nas operações de hoje.", "Muito bom o nível técnico dos debates atuais.", 
    "Alguém de olho nas movimentações de agora?", "Resiliência e estratégia geram resultados reais.", 
    "Diferentes abordagens enriquecem muito o setor.", "Analisando o cenário econômico com bastante critério.", 
    "Mais um ciclo de metas para bater hoje.", "Tamo junto, ótima tarde produtiva para nós.", 
    "A execução correta supera qualquer teoria complexa.", "Quem aí está ativo nos projetos hoje?", 
    "A persistence vence o talento sem disciplina.", "Bora produzir que o mercado não espera.", 
    "Observando os comportamento do público com atenção.", "O segredo do crescimento é a constância diária.", 
    "Novos desafios geram as melhores inovações.", "Mantenham o ritmo e a mente focada hoje.", 
    "A tomada de decisão lógica evita prejuízos desnecessários.", "Operando com critérios claros neste dia.", 
    "Grandes projetos nascem de debates bem estruturados.", "O dia promete boas oportunidades de conexão.", 
    "Seguimos firmes no planejamento estratégico traçado.", "Ótimo momento para revisar nossas prioridades.", 
    "Trocar experiências reais fortalece todo o ecossistema.", "Fiquem atentos às pequenas mudanças de mercado.", 
    "A paciência comercial é uma virtude indispensável.", "Sempre buscando herdar os processos atuais.", 
    "Bons insights comerciais surgem com o estudo.", "Evoluindo a estratégia um passo por vez.", 
    "Foco e discernimento nas escolhas de mercado.", "Networking inteligente impulsiona resultados reais.", 
    "Cenário atual exige calma and análise precisa.", "Mantenham a dedicação nos objetivos principais.", 
    "Cada ação planejada gera valor no futuro.", "Firmeza nos propósitos comerciais da nossa semana.", 
    "A dedicação diária constrói autoridade de mercado.", "Parcerias de longo prazo geram lucros mútuos.", 
    "Estudar os movimentos do mercado com critério.", "Planejar ações minimiza riscos desnecessários.", 
    "Mentalidade madura lida melhor com as oscilações.", "Construindo bases sólidas para novos negócios.", 
    "Seguimos focados na produtividade comercial diária.", "Oportunidades reais exigem preparação antecipada.", 
    "A constância nos planos gera solidez financeira.", "Networking ativo transforma ideias em grandes negócios.", 
    "Foco total na execução perfeita das metas.", "Conhecimento prático aplicado transforma qualquer negócio.", 
    "Análise de dados ajuda nas decisões comerciais.", "Mantenham o foco e a energia alta.", 
    "Bons negócios começam com parcerias alinhadas.", "A resiliência comercial constrói grandes histórias.", 
    "Estudar o cenário antes de agir poupa tempo.", "Visão estratégica clara dita o nosso sucesso.", 
    "Mais uma jornada com foco em novos negócios.", "Crescimento sustentável exige paciência diária.", 
    "Acompanhando atentamente as novidades comerciais de hoje.", "Determinação comercial gera resultados acima da média.", 
    "Networking de valor acelera projetos de mercado.", "Manter o foco nas operações mais lucrativas.", 
    "Decisões baseadas em dados evitam prejuízos bobos.", "Seguimos firmes nos propósitos profissionais.", 
    "A evolução profissional exige estudo diário focado.", "Bons debates geram ideias de alto valor.", 
    "Gerenciar riscos é a chave do crescimento.", "Foco nas metas principais do nosso mercado.", 
    "A paciência comercial gera as melhores escolhas.", "Construindo o futuro com ações focadas hoje.", 
    "Mais um dia de aprendizado prático intenso.", "Networking qualificado gera negócios de longo prazo.", 
    "Estudar os gráficos com calma traz clareza.", "Visão de longo prazo protege nossos investimentos.", 
    "Trabalho consistente gera resultados incontestáveis.", "Mantenham a calma e a disciplina operacional.", 
    "Foco total no progresso contínuo dos negócios.", "Parcerias certas geram resultados surpreendentes.", 
    "Análise técnica detalhada ajuda a mitigar riscos.", "Bora focar no que realmente expande negócios.", 
    "A persistência comercial vence desafios complexos.", "Excelente dia para revisar processos e metas.", 
    "Networking ativo gera valor para toda comunidade.", "Seguimos focados nas trends de crescimento.", 
    "A inteligência estratégica muda o patamar comercial.", "Bons insights profissionais surgem com a constância.", 
    "Foco absoluto nas soluções mais eficientes.", "A dedicação diária pavimenta caminhos de sucesso.", 
    "Estudar os concorrentes e o mercado traz clareza.", "Gerenciamento correto garante a nossa longevidade profissional.", 
    "Cada dia produtivo conta na soma final.", "Parcerias fortes geram marcas fortes no mercado.", 
    "Visão clara e foco na execução diária."
]

async def gerar_frase_ia():
    try:
        contextos = [
            "mentalidade financeira avançada e sutil.",
            "psicologia aplicada à disciplina, foco e hábitos maduros.",
            "uma pergunta retórica de alto nível para gerar debates profissionais rápidos.",
            "visão estratégica de mercado, paciência comercial e tomada de decisão lógica."
        ]
        contexto_da_vez = random.choice(contextos)
        semente = random.randint(1, 9999)
        
        prompt_txt = (
            f"Gere uma frase curta inédita número {semente} sobre {contexto_da_vez} "
            "Regras fundamentais: Mínimo 4 palavras, máximo 12 palavras. Responda estritamente em português do Brasil. "
            "Proibido usar qualquer clichê, aspas, hashtags, emojis, links ou anúncios. Texto puro corrido."
        )

        conn = http.client.HTTPSConnection("generativelanguage.googleapis.com")
        payload = json.dumps({"contents": [{"parts": [{"text": prompt_txt}]}]})
        headers = {'Content-Type': 'application/json'}
        
        conn.request("POST", f"/v1beta/models/gemini-1.5-flash:generateContent?key={CHAVE_GEMINI_REAL}", payload, headers)
        res = conn.getcall() if hasattr(conn, 'getcall') else conn.getresponse()
        data = res.read().decode("utf-8")
        json_data = json.loads(data)
        
        # AJUSTE DA LEITURA DO ARRAYS COM ÍNDICES REAIS [0]
        if 'candidates' in json_data and len(json_data['candidates']) > 0:
            text = json_data['candidates'][0]['content']['parts'][0]['text'].strip().replace('"', '')
            palavras = len(text.split())
            if 3 <= palavras <= 15 and text not in historico_mensagens:
                return text
    except Exception as e:
        print(f"Modo de segurança acionado: {e}", file=sys.stderr)
    
    # Plano B Inteligente: Garante o envio imediato da lista sem travar o loop
    disponiveis = [f for f in MENSAGENS if f not in historico_mensagens]
    if not disponiveis:
        historico_mensagens.clear()
        disponiveis = MENSAGENS
    return random.choice(disponiveis)

async def executar_envios():
    print("🚀 Loop definitivo com chaves AQ e leitura corrigida de JSON ativo!")
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
            print(f"[{horario}] Enviada com sucesso: {frase_escolhida}")
        except Exception as e:
            print(f"⚠️ Falha técnica: {e}", file=sys.stderr)
            await asyncio.sleep(15)

async def main():
    async with client:
        print("✅ Conectado com sucesso usando a sessão estável!")
        await executar_envios()

if __name__ == '__main__':
    t_web = threading.Thread(target=run_web_server)
    t_web.daemon = True
    t_web.start()
    asyncio.run(main())
    
