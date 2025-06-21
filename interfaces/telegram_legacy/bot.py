import os
import openai
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Load environment variables from .env file
load_dotenv()

# Fetch the Telegram and OpenAI API tokens
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set up the OpenAI API key
openai.api_key = OPENAI_API_KEY

# Function to communicate with OpenAI's GPT-3
def chat_with_openai(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can use different models
        prompt=prompt,
        max_tokens=100,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Command handler for /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = """
    Hello! I am your friendly AI bot powered by OpenAI.
    Here are some commands you can use:
    /start - Start the bot and get a welcome message.
    /help - Get a list of commands.
    /about - Learn more about this bot.
    /reset - Reset the conversation.
    /stop - Stop the bot.
    """
    await update.message.reply_text(welcome_message)

# Command handler for /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_message = """
    Available Commands:
    /start - Start the bot.
    /help - Show this help message.
    /about - About this bot.
    /reset - Reset the conversation.
    /stop - Stop the bot.
    """
    await update.message.reply_text(help_message)

# Command handler for /about
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_message = """
    This bot uses OpenAI's GPT model to generate responses based on your messages.
    Created by [Your Name or Team].
    """
    await update.message.reply_text(about_message)

# Command handler for /reset
async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reset_message = "The conversation has been reset. Feel free to start a new chat."
    # Optionally, reset any stored data or states here
    await update.message.reply_text(reset_message)

# Command handler for /stop
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stop_message = "Bot stopped. Thank you for using the bot!"
    await update.message.reply_text(stop_message)
    await context.application.stop()

# Handler to respond to any user message
async def respond_to_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text  # Get the message from the user
    bot_response = chat_with_openai(user_message)  # Send the message to OpenAI
    await update.message.reply_text(bot_response)  # Send the response back to the user

# Main function to run the bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CommandHandler("stop", stop))

    # Add message handler to respond to any text message
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond_to_message))

    print("Bot is running...")
    app.run_polling()
