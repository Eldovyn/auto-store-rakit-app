from models import ProductModel
from utils import DataNotFound


class Product:
    @staticmethod
    async def insert(title, description, code, role, category, min_buy, price):
        product = ProductModel(
            title=title,
            description=description,
            code=code,
            role=role,
            category=category,
            price=price,
            min_buy=min_buy,
        )
        product.save()
        return product

    @staticmethod
    async def get(category, **kwargs):
        code = kwargs.get("code")
        if category == "code":
            return ProductModel.objects(code=code).first()
        elif category == "all":
            return list(ProductModel.objects.all())

    @staticmethod
    async def update(category, **kwargs):
        code = kwargs.get("code")
        new_code = kwargs.get("new_code")
        role = kwargs.get("role")
        new_title = kwargs.get("new_title")
        min_buy = kwargs.get("min_buy")
        price = kwargs.get("price")
        new_description = kwargs.get("new_description")
        if category == "price":
            if product := ProductModel.objects(code=code).first():
                product.price = price
                product.save()
                return product
            raise DataNotFound("product", code)
        elif category == "code":
            if product := ProductModel.objects(code=code).first():
                product.code = new_code
                product.save()
                return product
            raise DataNotFound("product", code)
        elif category == "role":
            if product := ProductModel.objects(code=code).first():
                product.role = role
                product.save()
                return product
            raise DataNotFound("product", code)
        elif category == "title":
            if product := ProductModel.objects(code=code).first():
                product.title = new_title
                product.save()
                return product
            raise DataNotFound("product", code)
        elif category == "min-buy":
            if product := ProductModel.objects(code=code).first():
                product.min_buy = min_buy
                product.save()
                return product
            raise DataNotFound("product", code)
        elif category == "new_description":
            if product := ProductModel.objects(code=code).first():
                product.description = new_description
                product.save()
                return product
            raise DataNotFound("product", code)

    @staticmethod
    async def delete(category, **kwargs):
        code = kwargs.get("code")
        if category == "code":
            return ProductModel.objects(code=code).delete()
        elif category == "guild":
            return ProductModel.objects.delete()
