import nextcord
from databases import Player as PlayerDatabase, Leaderboard as LeaderboardDatabase
import yaml
import nextcord
from utils import InteractionResponse


class DeletePlayerModal(nextcord.ui.Modal):
    from utils.config import data

    def __init__(self, bot):
        super().__init__("Delete Player", timeout=None)

        self.growid = nextcord.ui.TextInput(
            label="Grow ID",
            min_length=2,
            max_length=50,
            custom_id="growid",
        )
        self.add_item(self.growid)

        self.confirm_growid = nextcord.ui.TextInput(
            label="Confirm Grow ID",
            min_length=2,
            max_length=50,
            custom_id="confirm_growid",
        )
        self.add_item(self.confirm_growid)

        self.bot = bot

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await InteractionResponse().response_loading(interaction)
        if self.growid.value != self.confirm_growid.value:
            return await InteractionResponse().response_error(
                interaction,
                f"delete player",
                self.data["emoji_cross"],
                "grow id not match",
            )
        growid = self.growid.value
        if not (player := await PlayerDatabase().get("growid", growid=growid)):
            return await InteractionResponse().response_error(
                interaction,
                f"delete player",
                self.data["emoji_cross"],
                f"grow id `{growid}` not found",
            )
        await PlayerDatabase().delete("discord_id", discord_id=player.discord_id)
        await InteractionResponse().response_success(
            interaction,
            f"delete player `{growid}`",
            self.data["emoji_tick"],
        )
