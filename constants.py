from pathlib import Path

CONFIG_PATH = Path(__file__).parent / 'config'
CONFIG_PATH.mkdir(exist_ok=True)
MESSAGES_PATH = Path(__file__).parent / 'messages'
MESSAGES_PATH.mkdir(exist_ok=True)

CACHES = {}
API_KEY_FILE = 'chave'

# SESSION_STATES
MESSAGES = 'messages'
ACTUAL_CHAT = 'actual_chat'
GPT_MODEL = 'gpt_model'
GPT_API_KEY = 'gpt_api_key'