"""
LLM client module for initializing the Claude AI model.
"""
from langchain_anthropic import ChatAnthropic
from src.utils.config import ANTHROPIC_API_KEY
from src.utils.logger import logger


def get_llm(
    model: str = "claude-sonnet-4-20250514",
    temperature: float = 0.0,
    max_tokens: int = 4096,
) -> ChatAnthropic:
    """
    Initializes and returns an instance of the Claude AI model.

    Args:
        model: Model name to use (default: claude-sonnet-4-20250514)
        temperature: Temperature for response randomness (0.0 - 1.0).
                    Value 0 ensures more consistent and deterministic responses.
        max_tokens: Maximum tokens in the response

    Returns:
        Configured ChatAnthropic instance

    Raises:
        ValueError: If the API key is not configured correctly

    Examples:
        >>> llm = get_llm()
        >>> llm = get_llm(temperature=0.7)
        >>> llm = get_llm(model="claude-sonnet-4-20250514", temperature=0.0)
    """
    # Validate if API key is configured
    if not ANTHROPIC_API_KEY:
        raise ValueError(
            "ANTHROPIC_API_KEY não está configurada. "
            "Por favor, configure sua chave da API no arquivo .env"
        )

    logger.info(f"Inicializando modelo Claude AI: {model}")
    logger.info(f"Configurações - Temperature: {temperature}, Max tokens: {max_tokens}")

    try:
        llm = ChatAnthropic(
            model=model,
            anthropic_api_key=ANTHROPIC_API_KEY,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        logger.info("Cliente LLM inicializado com sucesso")
        return llm

    except Exception as e:
        logger.error(f"Erro ao inicializar cliente LLM: {str(e)}")
        raise
