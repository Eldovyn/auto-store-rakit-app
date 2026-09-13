import nextcord
from nextcord.ext import commands, application_checks
from utils import (
    DataNotFound,
    DuplicateData,
    OnMaintenance,
    ImageNotAllow,
    DiscountNotAllow,
    NumberNotAllow,
    BalanceNotEnough,
    ChannelNotAllow,
    TimeInvalid,
    DisableQris,
    InteractionResponse,
)
from ui import GrowID as GrowIDUI
import yaml


class OnApplicationCommandError(commands.Cog):
    from utils.config import data

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, interaction, error):
        error = getattr(error, "original", error)
        if isinstance(error, OnMaintenance):
            return await interaction.send(
                embed=nextcord.Embed(
                    description=f"""{self.data["emoji_cross"]} failed process your transaction
-# bot is maintenance""",
                    color=nextcord.Color.red(),
                ),
                ephemeral=True,
            )
        elif isinstance(error, ChannelNotAllow):
            return await interaction.send(
                embed=nextcord.Embed(
                    description=f"""{self.data["emoji_cross"]} failed process your transaction
-# this channel not allow""",
                    color=nextcord.Color.red(),
                ),
                ephemeral=True,
            )
        elif isinstance(error, TimeInvalid):
            return await InteractionResponse().response_error(
                interaction,
                "process your transaction",
                self.data["emoji_cross"],
                "duration is invalid",
            )
        elif isinstance(error, application_checks.ApplicationMissingAnyRole):
            return await interaction.send(
                embed=nextcord.Embed(
                    description=f"""{self.data["emoji_cross"]} failed process your transaction
-# you don't have role `{', '.join((nextcord.utils.get(interaction.guild.roles, id=r)).name for r in error.missing_roles)}` to use this command""",
                    color=nextcord.Color.red(),
                ),
                ephemeral=True,
            )
        elif isinstance(error, application_checks.ApplicationMissingRole):
            return await interaction.send(
                embed=nextcord.Embed(
                    description=f"""{self.data["emoji_cross"]} failed process your transaction
-# you don't have role `{', '.join((nextcord.utils.get(interaction.guild.roles, id=r)).name for r in error.missing_roles)}` to use this command""",
                    color=nextcord.Color.red(),
                ),
                ephemeral=True,
            )
        elif isinstance(error, DisableQris):
            return await InteractionResponse().response_error(
                interaction,
                "process your transaction",
                self.data["emoji_cross"],
                "qris is disable",
            )
        elif isinstance(error, DataNotFound):
            view = GrowIDUI(self.bot)
            if error.category == "player":
                if interaction.user.id == error.data:
                    return await InteractionResponse().response_error(
                        interaction,
                        "process your transaction",
                        self.data["emoji_cross"],
                        "you not register yet",
                        view=view,
                    )
                return await InteractionResponse().response_error(
                    interaction,
                    "process your transaction",
                    self.data["emoji_cross"],
                    "user not have growid",
                )
            return await InteractionResponse().response_error(
                interaction,
                "process your transaction",
                self.data["emoji_cross"],
                f"{error.category} not found",
            )
        elif isinstance(error, DiscountNotAllow):
            return await InteractionResponse().response_error(
                interaction,
                "update discount product",
                self.data["emoji_cross"],
                f"price `{error.price}` not allow",
            )
        elif isinstance(error, NumberNotAllow):
            return await interaction.edit_original_message(
                embed=nextcord.Embed(
                    description=f"**number `{error.number}` not allow**",
                    color=nextcord.Color.red(),
                ),
            )
        elif isinstance(error, DuplicateData):
            if error.category == "product":
                return await InteractionResponse().response_error(
                    interaction,
                    "update product",
                    self.data["emoji_cross"],
                    f"duplicate data {error.data}",
                )
            elif error.category == "growid":
                return await InteractionResponse().response_error(
                    interaction,
                    "set growid",
                    self.data["emoji_cross"],
                    f"{error.data} already exist",
                )
            elif error.category == "discount":
                return await interaction.edit_original_message(
                    embed=nextcord.Embed(
                        description=f"**discount `{error.data}` already exist**",
                        color=nextcord.Color.red(),
                    ),
                )
            elif error.category == "buy_get":
                return await interaction.edit_original_message(
                    embed=nextcord.Embed(
                        description=f"**buy get `{error.data}` already exist**",
                        color=nextcord.Color.red(),
                    ),
                )
        elif isinstance(error, ImageNotAllow):
            return await interaction.edit_original_message(
                embed=nextcord.Embed(
                    description=f"**`{error.image_type}` not allow**",
                    color=nextcord.Color.red(),
                ),
            )
        elif isinstance(error, BalanceNotEnough):
            return await interaction.edit_original_message(
                embed=nextcord.Embed(
                    description=f"**balance `{error.amount} world lock` not enough**",
                    color=nextcord.Color.red(),
                ),
            )
        else:
            raise error


def setup(bot):
    bot.add_cog(OnApplicationCommandError(bot))
