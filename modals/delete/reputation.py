import nextcord
from databases import (
    Reputation as ReputationDatabase,
    ReputationChannel as ReputationChannelDatabase,
)
import yaml
from utils import InteractionResponse


class DeleteReputationModal(nextcord.ui.Modal):
    from utils.config import data

    def __init__(self):
        super().__init__("Delete Reputation", timeout=None)

        self.reputation_id = nextcord.ui.TextInput(
            label="Reputaton ID",
            min_length=1,
            max_length=50,
            custom_id="reputation_id",
        )
        self.add_item(self.reputation_id)

        self.confirm_reputation_id = nextcord.ui.TextInput(
            label="Confirm Reputaton ID",
            min_length=1,
            max_length=50,
            custom_id="confirm_reputation_id",
        )
        self.add_item(self.confirm_reputation_id)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await InteractionResponse().response_loading(interaction)

        if self.reputation_id.value != self.confirm_reputation_id.value:
            return await InteractionResponse().response_error(
                interaction,
                f"delete reputation",
                self.data["emoji_cross"],
                f"reputation id not match",
            )
        try:
            reputation_id = int(self.reputation_id.value)
        except:
            return await InteractionResponse().response_error(
                interaction,
                f"delete reputation",
                self.data["emoji_cross"],
                f"reputation id must be number",
            )
        if not (
            reputation := await ReputationDatabase().get(
                "reputation_id", reputation_id=int(self.reputation_id.value)
            )
        ):
            return await InteractionResponse().response_error(
                interaction,
                f"delete reputation `{self.reputation_id.value}`",
                self.data["emoji_cross"],
                f"reputatation id `{reputation_id}` not found",
            )
        message_id_user = await interaction.guild.get_channel(
            (await ReputationChannelDatabase().get("guild")).channel_id
        ).fetch_message(reputation.message_id_user)
        message_id_bot = await interaction.guild.get_channel(
            self.data["channel_reputation"]
        ).fetch_message(reputation.message_id_bot)
        if not message_id_user or not message_id_bot:
            return await InteractionResponse().response_error(
                interaction,
                f"delete reputation `{self.reputation_id.value}`",
                self.data["emoji_cross"],
                f"reputatation id `{reputation_id}` not found",
            )
        await message_id_user.delete()
        await message_id_bot.delete()
        await ReputationDatabase().delete("reputation_id", reputation_id=reputation_id)
        return await InteractionResponse().response_success(
            interaction,
            f"delete reputation id `{reputation_id}`",
            self.data["emoji_tick"],
        )
