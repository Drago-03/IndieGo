import pytest
import asyncio
from datetime import datetime, timedelta
from src.models.subscription import Subscription

@pytest.fixture
async def subscription():
    sub = Subscription(":memory:")
    await sub.init_db()
    return sub

@pytest.mark.asyncio
async def test_add_subscription(subscription):
    success = await subscription.add_subscription(
        123,
        "pro",
        months=1,
        is_guild=False
    )
    assert success

    sub_details = await subscription.get_subscription(123)
    assert sub_details is not None
    assert sub_details["tier"] == "pro"

@pytest.mark.asyncio
async def test_get_nonexistent_subscription(subscription):
    sub_details = await subscription.get_subscription(999)
    assert sub_details is None

@pytest.mark.asyncio
async def test_subscription_duration(subscription):
    await subscription.add_subscription(
        456,
        "enterprise",
        months=12,
        is_guild=True
    )
    
    sub_details = await subscription.get_subscription(456, is_guild=True)
    start_date = datetime.fromisoformat(sub_details["start_date"])
    end_date = datetime.fromisoformat(sub_details["end_date"])
    
    # Check if subscription duration is approximately 1 year
    assert (end_date - start_date).days >= 364