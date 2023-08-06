from dataclasses import dataclass
from datetime import datetime


@dataclass
class ApiKey:
    key_id: str
    name: str
    description: str
    created_at: datetime
