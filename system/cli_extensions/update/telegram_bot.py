from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

class TelegramBot:
    def __init__(self, token, controller):
        self.app = ApplicationBuilder().token(token).build()
        self.controller = controller
        
        # Register handlers
        self.app.add_handler(CommandHandler("reset", self.handle_reset))
        
    async def handle_reset(self, update: Update, context):
        await self.controller.reset_memory("soft")
        await update.message.reply_text("♻️ Memory reset completed")
        
    def run(self):
        self.app.run_polling()