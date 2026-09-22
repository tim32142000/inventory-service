from dataclasses import dataclass


@dataclass
class Item:
    name: str
    category: str
    price: int
    quantity: int
    id: int | None = None
