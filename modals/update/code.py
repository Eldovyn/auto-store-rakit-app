import nextcord
from databases import Product as ProductDatabase
import yaml
from utils import InteractionResponse


class UpdateCodeModal(nextcord.ui.Modal):
    from utils.config import data

    def __init__(self, code):
        super().__init__("Update Code", timeout=None)

        self.new_code = nextcord.ui.TextInput(
            label="Code",
            min_length=2,
            max_length=50,
            custom_id="new_code",
        )
        self.add_item(self.new_code)

        self.code_confirm = nextcord.ui.TextInput(
            label="Confirm Code",
            min_length=2,
            max_length=50,
            custom_id="code_confirm",
        )
        self.add_item(self.code_confirm)

        self.code = code

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await InteractionResponse().response_loading(interaction)
        if self.new_code.value != self.code_confirm.value:
            return await InteractionResponse().response_error(
                interaction,
                f"update code product `{self.code}`",
                self.data["emoji_cross"],
                "code not match",
            )
        if not (product := await ProductDatabase().get("code", code=self.code)):
            return await InteractionResponse().response_error(
                interaction,
                f"update code product `{self.code}`",
                self.data["emoji_cross"],
                f"code `{self.code}` not found",
            )
        await ProductDatabase().update(
            "code", code=self.code, new_code=self.new_code.value.upper()
        )
        await InteractionResponse().response_success(
            interaction,
            f"update code product `{self.code}`",
            self.data["emoji_tick"],
        )
