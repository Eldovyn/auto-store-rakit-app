import nextcord
from nextcord.ext import commands, application_checks
import yaml
from databases import (
    Deposit as DepositDatabase,
    RateDL as RateDlDatabase,
    EnableDonate,
    EnableSaweria,
    EnableSociabuzz,
    EnableTrakteer,
)
from utils import DataNotFound, CustomCheck, Misc, InteractionResponse
from ui import GrowID as GrowIDView


class DepositSlashCommand(commands.Cog):
    from utils.config import data as data_content

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="deposit",
        description="deposit balance",
    )
    @application_checks.check(CustomCheck().check_maintenance)
    async def deposit(self, interaction: nextcord.Interaction):
        pass

    @deposit.subcommand(
        description="deposit balance with non-qris", name="non-qris", inherit_hooks=True
    )
    async def non_qris(self, interaction: nextcord.Interaction):
        await InteractionResponse.response_loading(interaction)
        view = GrowIDView(self.bot)
        if data := await DepositDatabase().get("guild"):
            if data.growtopia:
                if not (
                    (st := await EnableDonate().get("guild")) and not st.status
                ) or not (str := await EnableDonate().get("guild")):
                    await interaction.followup.send(
                        embed=nextcord.Embed(
                            description=f"""**World Deposit {interaction.guild.name}**
```yml
World: {data.growtopia.world}
Owner: {data.growtopia.owner}
Bot: {data.growtopia.bot}```""",
                            color=nextcord.Color.green(),
                        ).set_image(self.data_content["thumbnail"]),
                        ephemeral=True,
                        view=view,
                    )
            if data.trakteer:
                if not (
                    (st := await EnableTrakteer().get("guild")) and not st.status
                ) or not (str := await EnableTrakteer().get("guild")):
                    await interaction.followup.send(
                        embed=nextcord.Embed(
                            description=f"**Trakteer Link : {data.trakteer}**",
                            color=nextcord.Color.green(),
                        ).set_image(self.data_content["thumbnail"]),
                        ephemeral=True,
                        view=view,
                    )
            if data.saweria:
                if not (
                    (st := await EnableSaweria().get("guild")) and not st.status
                ) or not (str := await EnableSaweria().get("guild")):
                    await interaction.followup.send(
                        embed=nextcord.Embed(
                            description=f"**Saweria Link : {data.saweria}**",
                            color=nextcord.Color.green(),
                        ).set_image(self.data_content["thumbnail"]),
                        ephemeral=True,
                        view=view,
                    )
            if data.sociabuzz:
                if not (
                    (st := await EnableSociabuzz().get("guild")) and not st.status
                ) or not (str := await EnableSociabuzz().get("guild")):
                    await interaction.followup.send(
                        embed=nextcord.Embed(
                            description=f"**Sociabuzz Link : {data.sociabuzz}**",
                            color=nextcord.Color.green(),
                        ).set_image(self.data_content["thumbnail"]),
                        ephemeral=True,
                        view=view,
                    )
            return await InteractionResponse.response_success(
                interaction, "show deposit", self.data_content["emoji_tick"]
            )
        raise DataNotFound("deposit", interaction.guild.id)


def setup(bot):
    bot.add_cog(DepositSlashCommand(bot))
