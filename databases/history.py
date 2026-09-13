from models import HistoryModel, PlayerModel
from utils import DataNotFound


class History:
    @staticmethod
    async def insert(
        history_id,
        discord_id,
        code,
        category,
        item,
        payment,
        price,
        total_price,
        created_at,
    ):
        if player := PlayerModel.objects(discord_id=discord_id).first():
            result = HistoryModel(
                history_id=history_id,
                code=code,
                category=category,
                item=item,
                player=player,
                payment=payment,
                price=price,
                total_price=total_price,
                created_at=created_at,
            )
            result.save()
            return result
        raise DataNotFound("player", discord_id)

    @staticmethod
    async def update(category, **kwargs):
        history_id = kwargs.get("history_id")
        message_id = kwargs.get("message_id")
        if category == "add_message_id":
            if history := HistoryModel.objects(history_id=history_id).first():
                history.message_id = message_id
                history.save()
                return history

    @staticmethod
    async def delete(category, **kwargs):
        history_id = kwargs.get("history_id")
        if category == "guild":
            return HistoryModel.objects.delete()
        elif category == "history_id":
            return HistoryModel.objects(history_id=history_id).delete()

    @staticmethod
    async def get(category, **kwargs):
        history_id = kwargs.get("history_id")
        if category == "guild":
            return list(HistoryModel.objects())
        elif category == "history_id":
            return HistoryModel.objects(history_id=history_id).first()
        elif category == "all":
            return list(HistoryModel.objects.all())
