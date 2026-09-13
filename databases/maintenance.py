from .database import Database
from models import MaintenanceModel


class Maintenance(Database):
    @staticmethod
    async def insert(created_at, status):
        if mt := MaintenanceModel.objects().first():
            mt.created_at = created_at
            mt.status = not mt.status
            mt.save()
            return mt
        mt = MaintenanceModel(created_at=created_at, status=status)
        mt.save()
        return mt

    @staticmethod
    async def update(**kwargs):
        pass

    @staticmethod
    async def delete(category, **kwargs):
        if category == "guild":
            return MaintenanceModel.objects().delete()

    @staticmethod
    async def get(category, **kwargs):
        if category == "all":
            return MaintenanceModel.objects.all()
        elif category == "maintenance":
            return MaintenanceModel.objects().first()
