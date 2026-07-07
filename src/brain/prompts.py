from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from config.settings import settings
from config.logger import logger


def get_atlas_prompt() -> ChatPromptTemplate:
    """Generates and compiles the ATLAS central prompt template orchestration block.

    Assembles structural configurations, injection hooks for historical data timelines,
    and real-time user inputs into a unified prompt tracking schema optimized for the
    LangGraph state graph engine.

    Args:
        None

    Returns:
        ChatPromptTemplate: A compiled prompt framework object ready for pipeline inference.

    Raises:
        KeyError: If the system configurations prompt template references missing parameter tags.
    """
    logger.debug("Building a ChatPromptTemplate for the central agent.")

    return ChatPromptTemplate.from_messages(
        [
            ("system", settings.SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )
