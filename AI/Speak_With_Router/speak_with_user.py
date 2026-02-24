import os
from openai import OpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("AI Bot is ready 🤖 Ask me anything.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    await update.message.reply_text("Thinking...")

    try:
        response = client.responses.create(
            model="gpt-5-mini",
            input=user_text
        )

        answer = response.output_text
    except Exception as e:
        answer = f"Error: {e}"

    # Telegram limit ~4096 chars
    if len(answer) > 3800:
        answer = answer[:3800] + "\n\n(Trimmed)"

    await update.message.reply_text(answer)

def main():
    if not TELEGRAM_BOT_TOKEN:
        raise SystemExit("Set TELEGRAM_BOT_TOKEN first.")
    if not OPENAI_API_KEY:
        raise SystemExit("Set OPENAI_API_KEY first.")

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("AI Telegram Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()