import os
import logging
import openai
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    ApplicationBuilder,
)
from os.path import (
    join,
    dirname,
)
from dotenv import load_dotenv

from handlers import (
    add_message,
    start,
    help,
    stat,
    stat_user,
    generate_text,
)

dotenv_path = join(dirname(__file__), '../.env')

load_dotenv(dotenv_path)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    openai_key = os.getenv('OPENAI_KEY')
    openai.api_key = openai_key
    application = ApplicationBuilder().token(telegram_token).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('stat', stat))
    application.add_handler(CommandHandler('stat_user', stat_user))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.Regex('^Куча'), add_message))
    application.add_handler(MessageHandler(filters.Regex('^Куча, подскажи*'), generate_text))
    application.run_polling()


if __name__ == '__main__':
    main()
