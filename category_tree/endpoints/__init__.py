from .category import api_router as category_router
from .client import api_router as client_router
from .order import api_router as order_router
from .ping import api_router as application_health_router
from .product import api_router as product_router


list_of_routes = [
    category_router,
    client_router,
    order_router,
    application_health_router,
    product_router,
]

__all__ = [
    "list_of_routes",
]
