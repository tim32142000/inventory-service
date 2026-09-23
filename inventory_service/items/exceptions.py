

class BusinessRuleError(Exception):
    pass

class ItemNotFoundError(Exception):
    def __init__(self, item_id: int) -> None:
        super().__init__(f"Item {item_id} not found")