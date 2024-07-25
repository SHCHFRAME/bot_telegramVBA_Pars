import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

# Новый токен бота
TOKEN = '7266577671:AAE9-rPYFHu9GX7lcgg27Cm0p_5DC6AB5sE'
# Замените CHANNEL_ID на ваш новый канал, если требуется
CHANNEL_ID = '-1002104343087'  # Пример ID канала

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)

async def start(update: Update, context: CallbackContext) -> None:
    logger.debug("Получена команда /start")
    keyboard = [
        [InlineKeyboardButton("Заказы", callback_data='order')],
        [InlineKeyboardButton("Оплата", callback_data='payment')],
        [InlineKeyboardButton("О нас", callback_data='about')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Добро пожаловать в CodeAdvance! Выберите опцию:', reply_markup=reply_markup)

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

async def send_to_channel(update: Update, context: CallbackContext) -> None:
    message = "Привет, канал!"
    await bot.send_message(chat_id=CHANNEL_ID, text=message)
    await update.message.reply_text("Сообщение отправлено в канал")

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler('send_to_channel', send_to_channel))

    # Запуск бота
    logger.info("Запуск бота...")
    application.run_polling()

if __name__ == '__main__':
    main()
