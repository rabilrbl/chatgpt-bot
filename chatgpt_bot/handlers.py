import asyncio
import typing as ty
from telegram import Update
from telegram.ext import (
    ContextTypes,
)
from telegram.error import NetworkError, BadRequest
from telegram.constants import ChatAction, ParseMode
from chatgpt_bot.chatgpt import chatgpt, generate_response
from chatgpt_bot.html_format import format_message

CHATGPT = None

async def init_chatgpt() -> None:
    global CHATGPT
    CHATGPT = await chatgpt()

def new_chat(context: ContextTypes.DEFAULT_TYPE) -> None:
    context.chat_data["conversation"] = CHATGPT.create_new_conversation()


async def start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}!\n\nStart sending messages with me to generate a response.\n\nSend /new to start a new chat session.",
        # reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
Basic commands:
/start - Start the bot
/help - Get help. Shows this message

Chat commands:
/new - Start a new chat session (model will forget previously generated messages)

Send a message to the bot to generate a response.
"""
    await update.message.reply_text(help_text)
    
    
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    init_msg = await update.message.reply_text(
        text="Generating response...",
        reply_to_message_id=update.message.message_id,
    )
    if context.chat_data.get("conversation") is None:
        new_chat(context)
    conversation = context.chat_data.get("conversation")
    prompt = update.message.text
    full_response = ""
    async for message in generate_response(conversation,prompt):
        try:
            full_response += message
            formatted_message = format_message(full_response)
            
            # Telegram message length limit is 4096 characters
            if len(formatted_message) > 4096:
                formatted_message = formatted_message[4096:]
                init_msg = await init_msg.reply_text(
                    text=formatted_message,
                    parse_mode=ParseMode.HTML,
                    reply_to_message_id=init_msg.message_id,
                    disable_web_page_preview=True,
                )
            else:
                if init_msg.text != "Generating response...":
                    init_msg = await init_msg.edit_text(
                        text=formatted_message,
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True,
                    )
                else:
                    init_msg = await init_msg.edit_text(
                        text=formatted_message,
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True,
                    )
        except (NetworkError, BadRequest) as e:
            print(e)
            pass
        await asyncio.sleep(0.1)
            


async def newchat_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start a new chat session."""
    init_msg = await update.message.reply_text(
        text="Starting new chat session...",
        reply_to_message_id=update.message.message_id,
    )
    new_chat(context)
    await init_msg.edit_text("New chat session started.")
