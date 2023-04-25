import os
import logging
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    ApplicationBuilder,
)
from os.path import join, dirname
from dotenv import load_dotenv

from handlers import (
    add_message,
    start,
    help,
    stat,
    stat_user,
)

dotenv_path = join(dirname(__file__), '../.env')

load_dotenv(dotenv_path)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    token = os.getenv('TELEGRAM_TOKEN')
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('stat', stat))
    application.add_handler(CommandHandler('stat_user', stat_user))
    application.add_handler(MessageHandler(filters.TEXT, add_message))

    application.run_polling()


if __name__ == '__main__':
    main()
