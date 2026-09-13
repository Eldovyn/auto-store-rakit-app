from models import LiveStockModel


class LiveStock:
    @staticmethod
    async def insert(guild_id, message_id, channel_id, updated_at):
        if ls := LiveStockModel.objects(guild_id=guild_id).first():
            ls.channel_id = channel_id
            ls.message_id = message_id
            ls.save()
            return ls
        else:
            live_stock = LiveStockModel(
                guild_id=guild_id,
                channel_id=channel_id,
                message_id=message_id,
                updated_at=updated_at,
            )
            live_stock.save()
            return live_stock

    @staticmethod
    async def update(category, **kwargs):
        updated_at = kwargs.get("updated_at")
        if category == "product":
            if ls := LiveStockModel.objects().first():
                ls.updated_at = updated_at
                ls.save()
                return ls

    @staticmethod
    async def delete(category, **kwargs):
        message_id = kwargs.get("message_id")
        channel_id = kwargs.get("channel_id")
        if category == "message_id":
            return LiveStockModel.objects(message_id=message_id).delete()
        elif category == "guild":
            return LiveStockModel.objects.delete()
        elif category == "channel":
            return LiveStockModel.objects(channel_id=channel_id).delete()

    @staticmethod
    async def get(category, **kwargs):
        message_id = kwargs.get("message_id")
        channel_id = kwargs.get("channel_id")
        if category == "guild":
            return LiveStockModel.objects().first()
        elif category == "message_id":
            return LiveStockModel.objects(message_id=message_id).first()
        elif category == "channel_id":
            return LiveStockModel.objects(channel_id=channel_id).first()
