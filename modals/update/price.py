import nextcord
from databases import Product as ProductDatabase
import yaml
from utils import InteractionResponse


class UpdatePriceModal(nextcord.ui.Modal):
    from utils.config import data

    def __init__(self, code):
        super().__init__("Update Price", timeout=None)

        self.price_lock = nextcord.ui.TextInput(
            label="Price", custom_id="price_lock", min_length=1, default_value="0"
        )
        self.add_item(self.price_lock)

        self.code = code

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await InteractionResponse().response_loading(interaction)
        try:
            price = int(self.price_lock.value)
        except:
            return await InteractionResponse().response_error(
                interaction,
                f"update price `{self.code}`",
                self.data["emoji_cross"],
                f"price must be number",
            )
        if price < 0:
            return await InteractionResponse().response_error(
                interaction,
                f"update price `{self.code}`",
                self.data["emoji_cross"],
                f"price must be greater than 0",
            )
        if not (product := await ProductDatabase().get("code", code=self.code)):
            return await InteractionResponse().response_error(
                interaction,
                f"update price `{self.code}`",
                self.data["emoji_cross"],
                f"product `{self.code}` not found",
            )
        await ProductDatabase().update(
            "price",
            code=self.code,
            price=price,
        )
        await InteractionResponse().response_success(
            interaction,
            f"update price `{self.code}`",
            self.data["emoji_tick"],
        )
