from dataclasses import dataclass

from dimensions import Dimensions
from meta import Meta
from review import Review


@dataclass
class Product:
    id: int
    title: str
    description: str
    category: str
    price: float
    discountPercentage: float
    rating: float
    stock: int
    tags: list[str]
    brand: str
    sku: str
    weight: int
    dimensions: Dimensions
    warrantyInformation: str
    shippingInformation: str
    availabilityStatus: str
    reviews: list[Review]
    returnPolicy: str
    minimumOrderQuantity: int
    meta: Meta
    images: list[str]
    thumbnail: str