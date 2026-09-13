import nextcord
from nextcord.ext import commands, tasks
from databases import Discount as DiscountDatabase, LiveStock as LiveStockDatabase


class OnDiscount(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loop_task = self.check_current_task.start()

    def cog_unload(self):
        self.loop_task.cancel()

    @tasks.loop(minutes=5)
    async def check_current_task(self):
        if data := await DiscountDatabase().get("guild"):
            for index, item in enumerate(data):
                now = nextcord.utils.utcnow().timestamp()
                discount_end = item.discount_end
                if discount_end == 0:
                    continue
                if discount_end <= now:
                    await DiscountDatabase().delete("product", code=item.product.code)
                    await LiveStockDatabase().update(
                        "product", updated_at=nextcord.utils.utcnow().timestamp()
                    )

    @check_current_task.before_loop
    async def before_check_current_task(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(OnDiscount(bot))
