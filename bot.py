import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

# Токен бота и ID канала
TOKEN = '7266577671:AAE9-rPYFHu9GX7lcgg27Cm0p_5DC6AB5sE'
CHANNEL_ID = '-1002104343087'

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)

# Обработчик команды /start
async def start(update: Update, context: CallbackContext) -> None:
    logger.debug("Получена команда /start")
    keyboard = [
        [InlineKeyboardButton("Заказы", callback_data='order')],
        [InlineKeyboardButton("Оплата", callback_data='payment')],
        [InlineKeyboardButton("О нас", callback_data='about')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Добро пожаловать в CodeAdvance! Выберите опцию:', reply_markup=reply_markup)

# Обработчик нажатий кнопок
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    choice = query.data
    logger.debug(f"Нажата кнопка: {choice}")

    if choice == 'order':
        await query.edit_message_text(text="Вы можете написать нам: @tolkovba")
    elif choice == 'payment':
        await query.edit_message_text(text="Наш криптокошелек для USDT TRC20: TTMc4wp1LT4QddSRkojCNxXeL8Z5cPVLcY")
    elif choice == 'about':
        await query.edit_message_text(text="Мы предоставляем комплексные услуги, включая VBA программирование и разработку сайтов. Обращайтесь к нам для качественного выполнения всех задач!")

# Обработчик команды send_to_channel
async def send_to_channel(update: Update, context: CallbackContext) -> None:
    logger.debug("Обработка команды send_to_channel")
    try:
        message = "Привет, канал!"
        await bot.send_message(chat_id=CHANNEL_ID, text=message)
        logger.info("Сообщение отправлено в канал")
        await update.message.reply_text("Сообщение отправлено в канал")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения в канал: {e}")
        await update.message.reply_text(f"Ошибка: {e}")

# Главная функция
def main() -> None:
    application = Application.builder().token(TOKEN).build()
    
    # Регистрация обработчиков команд
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler('send_to_channel', send_to_channel))

    logger.info("Запуск бота...")
    application.run_polling()

if __name__ == '__main__':
    main()
