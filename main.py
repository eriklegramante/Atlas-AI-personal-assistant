import asyncio
import sys
from config.settings import settings
from config.logger import logger
from src.database.brain_database import AtlasBrain
from src.brain.agent_graph import AtlasBrainGraph
from src.speech.listener import AtlasListener
from src.speech.speaker import AtlasSpeaker


async def core_loop():
    logger.info("=== ATLAS OPERATING SYSTEM STARTED ===")

    try:
        brain_db = AtlasBrain()
        await brain_db.initialize_db()

        listener = AtlasListener()
        speaker = AtlasSpeaker()
        graph = AtlasBrainGraph()

        session_id = "main_terminal_root"

        logger.info("All central systems initialized and stable. Ready to listen.")
        await speaker.speak("Systems initialized, sir. Awaiting instructions.")

    except Exception as e:
        logger.critical(f"Catastrophic system startup failure: {e}", exc_info=True)
        sys.exit(1)

    while True:
        try:
            print("\n" + "=" * 50)
            print(">>> ATLAS is listening... (Speak now)")
            print("=" * 50 + "\n")

            user_input = listener.listen(duration=4)

            if not user_input or len(user_input.strip()) == 0:
                await asyncio.sleep(0.5)
                continue

            # Internationalized local shutdown command triggers
            if any(
                cmd in user_input.lower()
                for cmd in ["shutdown system", "terminate atlas", "sleep atlas", "power off"]
            ):
                logger.warning("Shutdown protocol ordered by the operator.")
                await speaker.speak(
                    "Terminating local operations and saving logs. Goodbye, Root."
                )
                break

            chat_history = await brain_db.get_chat_history(
                session_id=session_id, limit=10
            )

            response_text = await graph.execute(
                user_input=user_input, history_raw=chat_history, humor="30%"
            )

            if response_text:
                await brain_db.add_message(
                    role="human", content=user_input, session_id=session_id
                )
                await brain_db.add_message(
                    role="ai", content=response_text, session_id=session_id
                )

                await speaker.speak(response_text)

            await asyncio.sleep(0.5)

        except KeyboardInterrupt:
            logger.warning("Manual interruption detected (Ctrl+C). Saving state and exiting.")
            break
        except Exception as e:
            logger.error(f"Unexpected error within execution loop: {e}", exc_info=True)
            await asyncio.sleep(2)


if __name__ == "__main__":
    try:
        asyncio.run(core_loop())
    except KeyboardInterrupt:
        print("\n[ATLAS] Operation aborted by user.")