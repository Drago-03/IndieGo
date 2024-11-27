import aiosqlite

async def init_db():
    async with aiosqlite.connect('data/messages.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.commit()

if __name__ == "__main__":
    import asyncio
    asyncio.run(init_db())
