import nextcord
from nextcord import ButtonStyle
from modals import GrowID as GrowIDModal
import yaml


class GrowID(nextcord.ui.View):
    from utils.config import data as data_content

    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @nextcord.ui.button(
        label="Set GrowID",
        style=ButtonStyle.green,
        custom_id="growid_button_set_error",
        emoji=data_content["emoji_bot"],
    )
    async def set_growid(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        modal = GrowIDModal(self.bot)
        await interaction.response.send_modal(modal)
