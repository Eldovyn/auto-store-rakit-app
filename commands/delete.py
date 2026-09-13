import nextcord
from nextcord.ext import commands, application_checks
import yaml
from databases import (
    Product as ProductDatabase,
    Player as PlayerDatabase,
    Reputation as ReputationDatabase,
    Maintenance as MaintenanceDatabase,
    History as HistoryDatabase,
    Deposit as DepositDatabase,
    LiveStock as LiveStockDatabase,
    Leaderboard as LeaderboardDatabase,
    Verification as VerificationDatabase,
    Discount as DiscountDatabase,
    ReputationChannel as ReputationChannelDatabase,
    Purchase as PurchaseDatabase,
    Giveaway as GiveawayDatabase,
    BuyGet as BuyGetDatabase,
)
from modals import (
    DeleteBuyGetModal,
    DeleteGiveawayModal,
    DeleteDiscountModal,
    DeleteHistoryModal,
    DeletePlayerModal,
    DeleteReputationModal,
    DeleteProductModal,
)
from utils import DataNotFound, CustomCheck, InteractionResponse


class DeleteSlashCommand(commands.Cog):
    from utils.config import data

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="to delete data in database")
    @application_checks.check(CustomCheck().check_admin)
    async def delete(
        self,
        interaction: nextcord.Interaction,
        category: str = nextcord.SlashOption(
            name="category",
            choices={
                "live-stock": "live-stock",
                "leaderboard": "leaderboard",
                "verification": "verification",
                "product": "product",
                "player": "player",
                "reputation": "reputation",
                "maintenance": "maintenance",
                "history": "history",
                "deposit": "deposit",
                "discount": "discount",
                "giveaway": "giveaway",
                "buy-get": "buy-get",
            },
            required=True,
        ),
    ):
        if category == "live-stock":
            await interaction.response.send_message(
                embed=nextcord.Embed(
                    description=f"**{self.data['emoji_loading']} process your transaction**",
                    color=nextcord.Color.yellow(),
                ),
                ephemeral=True,
            )
            if data := await LiveStockDatabase().get("guild"):
                try:
                    message = await interaction.guild.get_channel(
                        data.channel_id
                    ).fetch_message(data.message_id)
                    await message.delete()
                except:
                    await LiveStockDatabase().delete("guild")
                    raise DataNotFound("channel live stock")
                return await InteractionResponse().response_success(
                    interaction,
                    f"delete live stock {interaction.guild.name}",
                    self.data["emoji_tick"],
                )
            raise DataNotFound("channel live stock")
        elif category == "giveaway":
            modal = DeleteGiveawayModal()
            await interaction.response.send_modal(modal)
        elif category == "buy-get":
            modal = DeleteBuyGetModal(self.bot)
            await interaction.response.send_modal(modal)
        elif category == "leaderboard":
            await interaction.response.send_message(
                embed=nextcord.Embed(
                    description=f"**{self.data['emoji_loading']} process your transaction**",
                    color=nextcord.Color.yellow(),
                ),
                ephemeral=True,
            )
            if data := await LeaderboardDatabase().get("guild"):
                try:
                    message = await interaction.guild.get_channel(
                        data.channel_id
                    ).fetch_message(data.message_id)
                    await message.delete()
                except:
                    await LeaderboardDatabase().delete("guild")
                    raise DataNotFound("channel leaderboard")
                return await InteractionResponse().response_success(
                    interaction,
                    f"delete leaderboard {interaction.guild.name}",
                    self.data["emoji_tick"],
                )
            raise DataNotFound("channel leaderboard")
        elif category == "verification":
            await interaction.response.send_message(
                embed=nextcord.Embed(
                    description=f"**{self.data['emoji_loading']} process your transaction**",
                    color=nextcord.Color.yellow(),
                ),
                ephemeral=True,
            )
            if data := await VerificationDatabase().get("guild"):
                try:
                    message = await interaction.guild.get_channel(
                        data.channel_id
                    ).fetch_message(data.message_id)
                    await message.delete()
                except:
                    await VerificationDatabase().delete("guild")
                    raise DataNotFound("verification", interaction.guild_id)
                return await InteractionResponse().response_success(
                    interaction,
                    f"delete verification {interaction.guild.name}",
                    self.data["emoji_tick"],
                )
            raise DataNotFound("verification", interaction.guild_id)
        elif category == "product":
            modal = DeleteProductModal(self.bot)
            await interaction.response.send_modal(modal)
        elif category == "player":
            modal = DeletePlayerModal(self.bot)
            await interaction.response.send_modal(modal)
        elif category == "reputation":
            modal = DeleteReputationModal()
            await interaction.response.send_modal(modal)
        elif category == "maintenance":
            await MaintenanceDatabase().delete("guild")
            return await InteractionResponse().response_success(
                interaction,
                f"set maintenance : `False`",
                self.data["emoji_tick"],
            )
        elif category == "deposit":
            await interaction.response.send_message(
                embed=nextcord.Embed(
                    description=f"**{self.data['emoji_loading']} process your transaction**",
                    color=nextcord.Color.yellow(),
                ),
                ephemeral=True,
            )
            if not (data := await DepositDatabase().get("guild")):
                raise DataNotFound("deposit", interaction.guild_id)
            await DepositDatabase().delete("guild")
            return await InteractionResponse().response_success(
                interaction,
                f"success disable deposit {interaction.guild.name}",
                self.data["emoji_tick"],
            )
        elif category == "discount":
            discount_modal = DeleteDiscountModal(self.bot)
            await interaction.response.send_modal(discount_modal)
        else:
            history_modal = DeleteHistoryModal()
            await interaction.response.send_modal(history_modal)

    @nextcord.slash_command(description="to clear data in database")
    @application_checks.check(CustomCheck().check_admin)
    async def clear(
        self,
        interaction: nextcord.Interaction,
        category: str = nextcord.SlashOption(
            name="category",
            choices={
                "product": "product",
                "player": "player",
                "reputation": "reputation",
                "history": "history",
                "discount": "discount",
                "giveaway": "giveaway",
                "buy-get": "buy-get",
            },
            required=True,
        ),
    ):
        await interaction.response.send_message(
            embed=nextcord.Embed(
                description=f"**{self.data['emoji_loading']} process your transaction**",
                color=nextcord.Color.yellow(),
            ),
            ephemeral=True,
        )
        if category == "product":
            if not (prod := await ProductDatabase().get("all")):
                raise DataNotFound("product", interaction.guild_id)
            await ProductDatabase().delete("guild")
        elif category == "buy-get":
            if not (buy_get := await BuyGetDatabase().get("guild")):
                raise DataNotFound("buy-get", interaction.guild_id)
            await BuyGetDatabase().delete("guild")
        elif category == "giveaway":
            if not (giveaway := await GiveawayDatabase().get("guild")):
                raise DataNotFound("giveaway", interaction.guild_id)
            for g in giveaway:
                channel = interaction.guild.get_channel(g.channel_id)
                message = await channel.fetch_message(g.message_id)
                if message:
                    await message.delete()
            await GiveawayDatabase().delete("guild")
        elif category == "player":
            if not (player := await PlayerDatabase().get("all")):
                raise DataNotFound("player", interaction.guild_id)
            await PlayerDatabase().delete("guild")
        elif category == "reputation":
            if not (reputation := await ReputationDatabase().get("guild")):
                raise DataNotFound("reputation", interaction.guild_id)
            await interaction.guild.get_channel(
                (await ReputationChannelDatabase().get()).channel_id
            ).purge()
            await interaction.guild.get_channel(self.data["channel_reputation"]).purge()
            await ReputationDatabase().delete("guild")
        elif category == "discount":
            if not (discount := await DiscountDatabase().get("guild")):
                raise DataNotFound("discount", interaction.guild_id)
            await DiscountDatabase().delete("guild")
        else:
            if not (history := await HistoryDatabase().get("all")):
                raise DataNotFound("history", interaction.guild_id)
            await interaction.guild.get_channel(
                (await PurchaseDatabase().get()).channel_id
            ).purge()
            await HistoryDatabase().delete("guild")
        await InteractionResponse().response_success(
            interaction, f"clear `{category}`", self.data["emoji_tick"]
        )


def setup(bot):
    bot.add_cog(DeleteSlashCommand(bot))
