# test_atlas.py
import asyncio
from db import db

async def run():
    try:
        print("Listing collections...")
        names = await db.list_collection_names()
        print("Collections:", names)
    except Exception as e:
        print("ERROR:", e)

asyncio.run(run())
