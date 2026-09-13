import nextcord
from databases import Product as ProductDatabase
import yaml
from utils import InteractionResponse


class UpdateDescriptionModal(nextcord.ui.Modal):
    from utils.config import data

    def __init__(self, code):
        super().__init__("Update Description", timeout=None)

        self.new_description = nextcord.ui.TextInput(
            label="Description",
            min_length=2,
            custom_id="new_description",
        )
        self.add_item(self.new_description)

        self.confirm_description = nextcord.ui.TextInput(
            label="Confirm Description",
            min_length=2,
            custom_id="confirm_description",
        )
        self.add_item(self.confirm_description)

        self.code = code

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await InteractionResponse().response_loading(interaction)
        if self.new_description.value != self.confirm_description.value:
            return await InteractionResponse().response_error(
                interaction,
                f"update description `{self.code}`",
                self.data["emoji_cross"],
                f"description not match",
            )
        if not (product := await ProductDatabase().get("code", code=self.code)):
            return await InteractionResponse().response_error(
                interaction,
                f"update description `{self.code}`",
                self.data["emoji_cross"],
                f"product `{self.code}` not found",
            )
        await ProductDatabase().update(
            "new_description",
            code=self.code,
            new_description=self.new_description.value,
        )
        return await InteractionResponse().response_success(
            interaction,
            f"update description `{self.code}`",
            self.data["emoji_tick"],
        )
