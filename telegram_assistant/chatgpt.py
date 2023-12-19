import os, sys, asyncio
from re_gpt import AsyncChatGPT
from dotenv import load_dotenv

load_dotenv()

session_token = os.getenv("SESSION_TOKEN")

if sys.version_info >= (3, 8) and sys.platform.lower().startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    

async def chatgpt() -> AsyncChatGPT:
    return await AsyncChatGPT(session_token=session_token).__aenter__()


async def generate_response(conversation, prompt: str):
    pending_response = ""
    # yield streaming response
    async for message in conversation.chat(prompt):
        pending_response += message['content']
        if pending_response and len(pending_response) > 100:
            yield pending_response
            pending_response = ""
    if pending_response:
        yield pending_response