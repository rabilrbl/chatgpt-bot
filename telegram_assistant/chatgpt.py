import os, sys, asyncio
from re_gpt import AsyncChatGPT
from dotenv import load_dotenv

load_dotenv()

session_token = os.getenv("SESSION_TOKEN")

if sys.version_info >= (3, 8) and sys.platform.lower().startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    

async def chatgpt() -> AsyncChatGPT:
    return await AsyncChatGPT(session_token=session_token).__aenter__()