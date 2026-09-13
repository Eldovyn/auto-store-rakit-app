import nextcord
from databases import Product as ProductDatabase
import yaml
from utils import InteractionResponse


class DeleteProductModal(nextcord.ui.Modal):
    from utils.config import data

    def __init__(self, bot):
        super().__init__("Delete Product", timeout=None)

        self.code = nextcord.ui.TextInput(
            label="Code Product",
            min_length=2,
            max_length=50,
            custom_id="code",
        )
        self.add_item(self.code)

        self.confirm_code = nextcord.ui.TextInput(
            label="Confirm Code Product",
            min_length=2,
            max_length=50,
            custom_id="confirm_code",
        )
        self.add_item(self.confirm_code)

        self.bot = bot

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await InteractionResponse().response_loading(interaction)
        if self.code.value != self.confirm_code.value:
            return await InteractionResponse().response_error(
                interaction,
                f"delete product",
                self.data["emoji_cross"],
                "code not match",
            )
        code = self.code.value.upper()
        if not (product := await ProductDatabase().get("code", code=code)):
            return await InteractionResponse().response_error(
                interaction,
                f"delete product `{self.code}`",
                self.data["emoji_cross"],
                f"product `{code}` not found",
            )
        await ProductDatabase().delete("code", code=code)
        await InteractionResponse().response_success(
            interaction,
            f"delete product `{code}`",
            self.data["emoji_tick"],
        )
