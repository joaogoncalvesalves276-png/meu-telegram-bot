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

MENSAGENS = [
    "Bom dia pessoal, como estão as coisas por aqui?", "Acompanhando o grupo por aqui hoje.", 
    "Bons negócios para todo mundo hoje.", "O mercado brasileiro exige bastante atenção.", 
    "Sempre bom ver o grupo movimentado.", "Desejo uma excelente semana para todos.", 
    "Seguimos focados nas melhores oportunidades.", "Muito bom o nível das conversas aqui.", 
    "Alguém acompanhando as novidades de agora?", "Foco e paciência trazem ótimos resultados.", 
    "Interessante ver as diferentes opiniões aqui.", "Estou analisar o cenário atual com calma.", 
    "Mais um dia de muito aprendizado.", "Tamo junto pessoal, excelente tarde.", 
    "O planejamento faz toda a diferença.", "Quem aí está ativo hoje no mercado?", 
    "A constância supera qualquer obstacle por aqui.", "Bora para cima que a semana promete.", 
    "Observando os movimentos com bastante critério.", "O secret é manter a disciplina sempre.", 
    "Novos horizontes trazem excelentes resultados profissionais.", "Mantenham a energia alta durante o dia.", 
    "A análise técnica ajuda muito nas decisões.", "Quem está operando com foco hoje?", 
    "Grandes ideias surgem de debates inteligentes.", "O dia promete ótimas movimentações comerciais.", 
    "Seguimos firmes nos propósitos desta semana.", "Excelente oportunidade para rever nossas metas.", 
    "Compartilhar conhecimento fortalece toda a comunidade.", "Fiquem atentos aos detalhes do mercado.", 
    "Paciência é a virtude dos grandes negociadores.", "Sempre focado em evoluir um pouco mais.", 
    "Bons insights surgindo nas conversas recentes.", "Cada passo importa na construção do sucesso.", 
    "Vamos focar no que realmente gera valor.", "Determinação diária transforma qualquer reality difícil.", 
    "Dia produtivo para todos nós por aqui.", "Acompanhando atentamente as tendências de hoje.", 
    "Informação de qualidade faz total diferença.", "União e networking geram resultados incríveis.", 
    "Gerenciamento de risco é fundamental para todos.", "Mentalidade vencedora faz a diferença nos negócios.", 
    "Mais uma jornada de trabalho and foco.", "Estudar o cenário antes de agir evita erros.", 
    "Parcerias estratégicas aceleram nosso crescimento profissional.", "O success recompensa quem tem disciplina diária.", 
    "Foco nas soluções e não nos problemas.", "Troca de experiências enriquece muito o grupo.", 
    "Construindo o futuro com ações consistentes hoje.", "Fique atento às mudanças rápidas do mercado.", 
    "Ótimo momento para aprender algo totalmente novo.", "Trabalhar com inteligência traz melhores resultados sempre.", 
    "A persistence vence qualquer dificuldade temporária.", "Olho aberto nas oportunidades que surgem agora.", 
    "Fazer o simples com excelência traz resultados.", "Grupo muito qualificado e focado em evoluir.", 
    "Estratégia bem definida evita perdas desnecessárias.", "Bora produzir e gerar valor para todos.", 
    "O knowledge liberta e gera novas chances.", "Analisando os gráficos com muita paciência hoje.", 
    "Passo a passo chegaremos aos nossos objetivos.", "Atitude positiva muda nossa perspectiva de negócios.", 
    "Planejar o dia otimiza muito nosso tempo.", "Discussões construtivas elevam o nível do grupo.", 
    "Sempre buscando aprender com os erros passados.", "O sucesso exige dedicação em tempo integral.", 
    "Mantenham o foco no gerenciamento de vocês.", "Ótimas reflexões compartilhadas por aqui hoje.", 
    "Resultados sólidos demandam tempo e resiliência.", "Acompanhando de perto as principais movimentações financeiras.", 
    "Networking de alto nível se faz por aqui.", "Vamos aproveitar cada minuto do dia de hoje.", 
    "Disciplina supera o talento na maioria das vezes.", "Sempre focado nos planos de longo prazo.", 
    "Muito aprendizado prático nas conversas deste grupo.", "Execução precisa vale mais que planejamento perfeito.", 
    "Estudar sempre para não ficar para trás.", "Determinação é o combustível para nossos sonhos.", 
    "Análise fria do mercado evita decisões por impulso.", "Seguimos avançando com consistência e inteligência.", 
    "Bons negócios dependem de muita atenção diária.", "Oportunidades batem à porta de quem trabalha.", 
    "Gerenciar o tempo é gerenciar o próprio sucesso.", "Foco total na produtividade do dia de hoje.", 
    "Excelente dia para fechar novas parcerias.", "Conhecimento prático aplicado gera resultados imediatos.", 
    "Mantenham a calma nas oscilações do mercado.", "Visão de longo prazo evita ansiedade boba.", 
    "Trabalho duro em silêncio gera barulho nos resultados.", "Aprender com a experiência alheia economiza tempo.", 
    "Bora focar no progresso constante todos os dias.", "Mercado dinâmico exige atualização profissional constante.", 
    "Análise precisa faz toda a diferença nos investimentos.", "Foco, força e fé nos nossos objetivos.", 
    "Mais um dia para fazer acontecer de verdade.", "Comunidade focada in negócios e crescimento mútuo.", 
    "A inteligência financeira muda o jogo de qualquer um.", "Estudar as tendências nos coloca à frente sempre.", 
    "Resiliência para enfrentar os dias de mercado parado.", "Grandes resultados começam com pequenas escolhas diárias."
]

genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "AlzasyD-TEST_KEY_GENERATED_BY_AGENT"))
model = genai.GenerativeModel('gemini-pro')
client = TelegramClient('sessao_celular', API_ID, API_HASH)

historico_mensagens = deque(maxlen=150)

async def gerar_frase_ia():
    try:
        prompt = (
            "Create a highly creative, unique short message for a professional group. "
            "Vary the style entirely: it can be a quick market insight, a sharp psychological tip on discipline, "
            "a question to engage the group, or an intense motivational thought. "
            "Rules: Min 3, max 10 words. No emojis, no hashtags, no links, no ads. Just the pure text sentence."
        )
        response = model.generate_content(prompt)
        text = response.text.strip().replace('"', '')
        palavras = len(text.split())
        
        if 3 <= palavras <= 10 and text not in historico_mensagens:
            return text
    except Exception as e:
        print(f"Erro ao gerar frase na IA: {e}", file=sys.stderr)
    
    disponiveis = [f for f in MENSAGENS if f not in historico_mensagens]
    if not disponiveis:
        historico_mensagens.clear()
        disponiveis = MENSAGENS
    return random.choice(disponiveis)

async def executar_envios():
    print("🚀 Loop iniciado!")
    while True:
        try:
            frase_escolhida = await gerar_frase_ia()
            await client.send_message(LINK_DO_GRUPO, frase_escolhida, reply_to=ID_DO_TOPICO)
            historico_mensagens.append(frase_escolhida)
            horario = datetime.now().strftime('%H:%M:%S')
            print(f"[{horario}] Enviada: {frase_escolhida}")
        except Exception as e:
            print(f"⚠️ Erro: {e}", file=sys.stderr)
            await asyncio.sleep(15)
            continue
        await asyncio.sleep(TEMPO_ESPERA_SEGUNDOS)

async def main():
    await client.connect()
    if not await client.is_user_authorized():
        # Autenticação direta com seus dados reais de acesso
        await client.sign_in(phone='+5574981222350', code='43077')
    print("✅ Autenticação realizada com sucesso!")
    await executar_envios()

if __name__ == '__main__':
    t_web = threading.Thread(target=run_web_server)
    t_web.daemon = True
    t_web.start()
    import nest_asyncio
    nest_asyncio.apply()
    client.loop.run_until_complete(main())
