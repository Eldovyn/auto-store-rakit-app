import nextcord
from nextcord.ext import commands, application_checks
import yaml
from databases import Player as PlayerDatabase
from utils import (
    Webhook,
    BalanceNotEnough,
    DataNotFound,
    CustomCheck,
    NumberNotAllow,
    InteractionResponse,
)


class PlayerSlashCommand(commands.Cog):
    from utils.config import data

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="to transfer balance user")
    @application_checks.check(CustomCheck().check_maintenance)
    async def transfer(
        self,
        interaction: nextcord.Interaction,
        amount: int = nextcord.SlashOption(
            description="amount of balance", required=True, min_value=1
        ),
        member: nextcord.Member = nextcord.SlashOption(
            description="member for balance", required=True
        ),
    ):
        await InteractionResponse.response_loading(interaction)
        if amount <= 0:
            raise NumberNotAllow(amount)
        if not (
            author_balance := await PlayerDatabase().get(
                "discord_id", discord_id=interaction.user.id
            )
        ):
            raise DataNotFound("player", interaction.user.id)
        if not (
            member_balance := await PlayerDatabase().get(
                "discord_id", discord_id=member.id
            )
        ):
            raise DataNotFound("player", member.id)
        if author_balance.world_lock < amount:
            raise BalanceNotEnough("lock", amount)
        await PlayerDatabase().update(
            "discord_id",
            discord_id=member.id,
            amount=member_balance.world_lock + amount,
            updated_at=nextcord.utils.utcnow().timestamp(),
        )
        await PlayerDatabase().update(
            "discord_id",
            discord_id=interaction.user.id,
            amount=author_balance.world_lock - amount,
            updated_at=nextcord.utils.utcnow().timestamp(),
        )
        await InteractionResponse().response_success(
            interaction,
            f"transfer `{amount} world lock` to `{member_balance.growid}`",
            self.data["emoji_tick"],
        )
        await Webhook().update_balance(
            interaction.guild,
            "Transfer",
            self.data,
            "add",
            amount,
            member_balance.growid,
            member.mention,
            interaction.created_at,
        )

    @nextcord.slash_command(description="to share information balance user")
    @application_checks.check(CustomCheck().check_maintenance)
    async def balance(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = nextcord.SlashOption(
            description="member for balance", required=False
        ),
    ):
        await InteractionResponse.response_loading(interaction)
        member = member or interaction.user
        if not (
            player := await PlayerDatabase().get("discord_id", discord_id=member.id)
        ):
            raise DataNotFound("player", member.id)
        await interaction.followup.send(
            embed=nextcord.Embed(
                description=f"""**balance growid `{player.growid}`**
```yml
World Lock: {player.world_lock}
Total Buy: {player.total_buy}```""",
                color=nextcord.Color.green(),
            ).set_thumbnail(interaction.user.display_avatar.url),
            ephemeral=True,
        )
        await InteractionResponse.response_success(
            interaction, "show balance", self.data["emoji_tick"]
        )


def setup(bot):
    bot.add_cog(PlayerSlashCommand(bot))
