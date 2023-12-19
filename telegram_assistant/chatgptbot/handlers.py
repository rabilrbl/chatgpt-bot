import asyncio
import typing as ty
from telegram import Update
from telegram.ext import (
    ContextTypes,
)
from telegram.error import NetworkError, BadRequest
from telegram.constants import ChatAction, ParseMode
from telegram_assistant.chatgpt import chatgpt

chats: dict[str, ty.Any] = {}
CHATGPT = None

async def init_chatgpt() -> None:
    global CHATGPT
    CHATGPT = await chatgpt()

async def new_chat(chat_id: int) -> None:
    chats[chat_id] = {
        "conversation": CHATGPT.create_new_conversation(),
    }
    
async def generate_response(conversation, prompt: str):
    pending_response = ""
    # yield streaming response
    async for message in conversation.chat(prompt):
        pending_response += message['content']
        if pending_response and len(pending_response) > 50:
            yield pending_response
            pending_response = ""
    if pending_response:
        yield pending_response

async def start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!\n\nStart sending messages with me to generate a response.\n\nSend /new to start a new chat session.",
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
    
    
async def handle_message(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    init_msg = await update.message.reply_text(
        text="Generating response...",
        reply_to_message_id=update.message.message_id,
    )
    if update.message.chat.id not in chats:
        await new_chat(update.message.chat.id)
    conversation = chats[update.message.chat_id]["conversation"]
    prompt = update.message.text
    async for message in generate_response(conversation,prompt):
        try:
            if init_msg.text != "Generating response...":
                init_msg = await init_msg.edit_text(
                    text=init_msg.text + message,   
                )
            else:
                init_msg = await init_msg.edit_text(
                    text=message,
                )
        except (NetworkError, BadRequest) as e:
            print(e)
            pass
        await asyncio.sleep(0.5)
            


async def newchat_command(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Start a new chat session."""
    init_msg = await update.message.reply_text(
        text="Starting new chat session...",
        reply_to_message_id=update.message.message_id,
    )
    await new_chat(update.message.chat.id)
    await init_msg.edit_text("New chat session started.")