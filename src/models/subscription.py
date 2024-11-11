from datetime import datetime
from typing import Optional
import aiosqlite

class Subscription:
    """
    Handles user and guild subscription management
    """
    def __init__(self, db_path: str = "data/subscriptions.db"):
        self.db_path = db_path

    async def init_db(self):
        """Initialize the subscription database"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS subscriptions (
                    entity_id INTEGER PRIMARY KEY,
                    tier TEXT NOT NULL,
                    start_date TEXT NOT NULL,
                    end_date TEXT NOT NULL,
                    is_guild BOOLEAN NOT NULL
                )
            ''')
            await db.commit()

    async def get_subscription(self, entity_id: int, is_guild: bool = False) -> Optional[dict]:
        """
        Get subscription details for a user or guild
        
        Args:
            entity_id (int): User or Guild ID
            is_guild (bool): Whether the entity is a guild
            
        Returns:
            Optional[dict]: Subscription details if found
        """
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                'SELECT * FROM subscriptions WHERE entity_id = ? AND is_guild = ?',
                (entity_id, is_guild)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    return {
                        'entity_id': row[0],
                        'tier': row[1],
                        'start_date': row[2],
                        'end_date': row[3],
                        'is_guild': row[4]
                    }
                return None

    async def add_subscription(
        self,
        entity_id: int,
        tier: str,
        months: int = 1,
        is_guild: bool = False
    ) -> bool:
        """
        Add or update a subscription
        
        Args:
            entity_id (int): User or Guild ID
            tier (str): Subscription tier (pro/enterprise)
            months (int): Number of months to subscribe
            is_guild (bool): Whether the entity is a guild
            
        Returns:
            bool: Success status
        """
        try:
            start_date = datetime.now()
            end_date = datetime(
                start_date.year + ((start_date.month + months - 1) // 12),
                ((start_date.month + months - 1) % 12) + 1,
                start_date.day
            )

            async with aiosqlite.connect(self.db_path) as db:
                await db.execute('''
                    INSERT OR REPLACE INTO subscriptions
                    (entity_id, tier, start_date, end_date, is_guild)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    entity_id,
                    tier,
                    start_date.isoformat(),
                    end_date.isoformat(),
                    is_guild
                ))
                await db.commit()
                return True
        except Exception as e:
            print(f"Error adding subscription: {e}")
            return False