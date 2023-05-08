import os

class Config(object):
    # get a token from @BotFather
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "5651108082:AAFVgaHkjKM23fzDiQI30i7A2xEME2T3LD8")
    # The Telegram API things
    APP_ID = int(os.environ.get("API_ID", 2647779))
    API_HASH = os.environ.get("API_HASH","7ccea94fc3eed6cecaf37e08e512e09b")
