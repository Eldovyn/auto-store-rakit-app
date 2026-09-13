import nextcord
from databases import Player as PlayerDatabase, Maintenance as MaintenanceDatabase
import yaml
from utils import DuplicateData, InteractionResponse


class GrowID(nextcord.ui.Modal):
    from utils.config import data

    def __init__(self, bot):
        super().__init__("Set GrowID", timeout=None)

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
        if (
            data := await MaintenanceDatabase().get(
                "maintenance", guild_id=interaction.guild.id
            )
        ) and data.status:
            return await InteractionResponse().response_error(
                interaction,
                f"set growid",
                self.data["emoji_cross"],
                "bot is on maintenance",
            )
        if self.growid.value != self.confirm_growid.value:
            return await InteractionResponse().response_error(
                interaction,
                f"set growid",
                self.data["emoji_cross"],
                "grow id not match",
            )
        growid = self.growid.value
        created_at = nextcord.utils.utcnow().timestamp()
        try:
            await PlayerDatabase().insert(
                interaction.user.id, growid, created_at, created_at
            )
        except DuplicateData:
            return await InteractionResponse().response_error(
                interaction,
                f"set growid",
                self.data["emoji_cross"],
                f"Grow ID `{growid}` already exists",
            )
        await InteractionResponse().response_success(
            interaction,
            f"set growid `{growid}`",
            self.data["emoji_tick"],
        )
