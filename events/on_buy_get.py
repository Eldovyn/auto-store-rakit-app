import nextcord
from nextcord.ext import commands, tasks
from databases import BuyGet as BuyGetDatabase, LiveStock as LiveStockDatabase


class OnBuyGet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loop_task = self.check_current_task.start()

    def cog_unload(self):
        self.loop_task.cancel()

    @tasks.loop(minutes=5)
    async def check_current_task(self):
        if data := await BuyGetDatabase().get("guild"):
            for index, item in enumerate(data):
                now = nextcord.utils.utcnow().timestamp()
                promotion_end = item.promotion_end
                if promotion_end == 0:
                    continue
                if promotion_end <= now:
                    await BuyGetDatabase().delete("product", code=item.product.code)
                    await LiveStockDatabase().update(
                        "product", updated_at=nextcord.utils.utcnow().timestamp()
                    )

    @check_current_task.before_loop
    async def before_check_current_task(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(OnBuyGet(bot))
