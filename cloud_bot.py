"""
Облачная часть бота — запускается на Railway
Умеет только включать ПК через Wake-on-LAN
"""

from wakeonlan import send_magic_packet
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os


BOT_TOKEN  = os.environ.get("BOT_TOKEN")
ALLOWED_ID = 1130287078
PC_MAC     = "58:11:22:A8:F7:6C"


def is_allowed(update: Update) -> bool:
    return update.effective_user.id == ALLOWED_ID


async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update): return
    await update.message.reply_text(
        "☁️ *Облачная часть бота*\n\n"
        "/wakeup — включить ПК\n\n"
        "Остальные команды доступны когда ПК включён.",
        parse_mode="Markdown"
    )


async def wakeup(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update): return
    try:
        send_magic_packet(PC_MAC)
        await update.message.reply_text(
            "✅ Magic packet отправлен!\n"
            "ПК включится через 5–15 секунд.\n\n"
            "После включения все команды бота заработают."
        )
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start",  start))
    app.add_handler(CommandHandler("wakeup", wakeup))
    print("Облачный бот запущен.")
    app.run_polling()


if __name__ == "__main__":
    main()
