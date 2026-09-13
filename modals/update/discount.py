import nextcord
from databases import Discount as DiscountDatabase, Product as ProductDatabase
import yaml
from utils import TimeConverter, Misc, InteractionResponse, DataNotFound


class UpdateDiscountModal(nextcord.ui.Modal):
    from utils.config import data

    def __init__(self, code):
        super().__init__("Update Discount", timeout=None)

        self.new_price = nextcord.ui.TextInput(
            label="Price",
            min_length=1,
            max_length=10,
            custom_id="new_price",
        )
        self.add_item(self.new_price)

        self.duration = nextcord.ui.TextInput(
            label="Duration",
            min_length=1,
            max_length=10,
            custom_id="duration",
            default_value="0",
        )
        self.add_item(self.duration)

        self.code = code

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await InteractionResponse().response_loading(interaction)
        try:
            price = int(self.new_price.value)
            duration = self.duration.value
        except:
            return await InteractionResponse().response_error(
                interaction,
                f"update discount `{self.code}`",
                self.data["emoji_cross"],
                "price must be number",
            )
        if not (product := await ProductDatabase().get("code", code=self.code)):
            return await InteractionResponse().response_error(
                interaction,
                f"update discount `{self.code}`",
                self.data["emoji_cross"],
                f"product `{self.code}` not found",
            )
        if product.price <= price:
            return await InteractionResponse().response_error(
                interaction,
                f"update discount `{self.code}`",
                self.data["emoji_cross"],
                f"discount `{price}` not allow",
            )
        try:
            if not duration or duration == "0":
                seconds = 0
            else:
                seconds = await TimeConverter().convert(interaction, duration)
        except:
            return await InteractionResponse().response_error(
                interaction,
                f"update discount `{self.code}`",
                self.data["emoji_cross"],
                f"duration `{duration}` not valid",
            )
        calculate_discount = await Misc.calculate_discount(product.price, price)
        try:
            await DiscountDatabase().update(
                "discount-duration",
                code=self.code,
                price=price,
                duration=seconds,
            )
        except:
            return await InteractionResponse().response_error(
                interaction,
                f"update discount `{self.code}`",
                self.data["emoji_cross"],
                f"discount `{self.code}` not found",
            )
        return await InteractionResponse().response_success(
            interaction,
            f"set discount `{self.code} {calculate_discount}%`",
            self.data["emoji_tick"],
        )
