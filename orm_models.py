from sqlalchemy import CheckConstraint, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ItemRecord(Base):
    __tablename__ = "items"

    __table_args__ = (
        CheckConstraint(
            "length(name) > 0",
            name="ck_items_name_not_empty",
        ),
        CheckConstraint(
            "price >= 0",
            name="ck_items_price_nonnegative",
        ),
        CheckConstraint(
            "quantity >= 0",
            name="ck_items_quantity_nonnegative",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(Text)
    price: Mapped[int]
    quantity: Mapped[int]
