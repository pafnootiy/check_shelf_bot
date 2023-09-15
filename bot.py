import os
import logging


from dotenv import load_dotenv
from telegram import Update, ForceReply, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler


from check_shelf import CheckShelf


SAMPLE, PHOTO, MENU = range(3)


def create_keyboard():
    custom_keyboard = [['Показать шаблон', 'Проверить товар']]
    reply_markup = ReplyKeyboardMarkup(
        custom_keyboard, resize_keyboard=True, one_time_keyboard=True)
    return reply_markup


def start(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуйте, {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )
    response_text = '''Для загрузки шаблона нажмите кнопку -- *Показать шаблон*
                       Для загрузки фотографии - просто отправьте ее в бот
                       Для сверки с шаблоном нажмите кнопку -- *Проверить товар*'''

    formatted_response = '\n'.join(
        line.strip() for line in response_text.split('\n'))

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=formatted_response,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=create_keyboard())

    return MENU


def handle_sample_request(update: Update, context: CallbackContext) -> int:
    user_reply = update.message.text
    if user_reply == 'Показать шаблон':
        context.bot.send_photo(chat_id=update.message.chat_id, photo=open(
            'templates/sample.jpg', 'rb'), reply_markup=create_keyboard())
    return MENU


def handle_upload_photo(update: Update, context: CallbackContext) -> int:
    try:
        if update.message.photo:
            file_id = update.message.photo[-1].file_id
            file = context.bot.get_file(file_id)
            file_path = 'images/uploaded_photo.jpg'
            file.download(file_path)

            response_text = '''Фотография успешно загружена и сохранена.
            Для сверки с шаблоном нажмите кнопку -- Проверить товар'''

            formatted_response = '\n'.join(
                line.strip() for line in response_text.split('\n'))
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text=formatted_response,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=create_keyboard()
            )

        else:
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text="Вы не отправили фотографию. Возвращаемся в меню.",
                reply_markup=create_keyboard()
            )
    except Exception as e:
        logging.error(f"Ошибка при обработке фотографии: {str(e)}")
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Произошла ошибка при обработке фотографии. Попробуйте еще раз.",
            reply_markup=create_keyboard()
        )

    return MENU


def handle_check_shelf(update: Update, context: CallbackContext) -> int:

    user_reply = update.message.text
    if user_reply == 'Проверить товар':
        shelf_image_path = "images/uploaded_photo.jpg"
        template_path = "templates/sample.jpg"
        bot = CheckShelf(shelf_image_path, template_path)
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=bot.load_and_compare_images(),
            reply_markup=create_keyboard()
        )

    return MENU


def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'До свидания!', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main():
    load_dotenv()
    token = os.getenv('TG_API_TOKEN')

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: [
                MessageHandler(Filters.regex('Показать шаблон'),
                               handle_sample_request),
                MessageHandler(Filters.photo, handle_upload_photo),
                MessageHandler(Filters.regex('Проверить товар'),
                               handle_check_shelf),
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
