class OrderError(Exception):
    """Базовое исключение для ошибок заказа"""
    pass

class ProductNotFoundError(OrderError):
    """Товар не найден"""
    pass

class NotEnoughProductsError(OrderError):
    """Недостаточно товара"""
    pass

class NotEnoughInfoError(OrderError):
    """Недостаточно информации для создания заказа"""
    pass