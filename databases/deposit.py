from models import DepositModel, GrowtopiaModel


class Deposit:
    @staticmethod
    async def insert(world, owner, bot, saweria, trakteer, sociabuzz):
        if data := DepositModel.objects().first():
            data.growtopia.world = world
            data.growtopia.owner = owner
            data.growtopia.bot = bot
            data.trakteer = trakteer
            data.saweria = saweria
            data.sociabuzz = sociabuzz
            data.save()
            return data
        growtopia = GrowtopiaModel(world=world, owner=owner, bot=bot)
        result = DepositModel(
            growtopia=growtopia, trakteer=trakteer, saweria=saweria, sociabuzz=sociabuzz
        )
        result.save()
        return result

    @staticmethod
    async def update(**kwargs):
        pass

    @staticmethod
    async def delete(category, **kwargs):
        if category == "guild":
            return DepositModel.objects().first().delete()

    @staticmethod
    async def get(category, **kwargs):
        if category == "guild":
            return DepositModel.objects().first()
