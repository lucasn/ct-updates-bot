from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, \
    CommandHandler, CallbackContext
from database import Database
from scrapping import retrieve_news
import config


def main() -> None:
    application = ApplicationBuilder().token(config.TOKEN).build()

    database = Database()
    application.bot_data['database'] = database

    start_hander = CommandHandler('start', start)
    remove_handler = CommandHandler('remove', remove)

    application.job_queue.run_repeating(check_updates, interval=60)
    application.add_handler(start_hander)
    application.add_handler(remove_handler)

    application.run_polling()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    database = context.bot_data['database']
    database.register_chat_if_is_not_registered(chat_id)

    await context.bot.send_message(
        chat_id=chat_id,
        text='Usuário registrado com sucesso. Você receberá atualizações a partir de agora.\n\nEnvie <b>\\remove</b> para se descadastrar',
        parse_mode='HTML'
    )


async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    database = context.bot_data['database']
    database.remove_chat(chat_id)

    await context.bot.send_message(
        chat_id=chat_id,
        text='Usuário removido com sucesso. Caso deseje receber atualizações novamente, envie <b>\start</b>.',
        parse_mode='HTML'
    )


async def check_updates(context: CallbackContext) -> None:
    database = context.bot_data['database']
    news = await retrieve_news()
    for entry in news:
        if not database.check_news_entry(entry['url']):
            message = f"<b>{entry['title']}</b>\n\nData de publicação: {entry['publish_date']}\n\nLink: {entry['url']}"

            chats = database.retrieve_all_chats()
            for chat in chats:
                await context.bot.send_message(
                    chat_id=chat[0],
                    text=message,
                    parse_mode='HTML'
                )
            database.insert_news_entry(entry['title'], entry['url'])

if __name__ == '__main__':
    main()