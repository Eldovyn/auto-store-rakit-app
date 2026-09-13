import nextcord
from databases import (
    Giveaway as GiveawayDatabase,
)
import yaml
from utils import InteractionResponse


class DeleteGiveawayModal(nextcord.ui.Modal):
    from utils.config import data

    def __init__(self):
        super().__init__("Delete Giveaway", timeout=None)

        self.giveaway_id = nextcord.ui.TextInput(
            label="Giveaway ID",
            min_length=1,
            max_length=50,
            custom_id="giveaway_id",
        )
        self.add_item(self.giveaway_id)

        self.confirm_giveaway_id = nextcord.ui.TextInput(
            label="Confirm Giveaway ID",
            min_length=1,
            max_length=50,
            custom_id="confirm_giveaway_id",
        )
        self.add_item(self.confirm_giveaway_id)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await InteractionResponse().response_loading(interaction)

        if self.giveaway_id.value != self.confirm_giveaway_id.value:
            return await InteractionResponse().response_error(
                interaction,
                f"delete giveaway",
                self.data["emoji_cross"],
                f"product `{self.giveaway_id.value}` not found",
            )
        try:
            giveaway_id = float(self.giveaway_id.value)
        except:
            return await InteractionResponse().response_error(
                interaction,
                f"delete giveaway",
                self.data["emoji_cross"],
                f"giveaway id must be number",
            )
        if not (
            giveaway := await GiveawayDatabase().get(
                "created_at", created_at=giveaway_id
            )
        ):
            return await InteractionResponse().response_error(
                interaction,
                f"delete giveaway",
                self.data["emoji_cross"],
                f"giveaway id must be number",
            )
        channel = nextcord.utils.get(interaction.guild.channels, id=giveaway.channel_id)
        message = await channel.fetch_message(giveaway.message_id)
        if message:
            await message.delete()
            await GiveawayDatabase().delete("created_at", created_at=giveaway_id)
        await InteractionResponse().response_success(
            interaction,
            f"delete giveaway",
            self.data["emoji_tick"],
        )
