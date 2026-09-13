from models import StockModel, ProductModel
from utils import DataNotFound


class Stock:
    @staticmethod
    async def insert(
        code=None,
        file_name=None,
        item=None,
        created_at=None,
        category=None,
        bulk_items=None,
    ):
        if category == "bulk":
            return StockModel.objects.insert(bulk_items)
        if product := ProductModel.objects.get(code=code):
            stock = StockModel(
                file_name=file_name, item=item, product=product, created_at=created_at
            )
            stock.save()
            return stock
        raise DataNotFound("product", code)

    @staticmethod
    async def get(category, **kwargs):
        code = kwargs.get("code")
        item = kwargs.get("item")
        created_at = kwargs.get("created_at")
        if category == "code":
            if cd := ProductModel.objects(code=code).first():
                return StockModel.objects.filter(product=cd)
        elif category == "item":
            if cd := ProductModel.objects(code=code).first():
                return StockModel.objects.filter(product=cd, item=item).first()
        elif category == "all":
            return StockModel.objects.all()
        elif category == "created_at":
            if cd := ProductModel.objects(code=code).first():
                return StockModel.objects.filter(
                    product=cd, item=item, created_at=created_at
                ).first()

    @staticmethod
    async def delete(category, **kwargs):
        code = kwargs.get("code")
        item = kwargs.get("item")
        created_at = kwargs.get("created_at")
        if category == "code":
            if cd := ProductModel.objects(code=code).first():
                stock = StockModel.objects.filter(
                    product=cd, item=item, created_at=created_at
                ).delete()
                return stock
        elif category == "last":
            if cd := ProductModel.objects(code=code).first():
                return StockModel.objects(product=cd).first().delete()
        elif category == "clear":
            if cd := ProductModel.objects(code=code).first():
                return StockModel.objects(product=cd).delete()
        elif category == "bulk_delete":
            return StockModel.objects(created_at__in=item).delete()

    @staticmethod
    async def update(category, **kwargs):
        code = kwargs.get("code")
        item = kwargs.get("item")
        new_item = kwargs.get("new_item")
        if category == "edit":
            if cd := ProductModel.objects(code=code).first():
                if st := StockModel.objects.filter(product=cd, item=item).first():
                    st.item = new_item
                    st.save()
                    return st
