from dataclasses import dataclass
from datetime import datetime


@dataclass
class Review:
    rating: int
    comment: str
    date: datetime
    reviewerName: str
    reviewerEmail: str