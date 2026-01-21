"""
Configuration module for loading and validating environment variables.
"""
import os
from pathlib import Path
from dotenv import load_dotenv


def load_config():
    """Loads environment variables from the .env file."""
    env_path = Path(__file__).parent.parent.parent / ".env"

    if not env_path.exists():
        raise FileNotFoundError(
            f"Arquivo de ambiente não encontrado em {env_path}\n"
            "Por favor, crie um arquivo .env baseado no .env.example:\n"
            "  cp .env.example .env\n"
            "Depois adicione sua chave da API da Anthropic no arquivo .env."
        )

    load_dotenv(env_path)


# Load configuration on module import
load_config()

# Get and validate ANTHROPIC_API_KEY
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY or ANTHROPIC_API_KEY == "your_api_key_here":
    raise ValueError(
        "ANTHROPIC_API_KEY não está configurada ou ainda está usando o valor placeholder.\n"
        "Por favor, configure sua chave da API da Anthropic no arquivo .env.\n"
        "Obtenha sua chave da API em: https://console.anthropic.com/"
    )

# Get LOG_LEVEL with default value
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Validate LOG_LEVEL
VALID_LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
if LOG_LEVEL not in VALID_LOG_LEVELS:
    raise ValueError(
        f"LOG_LEVEL inválido: {LOG_LEVEL}\n"
        f"Deve ser um dos seguintes: {', '.join(VALID_LOG_LEVELS)}"
    )
