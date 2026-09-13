import nextcord
from databases import Product as ProductDatabase
from utils import InteractionResponse
import yaml


class UpdateTitleModal(nextcord.ui.Modal):
    from utils.config import data

    def __init__(self, code):
        super().__init__("Update Title", timeout=None)

        self.new_title = nextcord.ui.TextInput(
            label="Title",
            min_length=2,
            custom_id="new_title",
        )
        self.add_item(self.new_title)

        self.confirm_title = nextcord.ui.TextInput(
            label="Confirm Title",
            min_length=2,
            custom_id="confirm_title",
        )
        self.add_item(self.confirm_title)

        self.code = code

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await InteractionResponse().response_loading(interaction)
        if self.new_title.value != self.confirm_title.value:
            return await InteractionResponse().response_error(
                interaction,
                f"update title `{self.code}`",
                self.data["emoji_cross"],
                "title not match",
            )
        if not (product := await ProductDatabase().get("code", code=self.code)):
            return await InteractionResponse().response_error(
                interaction,
                f"update title `{self.code}`",
                self.data["emoji_cross"],
                f"product `{self.code}` not found",
            )
        await ProductDatabase().update(
            "title", code=self.code, new_title=self.new_title.value
        )
        await InteractionResponse().response_success(
            interaction,
            f"update title `{self.code}`",
            self.data["emoji_tick"],
        )
