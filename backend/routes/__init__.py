# routes package
from .auth_routes import auth
from .customer_routes import customers
from .products_routes import products
from .milk_entry_routes import milk_entries
from .daily_entry_route import daily_entries
from .payment_routes import payments
from .billing_routes import billing

__all__ = [
    "auth",
    "customers",
    "products",
    "milk_entries",
    "daily_entry_route",
    "payments",
    "billing",
]

