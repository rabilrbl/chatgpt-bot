import os, asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram_assistant.handlers import start, help_command, handle_message, newchat_command, init_chatgpt

def start_bot():
    loop = asyncio.get_event_loop()
    asyncio.run_coroutine_threadsafe(init_chatgpt(), loop)
    app = Application.builder().token(os.getenv("BOT_TOKEN")).build()
    
    # Commands
    app.add_handlers(handlers=[
        # Commands
        CommandHandler("start", start),
        CommandHandler("help", help_command),
        CommandHandler("new", newchat_command),
        
        # Messages
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    ])
    
    # Run the bot until the user presses Ctrl-C
    app.run_polling(allowed_updates=Update.ALL_TYPES)