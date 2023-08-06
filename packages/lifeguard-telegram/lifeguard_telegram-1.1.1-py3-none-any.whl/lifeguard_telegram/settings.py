"""
Lifeguard Telegram Settings
"""
from lifeguard.settings import SettingsManager

SETTINGS_MANAGER = SettingsManager(
    {
        "LIFEGUARD_TELEGRAM_VALIDATIONS_HANDLER_ENABLED": {
            "default": "true",
            "type": "boolean",
            "description": "Enable telegram validations handler",
        },
        "LIFEGUARD_TELEGRAM_ENABLE_BOTS_LOADER": {
            "default": "true",
            "type": "bool",
            "description": "Enable bots loader",
        },
        "TELEGRAM_API_KEY": {
            "default": "",
            "description": "Telegram bot token",
        },
        "TELEGRAM_DEFAULT_CHAT_ID": {
            "default": "",
            "description": "Telegram default chat id",
        },
    }
)

LIFEGUARD_TELEGRAM_VALIDATIONS_HANDLER_ENABLED = SETTINGS_MANAGER.read_value(
    "LIFEGUARD_TELEGRAM_VALIDATIONS_HANDLER_ENABLED"
)
LIFEGUARD_TELEGRAM_ENABLE_BOTS_LOADER = SETTINGS_MANAGER.read_value(
    "LIFEGUARD_TELEGRAM_ENABLE_BOTS_LOADER"
)
TELEGRAM_API_KEY = SETTINGS_MANAGER.read_value("TELEGRAM_API_KEY")
TELEGRAM_DEFAULT_CHAT_ID = SETTINGS_MANAGER.read_value("TELEGRAM_DEFAULT_CHAT_ID")
