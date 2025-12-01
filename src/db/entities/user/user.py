from dataclasses import dataclass
from typing import Optional


@dataclass
class UserEntity:
    discord_id: int
    avatar_url: Optional[str] = None
    id: Optional[int] = None
