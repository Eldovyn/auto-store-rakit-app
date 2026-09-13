import nextcord
from nextcord.ext import commands
import yaml
from databases import RateDL as RateDlDatabase
from utils import Misc, InteractionResponse, DataNotFound


class RateDl(commands.Cog):
    from utils.config import data

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="to show rate diamond lock")
    async def rate_dl(
        self,
        interaction: nextcord.Interaction,
    ):
        await InteractionResponse.response_loading(interaction)
        if rdl := await RateDlDatabase().get():
            rupiah = await Misc().format_rupiah(rdl.rate)
            await interaction.followup.send(
                embed=nextcord.Embed(
                    description=f"**Rate DL : `{rupiah}`**",
                    color=nextcord.Color.green(),
                ),
                ephemeral=True,
            )
            return await InteractionResponse.response_success(
                interaction, "show rate dl", self.data["emoji_tick"]
            )
        await InteractionResponse().response_error(
            interaction,
            f"process your transaction",
            self.data["emoji_cross"],
            "rate dl not available",
        )

    @nextcord.slash_command(description="to calculate rate diamond lock")
    async def calc_dl(
        self,
        interaction: nextcord.Interaction,
        rupiah: float = nextcord.SlashOption(
            description="rupiah your want to calculate", required=True, min_value=1
        ),
    ):
        await InteractionResponse.response_loading(interaction)
        if rdl := await RateDlDatabase().get():
            format_rupiah = await Misc().format_rupiah(rupiah)
            world_lock = await Misc().calculate_rate_dl(rdl.rate, rupiah)
            await interaction.followup.send(
                embed=nextcord.Embed(
                    description=f"**`{format_rupiah}` = `{world_lock} world lock`**",
                    color=nextcord.Color.green(),
                ),
                ephemeral=True,
            )
            return await InteractionResponse.response_success(
                interaction, "calculate rate dl", self.data["emoji_tick"]
            )
        raise DataNotFound("rate dl", interaction.guild.id)


def setup(bot):
    bot.add_cog(RateDl(bot))
