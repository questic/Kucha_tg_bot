import logging
from telegram import Update
from telegram.ext import (
    CallbackContext,
)

from models import Session, User, Message
from sqlalchemy import func


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def generate_text(update: Update, context: CallbackContext):):	
    input_text = update.message.text
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=input_text,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.5,
    )
    await context.bot.send_message(chat_id=update.message.chat_id, text=response.choices[0].text)

async def add_message(update: Update, context: CallbackContext):
    logging.info('Received message from %s in chat %s: %s', update.message.from_user.username, update.message.chat_id,
                 update.message.text)
    if update.message.text:
        message = update.message.text
        username = update.message.from_user.username

        session = Session()
        user = session.query(User).filter(User.username == username).first()
        if user is None:
            session.add(User(username=username))
            session.commit()
            user = session.query(User).filter(User.username == username).first()
        message = Message(user=user, message=message)
        session.add(message)
        session.commit()



async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        'Привет! Я бот канала КУЧА. Введите /help для получения списка команд.',
    )


async def help(update: Update, context: CallbackContext):
    await update.message.reply_text(
        'Список доступных команд:\n/help - выводит список команд\n/stat - выводит статистику по всему каналу\n/stat user - выводит статистику по конкретному пользователю')


async def stat(update: Update, context: CallbackContext):
    members_count = await update.message.chat.get_member_count()
    session = Session()
    total_messages = session.query(func.count(Message.id)).scalar()

    logger.info(f"Members count: {members_count}")
    logger.info(f"Total messages: {total_messages}")

    await update.message.reply_text(
        f"Статистика всего канала.\nОбщее число участников канала: {members_count}\nКоличество сообщений в канале: {total_messages}")


async def stat_user(update: Update, context: CallbackContext):
    username = update.message.text.split(' ')[-1]
    session = Session()
    user = session.query(User).filter(User.username == username).first()

    messages = user.messages
    message_count = len(messages)

    word_counts = {}
    for message in messages:
        words = message.message.split()
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1

    most_usage_word = max(word_counts, key=word_counts.get)

    await update.message.reply_text(
        f"Статистика по пользователю {username}\nКоличество сообщений: {message_count}\nСамое частое слово в сообщениях: {most_usage_word}")
