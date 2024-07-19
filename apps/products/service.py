import uuid
from http import HTTPStatus

from ninja.errors import HttpError

from apps.products.models import Product
from apps.products.schema import ProductSchemaInput


class ProductService:
    def get_all_products(self):
        return Product.objects.all()

    def get_product_by_id(self, product_id: uuid.UUID):
        return Product.objects.filter(id=product_id).first()

    def get_product_by_code(self, code: str):
        return Product.objects.filter(code=code).first()

    def __filter_products(self, products: Product, **kwargs):
        if code := kwargs.get("code"):
            if not products:
                products = Product.objects.filter(code=code)
            else:
                products = products.filter(code=code)
        if un := kwargs.get("un"):
            if not products:
                products = Product.objects.filter(un=un)
            else:
                products = products.filter(un=un)
        if description := kwargs.get("description"):
            if not products:
                products = Product.objects.filter(description=description)
            else:
                products = products.filter(description=description)

        return products

    def list(self, **kwargs):
        if not kwargs.get("code") and not kwargs.get("un") and not kwargs.get("description"):
            products = self.get_all_products()
        else:
            products = self.__filter_products(None, **kwargs)
        orderby = kwargs.get("orderby", "code")
        products = products.order_by(orderby)
        total = products.count()
        offset_max = int(kwargs.get("offset_max"))
        offset_min = int(kwargs.get("offset_min"))
        data = {"total": total, "products": products[offset_min:offset_max]}
        return data

    def get(self, product_id: uuid.UUID):
        product = self.get_product_by_id(product_id)
        return product

    def create(self, input_data: ProductSchemaInput):
        if self.get_product_by_code(input_data.code):
            raise HttpError(HTTPStatus.BAD_REQUEST, "Product already exists")

        product = Product.objects.create(**input_data.dict())
        return product
