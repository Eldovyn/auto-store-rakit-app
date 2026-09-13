import nextcord
from databases import Discount as DiscountDatabase
import yaml
from utils import InteractionResponse


class DeleteDiscountModal(nextcord.ui.Modal):
    from utils.config import data

    def __init__(self, bot):
        super().__init__("Delete Discount", timeout=None)

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
                f"delete discount",
                self.data["emoji_cross"],
                "code not match",
            )
        code = self.code.value.upper()
        try:
            await DiscountDatabase().delete("product", code=code)
        except:
            return await InteractionResponse().response_error(
                interaction,
                f"delete discount `{code}`",
                self.data["emoji_cross"],
                f"product `{code}` not found",
            )
        await InteractionResponse().response_success(
            interaction,
            f"delete discount `{code}`",
            self.data["emoji_success"],
            f"product `{code}` not found",
        )
