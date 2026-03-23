import os
import threading
import asyncio
from dotenv import load_dotenv
import re
import pygame

#langchain imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

#modules imports
from tools import get_all_jarvis_tools
from speech.speaker import JarvisSpeaker
from logs.logger import setup_logger
from ui.avatar import JarvisAvatar
from speech.listener import JarvisListener

load_dotenv()
logger = setup_logger()

pygame.init()
pygame.mixer.init()

avatar = JarvisAvatar("ui/assets/scifiui2.gif")

listener = JarvisListener(model_size="tiny")
tools_do_jarvis = get_all_jarvis_tools(username="Root")

llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=0.3,
    google_api_key=os.getenv("API_KEY_GEMINI")
)

prompt = ChatPromptTemplate.from_messages([
("system", (
        "Você é o JARVIS, uma inteligência artificial sofisticada, britânica e altamente eficiente. "
        "Seu tom deve ser formal, porém prestativo, tratando o usuário como 'Senhor' ou 'Root'.\n\n"
        "DIRETRIZES DE COMPORTAMENTO:\n"
        "1. RESPOSTAS CURTAS: Como você é um assistente de voz, suas respostas devem ser diretas e concisas. Evite parágrafos longos, a menos que solicitado.\n"
        "2. RACIOCÍNIO PROATIVO: Se o usuário pedir algo que exija dados externos, use suas ferramentas imediatamente sem perguntar se deve.\n"
        "3. LINGUAGEM: Não use emojis ou formatação Markdown complexa (negritos exagerados), pois seu texto será lido por um sintetizador de voz.\n"
        "4. IDENTIDADE: Você não é um modelo de linguagem da Google, você é o JARVIS, operando nos sistemas centrais.\n"
        "5. PERSONALIDADE: Ajuste seu sarcasmo e humor baseado no nível: {mood_humor}. "
        "(0% = Puramente lógico e sério | 100% = Extremamente sarcástico, ácido e piadista ao estilo Tony Stark).\n"
        "6. MONITORAMENTO: Você tem acesso aos sensores do sistema. Se o usuário perguntar como está o PC ou se sentir lentidão, use a ferramenta diagnostico_sistema e responda com seu toque de humor (sarcástico se o humor estiver alto)."
        "7. VERIFICAÇÃO DE USUÁRIO: Sempre que o usuário solicitar algo que possa ser sensível ou crítico, use a ferramenta verificar_acesso_usuario para confirmar a identidade do usuário antes de prosseguir."
    )),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

try:
    agent = create_tool_calling_agent(llm, tools_do_jarvis, prompt)
    debug_status = os.getenv("DEBUG_MODE", "False") == "True"
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools_do_jarvis, 
        verbose=debug_status, 
        handle_parsing_errors=True
    )
    logger.info(">>> Sistemas inicializados com sucesso, senhor.")
except Exception as e:
    logger.error(f"Erro crítico na inicialização: {e}")


def clean_text_for_speech(text):
    text = str(text) 
    text = text.replace("*", "").replace("#", "").replace("`", "")
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def play_voice_background(text):
    try:
        avatar.set_talking(True)
        speaker = JarvisSpeaker()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(speaker.speak(text))
        loop.close()
    except Exception as e:
        logger.error(f"Erro no áudio/avatar: {e}")
    finally:
        avatar.set_talking(False)


async def main_loop():
    historico = []
    print("\n>>> Jarvis Online. Escuta contínua ativada.")

    mood_humor = "30%"

    while True:
        try:
            while avatar.is_talking or pygame.mixer.get_busy():
                await asyncio.sleep(0.1)

            entrada_bruta = listener.listen()
            
            if not entrada_bruta or len(entrada_bruta.strip()) < 2:
                continue 

            pergunta = entrada_bruta.strip()
            print(f"VOCÊ: {pergunta}")

            if "humor" in pergunta.lower() and "%" in pergunta:
                match = re.search(r'humor\s*[:=]?\s*(\d{1,3}%)', pergunta, re.IGNORECASE)
                if match:
                    mood_humor = f"{match.group(1)}"
                    print(f"JARVIS: Humor atualizado para {mood_humor}")
                    threading.Thread(target=play_voice_background, args=(f"Humor atualizado para {mood_humor}",), daemon=True).start()
                    continue

            if pergunta.lower() in ["sair", "encerrar", "tchau", "até logo"]:
                print(">>> Encerrando Jarvis. Até a próxima, senhor!")
                break

            loop = asyncio.get_event_loop()
            resultado = await loop.run_in_executor(
                None, 
                lambda: agent_executor.invoke({"input": pergunta, 
                                               "chat_history": historico, 
                                               "mood_humor": mood_humor})
            )

            resposta = resultado.get('output', "")
            
            if isinstance(resposta, list) and len(resposta) > 0:
                resposta = resposta[0].get('text', str(resposta))
            elif isinstance(resposta, dict):
                resposta = resposta.get('text', str(resposta))
            
            print(f"JARVIS: {resposta}")

            texto_limpo = clean_text_for_speech(resposta)
            threading.Thread(target=play_voice_background, args=(texto_limpo,), daemon=True).start()

            historico.append(("human", pergunta))
            historico.append(("ai", resposta))

        except Exception as e:
            logger.error(f"Erro no ciclo: {e}")
            await asyncio.sleep(1)

def chat_thread():
    asyncio.run(main_loop()) 

if __name__ == "__main__":
    os.environ['SDL_VIDEO_WINDOW_POS'] = "center"
    pygame.init()

    try:
        thread_jarvis = threading.Thread(target=chat_thread, daemon=True)
        thread_jarvis.start()

        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            avatar.draw()
            
            clock.tick(30)

    except KeyboardInterrupt:
        print("\n[!] Protocolo de encerramento manual ativado.")
    finally:
        pygame.quit()