from ninja import NinjaAPI, Redoc

from apps.authentication.api import authentication_router
from apps.departments.api import departments_router
from apps.products.api import products_router
from apps.purchases.api import purchases_router

api = NinjaAPI(
    csrf=False,
    title="Requisition API",
    version="2.0.0",
    description="This is a simple API to manage requisitions",
)


api.add_router("/auth", authentication_router, tags=["Authentication"])
api.add_router("/products", products_router, tags=["Products"])
api.add_router("/purchases", purchases_router, tags=["Purchases"])
api.add_router("/departments", departments_router, tags=["Departments"])
