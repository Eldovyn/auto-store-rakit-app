import nextcord
from databases import BuyGet as BuyGetDatabase
import yaml
from utils import InteractionResponse


class DeleteBuyGetModal(nextcord.ui.Modal):
    from utils.config import data

    def __init__(self):
        super().__init__("Delete Free Product", timeout=None)

        self.code = nextcord.ui.TextInput(
            label="Code",
            min_length=1,
            max_length=50,
            custom_id="code",
        )
        self.add_item(self.code)

        self.confirm_code = nextcord.ui.TextInput(
            label="Confirm Code",
            min_length=1,
            max_length=50,
            custom_id="confirm_code",
        )
        self.add_item(self.confirm_code)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await InteractionResponse().response_loading(interaction)

        if self.code.value != self.confirm_code.value:
            return await InteractionResponse().response_error(
                interaction,
                f"delete free product",
                self.data["emoji_cross"],
                "code not match",
            )
        code = self.code.value.upper()
        if not (prod := await BuyGetDatabase().get("code", code=code)):
            return await InteractionResponse().response_error(
                interaction,
                f"delete free product `{self.code}`",
                self.data["emoji_cross"],
                f"product `{code}` not found",
            )
        await BuyGetDatabase().delete("product", code=code)
        await InteractionResponse().response_success(
            interaction,
            f"delete free product `{code}`",
            self.data["emoji_tick"],
        )
