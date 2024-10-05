import json
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

client = AsyncOpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


async def chat(message_collection:list[dict[str, any]]):
    chat_completion = await client.chat.completions.create(
        messages=message_collection,
        model=os.environ.get("OPENAI_API_MODEL"))    
    return chat_completion.choices[0].message.content

