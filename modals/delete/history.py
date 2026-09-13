import nextcord
from databases import History as HistoryDatabase, Purchase as PurchaseDatabase
import yaml
from utils import InteractionResponse


class DeleteHistoryModal(nextcord.ui.Modal):
    from utils.config import data

    def __init__(self):
        super().__init__("Delete History", timeout=None)

        self.history_id = nextcord.ui.TextInput(
            label="History ID",
            min_length=1,
            max_length=50,
            custom_id="history_id",
        )
        self.add_item(self.history_id)

        self.confirm_history_id = nextcord.ui.TextInput(
            label="Confirm History ID",
            min_length=1,
            max_length=50,
            custom_id="confirm_history_id",
        )
        self.add_item(self.confirm_history_id)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await InteractionResponse().response_loading(interaction)
        if self.history_id.value != self.confirm_history_id.value:
            return await InteractionResponse().response_error(
                interaction,
                f"delete history",
                self.data["emoji_cross"],
                "history id not match",
            )
        try:
            history_id = int(self.history_id.value)
        except:
            return await InteractionResponse().response_error(
                interaction,
                f"delete history",
                self.data["emoji_cross"],
                "history id must be number",
            )
        if not (
            history := await HistoryDatabase().get(
                "history_id", history_id=int(self.history_id.value)
            )
        ):
            return await InteractionResponse().response_error(
                interaction,
                f"delete history",
                self.data["emoji_cross"],
                f"history id {history_id} not found",
            )
        await HistoryDatabase().delete("history_id", history_id=history_id)
        message = interaction.guild.get_channel(
            (await PurchaseDatabase().get("guild")).channel_id
        ).get_partial_message(history.message_id)
        await message.delete()
        await InteractionResponse().response_success(
            interaction,
            f"delete history `{history_id}`",
            self.data["emoji_tick"],
        )
