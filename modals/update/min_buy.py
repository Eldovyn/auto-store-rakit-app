import nextcord
from databases import Product as ProductDatabase
import yaml
from utils import InteractionResponse


class UpdateMinBuyModal(nextcord.ui.Modal):
    from utils.config import data

    def __init__(self, code):
        super().__init__("Set GrowID", timeout=None)

        self.min_buy = nextcord.ui.TextInput(
            label="Min Buy",
            min_length=1,
            max_length=50,
            custom_id="min_buy",
        )
        self.add_item(self.min_buy)

        self.confirm_min_buy = nextcord.ui.TextInput(
            label="Confirm Min Buy",
            min_length=1,
            max_length=50,
            custom_id="confirm_min_buy",
        )
        self.add_item(self.confirm_min_buy)

        self.code = code

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await InteractionResponse().response_loading(interaction)

        try:
            amount = int(self.min_buy.value)
        except:
            return await InteractionResponse().response_error(
                interaction,
                f"update min buy `{self.code}`",
                self.data["emoji_cross"],
                "min buy must be number",
            )
        if self.min_buy.value != self.confirm_min_buy.value:
            return await InteractionResponse().response_error(
                interaction,
                f"update min buy `{self.code}`",
                self.data["emoji_cross"],
                "min buy not match",
            )
        if int(self.min_buy.value) <= 0:
            return await InteractionResponse().response_error(
                interaction,
                f"update min buy `{self.code}`",
                self.data["emoji_cross"],
                "min buy must be greater than 0",
            )
        if not (product := await ProductDatabase().get("code", code=self.code)):
            return await InteractionResponse().response_error(
                interaction,
                f"update min buy `{self.code}`",
                self.data["emoji_cross"],
                f"product `{self.code}` not found",
            )
        await ProductDatabase().update("min-buy", code=self.code, min_buy=amount)
        await InteractionResponse().response_success(
            interaction,
            f"update min buy `{self.code}`",
            self.data["emoji_cross"],
        )
