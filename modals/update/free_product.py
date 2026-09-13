import nextcord
from databases import (
    Product as ProductDatabase,
    BuyGet as BuyGetDatabase,
)
import yaml
from utils import InteractionResponse


class UpdateFreeProductModal(nextcord.ui.Modal):
    from utils.config import data

    def __init__(self, code):
        super().__init__("Update Free Product", timeout=None)

        self.min_buy = nextcord.ui.TextInput(
            label="Min Buy",
            min_length=1,
            max_length=10,
            custom_id="min_buy",
            default_value="1",
        )
        self.add_item(self.min_buy)

        self.free_product = nextcord.ui.TextInput(
            label="Free Product",
            min_length=1,
            max_length=10,
            custom_id="free_product",
            default_value="1",
        )
        self.add_item(self.free_product)

        self.code = code

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await InteractionResponse().response_loading(interaction)
        try:
            min_buy = int(self.min_buy.value)
            free_product = int(self.free_product.value)
        except:
            return await InteractionResponse().response_error(
                interaction,
                f"update free product `{self.code}`",
                self.data["emoji_cross"],
                "input must be number",
            )
        if not (product := await ProductDatabase().get("code", code=self.code)):
            return await InteractionResponse().response_error(
                interaction,
                f"update free product `{self.code}`",
                self.data["emoji_cross"],
                f"product `{self.code}` not found",
            )
        await BuyGetDatabase().update(
            "product", code=self.code, min_buy=min_buy, get_product=free_product
        )
        await InteractionResponse().response_success(
            interaction,
            f"update free product `{self.code}`",
            self.data["emoji_cross"],
        )
