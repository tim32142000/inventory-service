from pydantic import BaseModel, Field, field_validator


class ItemCreate(BaseModel):
    name: str = Field(min_length=1)
    category: str
    price: int = Field(ge=0)
    quantity: int = Field(ge=0)


class StockAdjustment(BaseModel):
    change: int

    @field_validator("change")
    @classmethod
    def change_must_not_be_zero(cls, value: int) -> int:
        if value == 0:
            raise ValueError("Change cannot be 0")

        return value


class ItemResponse(BaseModel):
    id: int
    name: str = Field(min_length=1)
    category: str
    price: int = Field(ge=0)
    quantity: int = Field(ge=0)
