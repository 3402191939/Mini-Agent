def calculate_total(price: float, quantity: int) -> float:
    if price < 0:
        raise ValueError("Price cannot be negative")

    if quantity <= 0:
        raise ValueError("Quantity must be a positive number")

    subtotal = price * quantity

    if subtotal >= 100:
        return subtotal * 0.9

    return subtotal