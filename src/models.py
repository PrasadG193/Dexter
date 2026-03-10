"""Order domain model and status constants."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import uuid

VALID_STATUSES = ("pending", "fulfilled", "cancelled")

STATUS_TRANSITIONS: dict[str, set[str]] = {
    "pending": {"fulfilled", "cancelled"},
    "fulfilled": set(),
    "cancelled": set(),
}


@dataclass
class Order:
    customer: str
    item: str
    quantity: int
    price: float
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: str = "pending"
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
