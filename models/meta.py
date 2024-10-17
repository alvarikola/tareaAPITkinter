from dataclasses import dataclass
from datetime import datetime


@dataclass
class Meta:
    createdAt: datetime
    updatedAt: datetime
    barcode: str
    qrCode: str