from telegram import Update, ForceReply, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
import os
from dotenv import load_dotenv

load_dotenv()

SAMPLE, PHOTO, MENU = range(3)


def create_keyboard():
    custom_keyboard = [['Показать шаблон', 'Загрузить фото']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True)
    return reply_markup


def start(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Привет {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )
    update.message.reply_text('''Выберите действие:''',
                              reply_markup=create_keyboard())
    return MENU


def handle_sample_request(update: Update, context: CallbackContext) -> int:
    user_reply = update.message.text
    if user_reply == 'Показать шаблон':
        context.bot.send_photo(chat_id=update.message.chat_id, photo=open(
            'templates/sample.jpg', 'rb'), reply_markup=create_keyboard())
    return MENU  # После показа шаблона вернемся в меню


def handle_upload_photo(update: Update, context: CallbackContext) -> int:
    try:
        if update.message.photo:
            file_id = update.message.photo[-1].file_id
            file = context.bot.get_file(file_id)

            # Задайте путь для сохранения фотографии
            file_path = 'images/uploaded_photo.jpg'
            file.download(file_path)

            context.bot.send_message(
                chat_id=update.message.chat_id,
                text="Фотография успешно загружена и сохранена.",
                reply_markup=create_keyboard()
            )
        else:
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text="Вы не отправили фотографию. Возвращаемся в меню.",
                reply_markup=create_keyboard()
            )
    except Exception as e:
        # Запишите ошибку в лог
        # logging.error(f"Ошибка при обработке фотографии: {str(e)}")
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Произошла ошибка при обработке фотографии. Попробуйте еще раз.",
            reply_markup=create_keyboard()
        )
    return MENU


def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Приятно было провести с тобой время, увидимся в следующий раз!', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main():
    token = os.getenv('TG_API_TOKEN')
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: [
                MessageHandler(Filters.regex('Показать шаблон'),
                               handle_sample_request),
                MessageHandler(Filters.photo, handle_upload_photo),
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
