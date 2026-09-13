import nextcord
from nextcord.ext import commands, tasks
from databases import Giveaway as GiveawayDatabase
from io import BytesIO
import random


class OnGiveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loop_task = self.check_current_task.start()

    def cog_unload(self):
        self.loop_task.cancel()

    @tasks.loop(minutes=5)
    async def check_current_task(self):
        if data := await GiveawayDatabase().get("guild"):
            created_at = nextcord.utils.utcnow().timestamp()
            for index, item in enumerate(data):
                now = nextcord.utils.utcnow().timestamp()
                discount_end = item.giveaway_end
                if discount_end <= now:
                    guild = self.bot.get_guild(item.guild_id)
                    channel = guild.get_channel(item.channel_id)
                    message = await channel.fetch_message(item.message_id)
                    users = [user async for user in message.reactions[0].users()]
                    users = [
                        user
                        for user in users
                        if user != self.bot.user or user.id != item.hoster_id
                    ]
                    message_edit = await message.edit(
                        f"**Giveaway Ended <t:{int(created_at)}:R>**",
                    )
                    if len(users) == 0:
                        return await message.reply(
                            "**no one win, please try again later**"
                        )
                    user_winner = random.choice(users)
                    await message_edit.reply(f"**winner is : {user_winner.mention}**")
                    file_data = BytesIO(item.item)
                    file_data.seek(0)
                    await user_winner.send(
                        f"**congrats {user_winner.mention}, you win giveaway `{item.description}`**",
                        file=nextcord.File(file_data, f"{item.file_name}"),
                    )
                    await GiveawayDatabase().delete(
                        "created_at", created_at=item.created_at
                    )

    @check_current_task.before_loop
    async def before_check_current_task(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(OnGiveaway(bot))
