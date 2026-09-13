import nextcord
import asyncio
from databases import (
    Product as ProductDatabase,
    Stock as StockDatabase,
    Player as PlayerDatabase,
    Purchase as PurchaseDatabase,
    History as HistoryDatabase,
    Discount as DiscountDatabase,
    BuyGet as BuyGetDatabase,
    SendLog as SendLogDatabase,
    Maintenance as MaintenanceDatabase,
    RateDL as RateDlDatabase,
    Deposit as DepositDatabase,
)
import yaml
from io import StringIO, BytesIO
from utils import Misc, InteractionResponse

product_locks = {}


class Buy(nextcord.ui.Modal):
    from utils.config import data

    def __init__(self, bot):
        super().__init__("Buy Product", timeout=None)

        self.code = nextcord.ui.TextInput(
            label="Code",
            min_length=2,
            max_length=50,
            custom_id="code_product",
        )
        self.add_item(self.code)

        self.amount = nextcord.ui.TextInput(
            label="Amount",
            min_length=1,
            max_length=50,
            custom_id="amount",
            default_value="1",
        )
        self.add_item(self.amount)

        self.bot = bot

    async def callback(self, interaction: nextcord.Interaction) -> None:
        from ui import GrowID as GrowIDView

        await InteractionResponse().response_loading(interaction)

        product_code = self.code.value.upper()
        if (
            data := await MaintenanceDatabase().get(
                "maintenance", guild_id=interaction.guild.id
            )
        ) and data.status:
            return await InteractionResponse().response_error(
                interaction,
                f"buy product `{product_code}`",
                self.data["emoji_cross"],
                "bot is on maintenance",
            )

        if product_code in product_locks:
            return await InteractionResponse().response_error(
                interaction,
                f"buy product `{product_code}`",
                self.data["emoji_cross"],
                f"another transaction is in progress, please try again later",
            )

        product_locks[product_code] = asyncio.Lock()
        await product_locks[product_code].acquire()

        try:
            if not (channel_purchase := await PurchaseDatabase().get("guild")):
                return await InteractionResponse().response_error(
                    interaction,
                    f"buy product `{product_code}`",
                    self.data["emoji_cross"],
                    f"mention admin to enable purchase log",
                )
            if not (proof_send := await SendLogDatabase().get("guild")):
                return await InteractionResponse().response_error(
                    interaction,
                    f"buy product `{product_code}`",
                    self.data["emoji_cross"],
                    f"mention admin to enable proof log",
                )
            if not (rdl := await RateDlDatabase().get()):
                return await InteractionResponse().response_error(
                    interaction,
                    f"buy product `{product_code}`",
                    self.data["emoji_cross"],
                    "mention admin to set rate dl",
                )
            if not (data := await DepositDatabase().get("guild")):
                return await InteractionResponse().response_error(
                    interaction,
                    f"buy product `{product_code}`",
                    self.data["emoji_cross"],
                    "mention admin to set deposit",
                )
            try:
                amount = int(self.amount.value)
            except:
                return await InteractionResponse().response_error(
                    interaction,
                    f"buy product `{product_code}`",
                    self.data["emoji_cross"],
                    f"amount must be number",
                )

            member = interaction.user

            if not (
                user_balance := await PlayerDatabase().get(
                    "discord_id", discord_id=member.id
                )
            ):
                return await InteractionResponse().response_error(
                    interaction,
                    f"buy product `{product_code}`",
                    self.data["emoji_cross"],
                    f"you not have a growid",
                    view=GrowIDView(self.bot),
                )

            if not (product := await ProductDatabase().get("code", code=product_code)):
                return await InteractionResponse().response_error(
                    interaction,
                    f"buy product `{product_code}`",
                    self.data["emoji_cross"],
                    f"product `{product_code}` not found",
                )

            stock_product = await StockDatabase().get("code", code=product_code)
            stock = len(stock_product) if stock_product else 0

            if stock < amount:
                return await InteractionResponse().response_error(
                    interaction,
                    f"buy product `{product_code}`",
                    self.data["emoji_cross"],
                    f"product `{product_code}` not enough in stock",
                )

            if amount < product.min_buy:
                return await InteractionResponse().response_error(
                    interaction,
                    f"buy product `{product_code}`",
                    self.data["emoji_cross"],
                    f"minimum buy product : `{product.min_buy}`",
                )

            created_at = nextcord.utils.utcnow()
            total_price = 0
            total_price_lock = f"0 {self.data['emoji_world_lock']}"
            if product.price and product.price != 0:
                if disc := await DiscountDatabase().get("product", code=product_code):
                    if disc.price:
                        calculate_discount = await Misc.calculate_discount(
                            product.price, disc.price
                        )
                        total_price = amount * disc.price
                        total_price_lock = f"""{await Misc.format_price(total_price)} 
-# [ Discount ({calculate_discount}%) ]"""
                else:
                    total_price = amount * product.price
                    total_price_lock = f"{await Misc.format_price(total_price)}"
            else:
                return await InteractionResponse().response_error(
                    interaction,
                    f"buy product `{product_code}`",
                    self.data["emoji_cross"],
                    f"price `{product_code}` not available",
                )

            if total_price > user_balance.world_lock:
                return await InteractionResponse().response_error(
                    interaction,
                    f"buy product `{product_code}`",
                    self.data["emoji_cross"],
                    f"you not have enough balance",
                )

            last_item = stock_product[:amount]

            file_object = None
            if product.category == "non-script":
                result_item = "\n".join(i.item for i in last_item)
                file_object = StringIO(result_item)
                file_object.seek(0)

            result_balance = await PlayerDatabase().update(
                "discord_id",
                discord_id=user_balance.discord_id,
                amount=user_balance.world_lock - total_price,
                updated_at=created_at.timestamp(),
            )

            if not result_balance:
                return await InteractionResponse().response_error(
                    interaction,
                    f"buy product `{product_code}`",
                    self.data["emoji_cross"],
                    f"something went wrong, please try again later",
                )

            embed_message = nextcord.Embed(
                color=nextcord.Color.green(),
            ).set_image(self.data["thumbnail"])
            channel_proof = interaction.guild.get_channel(proof_send.channel_id)
            if not channel_proof:
                return await InteractionResponse().response_error(
                    interaction,
                    f"buy product `{product_code}`",
                    self.data["emoji_cross"],
                    f"mention admin to enable proof log",
                )
            try:
                if product.category == "non-script" and file_object:
                    embed_message.title = "Purchase Item Successfull"
                    embed_message.timestamp = created_at
                    embed_message.description = f"""-# {member.mention} successfully purchase `{product.code}`
{self.data['emoji_arrow']} Amount : {amount}
{self.data['emoji_arrow']} Total Price : {total_price_lock}"""
                    message = await member.send(
                        embed=embed_message,
                        file=nextcord.File(file_object, f"{product_code}.txt"),
                    )
                    await message.reply(
                        f"""Thank You For Purchasing `{result_balance.growid}` ({member.mention})
Your Balance Is `{result_balance.world_lock} World Lock`
-# Dont Forget To Rep"""
                    )
                else:
                    embed_message.title = "Purchase Item Successfull"
                    embed_message.timestamp = created_at
                    embed_message.description = f"""-# {member.mention} successfully purchase `{product.code}`
{self.data['emoji_arrow']} Amount : {amount}
{self.data['emoji_arrow']} Total Price : {total_price_lock}"""
                    message = await member.send(embed=embed_message)
                    await message.reply(
                        f"""Thank You For Purchasing `{result_balance.growid}` ({member.mention})
Your Balance Is `{result_balance.world_lock} World Lock`
-# Dont Forget To Rep"""
                    )
                    for sc in last_item:
                        file_data = BytesIO(sc.item)
                        file_data.seek(0)
                        await member.send(
                            file=nextcord.File(file_data, f"{sc.file_name}")
                        )
            except nextcord.HTTPException:
                await PlayerDatabase().update(
                    "discord_id",
                    discord_id=result_balance.discord_id,
                    amount=result_balance.world_lock + total_price,
                    updated_at=created_at.timestamp(),
                )
                if product.category == "non-script" and file_object:
                    embed_message.title = "Purchase Item failed"
                    embed_message.timestamp = created_at
                    embed_message.description = f"""-# {member.mention} failed send `{product.code}`
{self.data['emoji_arrow']} Amount : {amount}
{self.data['emoji_arrow']} Total Price : {total_price_lock}"""
                    file_object.seek(0)
                    await channel_proof.send(
                        embed=embed_message,
                        file=nextcord.File(file_object, f"{product_code}.txt"),
                    )
                else:
                    embed_message.title = "Purchase Item Failed"
                    embed_message.timestamp = created_at
                    embed_message.description = f"""-# {member.mention} failed send `{product.code}`
{self.data['emoji_arrow']} Amount : {amount}
{self.data['emoji_arrow']} Total Price : {total_price_lock}"""
                    await channel_proof.send(embed=embed_message)
                    for sc in last_item:
                        file_data = BytesIO(sc.item)
                        file_data.seek(0)
                        await channel_proof.send(
                            file=nextcord.File(file_data, f"{sc.file_name}")
                        )
                return await InteractionResponse().response_error(
                    interaction,
                    f"buy product `{product_code}`",
                    self.data["emoji_cross"],
                    f"http block",
                )
            except nextcord.Forbidden:
                await PlayerDatabase().update(
                    "discord_id",
                    discord_id=result_balance.discord_id,
                    amount=result_balance.world_lock + total_price,
                    updated_at=created_at.timestamp(),
                )
                if product.category == "non-script" and file_object:
                    embed_message.title = "Purchase Item failed"
                    embed_message.timestamp = created_at
                    embed_message.description = f"""-# {member.mention} failed send `{product.code}`
{self.data['emoji_arrow']} Amount : {amount}
{self.data['emoji_arrow']} Total Price : {total_price_lock}"""
                    file_object.seek(0)
                    await channel_proof.send(
                        embed=embed_message,
                        file=nextcord.File(file_object, f"{product_code}.txt"),
                    )
                else:
                    embed_message.title = "Purchase Item Failed"
                    embed_message.timestamp = created_at
                    embed_message.description = f"""-# {member.mention} failed send `{product.code}`
{self.data['emoji_arrow']} Amount : {amount}
{self.data['emoji_arrow']} Total Price : {total_price_lock}"""
                    await channel_proof.send(embed=embed_message)
                    for sc in last_item:
                        file_data = BytesIO(sc.item)
                        file_data.seek(0)
                        await channel_proof.send(
                            file=nextcord.File(file_data, f"{sc.file_name}")
                        )
                return await InteractionResponse().response_error(
                    interaction,
                    f"buy product `{product_code}`",
                    self.data["emoji_cross"],
                    f"please public your dm",
                )
            else:
                item_delete = [i.created_at for i in last_item]
                await StockDatabase().delete("bulk_delete", item=item_delete)
                await PlayerDatabase().update(
                    "total_buy",
                    discord_id=result_balance.discord_id,
                    total_buy=result_balance.total_buy + amount,
                    updated_at=created_at.timestamp(),
                )
            if product.category == "non-script" and file_object:
                embed_message.title = "Purchase Item Successfull"
                embed_message.timestamp = created_at
                embed_message.description = f"""-# {member.mention} successfully send `{product.code}`
{self.data['emoji_arrow']} Amount : {amount}
{self.data['emoji_arrow']} Total Price : {total_price_lock}"""
                file_object.seek(0)
                await channel_proof.send(
                    embed=embed_message,
                    file=nextcord.File(file_object, f"{product_code}.txt"),
                )
            else:
                embed_message.title = "Purchase Item Successfull"
                embed_message.timestamp = created_at
                embed_message.description = f"""-# {member.mention} successfully send `{product.code}`
{self.data['emoji_arrow']} Amount : {amount}
{self.data['emoji_arrow']} Total Price : {total_price_lock}"""
                await channel_proof.send(embed=embed_message)
                for sc in last_item:
                    file_data = BytesIO(sc.item)
                    file_data.seek(0)
                    await channel_proof.send(
                        file=nextcord.File(file_data, f"{sc.file_name}")
                    )

            await InteractionResponse().response_success(
                interaction,
                f"send product `{product_code}`",
                self.data["emoji_tick"],
            )

            history_id = 1
            if data_history := await HistoryDatabase().get("guild"):
                history_id = data_history[-1].history_id + 1
            purchase = interaction.guild.get_channel(channel_purchase.channel_id)
            embed_message.title = (
                f"{interaction.guild.name} | Order Number : {history_id}"
            )
            embed_message.timestamp = created_at
            embed_message.set_thumbnail(member.display_avatar.url)
            embed_message.description = f"""-# {member.mention} just ordered `{product.code}`
{self.data['emoji_arrow']} Amount : {amount}
{self.data['emoji_arrow']} Total Price : {total_price_lock}"""
            message_purchase = await purchase.send(
                embed=embed_message,
            )
            await HistoryDatabase().insert(
                history_id,
                interaction.user.id,
                product_code,
                product.category,
                [i.item for i in last_item],
                "world lock",
                product.price,
                total_price,
                created_at.timestamp(),
            )
            await HistoryDatabase().update(
                "add_message_id", history_id=history_id, message_id=message_purchase.id
            )
            free_item = None
            if pm := await BuyGetDatabase().get("code", code=product_code):
                if amount <= pm.min_buy:
                    try:
                        if stock_product := await StockDatabase().get(
                            "code", code=product_code
                        ):
                            embed_message.title = (
                                f"Buy {pm.min_buy} Get {pm.get_product}"
                            )
                            free_item = stock_product[: int(pm.get_product)]
                            if product.category == "non-script":
                                result_item = "\n".join(i.item for i in free_item)
                                file_object = StringIO()
                                file_object.write(result_item)
                                file_object.seek(0)
                                message = await member.send(
                                    embed=embed_message,
                                    file=nextcord.File(
                                        file_object, f"{product_code}.txt"
                                    ),
                                )
                                file_object.seek(0)
                                embed_message.timestamp = created_at
                                embed_message.set_thumbnail(member.display_avatar.url)
                                embed_message.description = f"""-# {member.mention} just ordered `{product.code}`
{self.data['emoji_arrow']} Amount : {amount}
{self.data['emoji_arrow']} Total Price : {total_price_lock}"""
                                await channel_proof.send(
                                    embed=embed_message,
                                    file=nextcord.File(
                                        file_object, f"{product_code}.txt"
                                    ),
                                )
                                result_promo_message = await message.reply(
                                    f"""Thank You For Purchasing `{result_balance.growid}` ({member.mention})
You Get Free `{pm.get_product} {product_code}`
-# Dont Forget To Rep"""
                                )
                            else:
                                file_object = free_item
                                for index, item in enumerate(free_item):
                                    file_data = BytesIO(item.item)
                                    file_data.seek(0)
                                    message = await member.send(
                                        file=nextcord.File(file_data, f"{sc.file_name}")
                                    )
                                    file_data.seek(0)
                                    await channel_proof.send(
                                        file=nextcord.File(file_data, f"{sc.file_name}")
                                    )
                                    if index == len(free_item) - 1:
                                        result_promo_message = await message.reply(
                                            f"""Thank You For Purchasing `{result_balance.growid}` ({member.mention})
You Get Free `{pm.get_product} {product_code}`
-# Dont Forget To Rep"""
                                        )
                                embed_message.timestamp = created_at
                                embed_message.set_thumbnail(member.display_avatar.url)
                                embed_message.description = f"""-# {member.mention} just ordered `{product.code}`
{self.data['emoji_arrow']} Amount : {amount}
{self.data['emoji_arrow']} Total Price : {total_price_lock}"""
                                await channel_proof.send(embed=embed_message)
                            if len(free_item) < pm.get_product:
                                await result_promo_message.reply(
                                    f"""DM Admin To Get `{pm.get_product - len(free_item)} {product_code}`
DM Admin To Get `{pm.get_product} {product_code}`
-# Dont Forget To Rep"""
                                )
                        else:
                            await message.reply(
                                f"""Thank You For Purchasing `{result_balance.growid}` ({member.mention})
DM Admin To Get `{pm.get_product} {product_code}`
-# Dont Forget To Rep"""
                            )
                    except:
                        embed_message.title = f"Buy {pm.min_buy} Get {pm.get_product}"
                        free_item = stock_product[: int(pm.get_product)]
                        if product.category == "non-script":
                            result_item = "\n".join(i.item for i in free_item)
                            file_object = StringIO()
                            file_object.write(result_item)
                            file_object.seek(0)
                            message = await member.send(
                                embed=embed_message,
                                file=nextcord.File(file_object, f"{product_code}.txt"),
                            )
                            file_object.seek(0)
                            embed_message.timestamp = created_at
                            embed_message.set_thumbnail(member.display_avatar.url)
                            embed_message.description = f"""-# {member.mention} failed send `{product.code}`
{self.data['emoji_arrow']} Amount : {amount}
{self.data['emoji_arrow']} Total Price : {total_price_lock}"""
                            await channel_proof.send(
                                embed=embed_message,
                                file=nextcord.File(file_object, f"{product_code}.txt"),
                            )
                        else:
                            file_object = free_item
                            for index, item in enumerate(free_item):
                                file_data = BytesIO(item.item)
                                file_data.seek(0)
                                message = await member.send(
                                    file=nextcord.File(file_data, f"{sc.file_name}")
                                )
                                file_data.seek(0)
                                await channel_proof.send(
                                    file=nextcord.File(file_data, f"{sc.file_name}")
                                )
                            embed_message.timestamp = created_at
                            embed_message.set_thumbnail(member.display_avatar.url)
                            embed_message.description = f"""-# {member.mention} failed send `{product.code}`
{self.data['emoji_arrow']} Amount : {amount}
{self.data['emoji_arrow']} Total Price : {total_price_lock}"""
                            await channel_proof.send(embed=embed_message)
                    else:
                        item_delete = [i.created_at for i in last_item]
                        await StockDatabase().delete("bulk_delete", item=item_delete)
            role_buyer = interaction.guild.get_role(self.data["role_buyer"])
            role_product = interaction.guild.get_role(product.role)
            await member.add_roles(role_buyer, role_product)

        finally:
            if product_code in product_locks:
                product_locks[product_code].release()
                del product_locks[product_code]
