import os
import logging
import telegram
import sqlite3
from telegram import Update, ParseMode
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater, CallbackContext

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def add_message(update, context):
    print('add_message called')
    logging.info('Received message from %s in chat %s: %s', update.message.from_user.username, update.message.chat_id, update.message.text)
    if update.message.text:
        conn = sqlite3.connect('messages.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      date TEXT, 
                      message TEXT, 
                      username TEXT)''')
        date = update.message.date
        message = update.message.text
        username = update.message.from_user.username

        cursor.execute("INSERT INTO messages (date, message, username) VALUES (?, ?, ?)",
                       (date, message, username))
        conn.commit()
        conn.close()

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Привет! Я бот канала КУЧА. Введите /help для получения списка команд.')

def help(update: Update, context: CallbackContext):
    update.message.reply_text('Список доступных команд:\n/help - выводит список команд\n/stat - выводит статистику по всему каналу\n/stat user - выводит статистику по конкретному пользователю')

def stat(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    members_count = context.bot.get_chat_members_count(chat_id)
    
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM messages")
    total_messages = cursor.fetchone()[0]
    conn.close()

    logger.info(f"Members count: {members_count}")
    logger.info(f"Total messages: {total_messages}")

    update.message.reply_text(f"Статистика всего канала.\nОбщее число участников канала: {members_count}\nКоличество сообщений в канале: {total_messages}")

def stat_user(update: Update, context: CallbackContext):
    # TODO: реализовать статистику по конкретному пользователю
    update.message.reply_text('Статистика по пользователю:')

def main():
    updater = Updater(os.getenv('TELEGRAM_TOKEN'), use_context=True)
    
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('stat', stat))
    updater.dispatcher.add_handler(CommandHandler('stat_user', stat_user))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, add_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()