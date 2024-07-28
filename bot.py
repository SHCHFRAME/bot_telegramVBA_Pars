import logging
from telegram import Update, Bot, BotCommand, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import asyncio
import nest_asyncio

# Настройка nest_asyncio
nest_asyncio.apply()

# Токен бота и ID канала
TOKEN = '7266577671:AAE9-rPYFHu9GX7lcgg27Cm0p_5DC6AB5sE'
CHANNEL_ID = '-1002104343087'

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)

# Функция для создания главного меню
def main_menu_keyboard():
    keyboard = [
        [KeyboardButton("🛠️ Заказать услугу")],
        [KeyboardButton("💳 Способы оплаты")],
        [KeyboardButton("🏢 О компании")],
        [KeyboardButton("📞 Контакты")],
        [KeyboardButton("📨 Отправить сообщение в канал")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Обработчик команды /start
async def start(update: Update, context: CallbackContext) -> None:
    logger.debug("Получена команда /start")
    await update.message.reply_text(
        '👋 Добро пожаловать в CodeAdvance! Мы предлагаем профессиональные услуги по программированию и разработке сайтов. Выберите нужную опцию:',
        reply_markup=main_menu_keyboard()
    )

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    logger.debug(f"Получено сообщение: {text}")

    if text == '🛠️ Заказать услугу':
        await update.message.reply_text("📞 Для заказа услуги напишите нам в Telegram: @tolkovba", reply_markup=main_menu_keyboard())
    elif text == '💳 Способы оплаты':
        await update.message.reply_text("💰 Мы принимаем оплату через криптокошелек USDT TRC20: TTMc4wp1LT4QddSRkojCNxXeL8Z5cPVLcY", reply_markup=main_menu_keyboard())
    elif text == '🏢 О компании':
        await update.message.reply_text("🔍 CodeAdvance – ведущая компания в области VBA программирования и веб-разработки. Мы гарантируем высокое качество услуг и индивидуальный подход к каждому клиенту.", reply_markup=main_menu_keyboard())
    elif text == '📞 Контакты':
        await update.message.reply_text("📬 Свяжитесь с нами: Email: support@codeadvance.com, Telegram: @tolkovba", reply_markup=main_menu_keyboard())
    elif text == '📨 Отправить сообщение в канал':
        await send_to_channel(update, context)

# Обработчик команды send_to_channel
async def send_to_channel(update: Update, context: CallbackContext) -> None:
    logger.debug("Обработка команды send_to_channel")
    try:
        message = "Привет, канал! 👋"
        await bot.send_message(chat_id=CHANNEL_ID, text=message)
        logger.info("Сообщение отправлено в канал")
        await update.message.reply_text("✅ Сообщение успешно отправлено в канал", reply_markup=main_menu_keyboard())
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения в канал: {e}")
        await update.message.reply_text(f"❌ Ошибка: {e}", reply_markup=main_menu_keyboard())

# Функция для установки команд бота
async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Запуск бота"),
        BotCommand(command="send_to_channel", description="Отправить сообщение в канал")
    ]
    await bot.set_my_commands(commands)

# Главная функция
async def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # Регистрация обработчиков команд и сообщений
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await set_bot_commands(application.bot)

    logger.info("Запуск бота...")
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
