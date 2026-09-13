import nextcord
from nextcord.ext import commands, application_checks
import yaml
from databases import (
    Product as ProductDatabase,
    Stock as StockDatabase,
    Player as PlayerDatabase,
    Discount as DiscountDatabase,
    BuyGet as BuyGetDatabase,
    SendLog as SendLogDatabase,
)
from utils import DataNotFound, CustomCheck, Misc, InteractionResponse
from modals import Buy as BuyModal
from io import StringIO, BytesIO
from ui import Paginated as PaginatedView


class ProductSlashCommand(commands.Cog):
    from utils.config import data

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="to show all product")
    @application_checks.check(CustomCheck().check_maintenance)
    async def stock(
        self,
        interaction: nextcord.Interaction,
        per_page: int = nextcord.SlashOption(
            description="number of items per page",
            required=False,
            min_value=1,
            default=2,
        ),
    ):
        await InteractionResponse.response_loading(interaction)
        if not (product := await ProductDatabase().get("all")):
            raise DataNotFound("stock", None)
        paginated_arr = await Misc.split_array(product, per_page)

        embeds = []
        for idx, page in enumerate(paginated_arr):
            embed = (
                nextcord.Embed(
                    title=f"Stock Product",
                    color=nextcord.Color.green(),
                )
                .set_image(self.data["thumbnail"])
                .set_thumbnail(interaction.guild.icon.url)
                .set_footer(text=f"{interaction.guild.name}")
            )
            for i, value in enumerate(page):
                stock = await StockDatabase().get("code", code=value.code)
                price = f"0 {self.data['emoji_world_lock']}"
                promotion = None
                if pm := await BuyGetDatabase().get("code", code=value.code):
                    promotion = f"Buy {pm.min_buy} Get {pm.get_product}"
                if value.price and value.price != 0:
                    if disc := await DiscountDatabase().get(
                        "product", code=value.code.upper()
                    ):
                        if disc.price:
                            calculate_discount = await Misc.calculate_discount(
                                value.price, disc.price
                            )
                            price = f"{await Misc.format_price(disc.price)} `Discount ({calculate_discount}%)`"
                    else:
                        price = f"{await Misc.format_price(value.price)}"
                embed.add_field(
                    name=f"{self.data['emoji_crown']} {value.title} {self.data['emoji_crown']}",
                    value=f"""{self.data["emoji_arrow"]} Description : {value.description}
{self.data['emoji_arrow']} Code : {value.code}
{self.data['emoji_arrow']} Min Buy : {value.min_buy}
{self.data['emoji_arrow']} Stock : {self.data['emoji_cross'] if not stock else f'{len(stock)} {self.data["emoji_tick"]}'}
{self.data['emoji_arrow']} Price : {price}
{f'''-# [ {promotion} ]
{self.data["emoji_line"] * 6 if not idx == len(page) - 1 else ""}''' if promotion else self.data["emoji_line"] * 6 if not i == len(page) - 1 else ''}""",
                    inline=False,
                )
            embeds.append(embed)

        if embeds:
            view = PaginatedView(embeds)
            await view.disable_buttons()
            await interaction.edit_original_message(
                embed=embeds[0],
                view=view,
            )

    @nextcord.slash_command(description="to send a product")
    @application_checks.check(CustomCheck().check_maintenance)
    @application_checks.check(CustomCheck().check_admin)
    async def send(
        self,
        interaction: nextcord.Interaction,
        code: str = nextcord.SlashOption(description="code product", required=True),
        amount: int = nextcord.SlashOption(
            description="amount product", required=False, min_value=1, default=1
        ),
        member: nextcord.Member = nextcord.SlashOption(
            description="target member", required=False
        ),
    ):
        await InteractionResponse.response_loading(interaction)
        created_at = nextcord.utils.utcnow()
        code = code.upper()
        member = member or interaction.user
        if not (proof_send := await SendLogDatabase().get("guild")):
            return await InteractionResponse().response_error(
                interaction,
                f"buy product `{code}`",
                self.data["emoji_cross"],
                f"mention admin to enable proof log",
            )

        product = await ProductDatabase().get("code", code=code)
        if not product:
            raise DataNotFound("product", code)

        user_balance = await PlayerDatabase().get("discord_id", discord_id=member.id)
        if not user_balance:
            raise DataNotFound("player", member.id)

        stock_product = await StockDatabase().get("code", code=code)
        stock = len(stock_product) if stock_product else 0
        if stock < amount:
            return await InteractionResponse().response_error(
                interaction,
                f"send product `{code}`",
                self.data["emoji_cross"],
                f"stock `{code}` not enough",
            )
        last_item = stock_product[:amount]

        file_object = None
        if product.category == "non-script":
            result_item = "\n".join(i.item for i in last_item)
            file_object = StringIO(result_item)
            file_object.seek(0)

        price_lock = f"0 {self.data['emoji_world_lock']}"
        if product.price and product.price != 0:
            if disc := await DiscountDatabase().get("product", code=product.code):
                if disc.price:
                    calculate_discount = await Misc.calculate_discount(
                        product.price, disc.price
                    )
                    price_lock = f"""{await Misc.format_price(disc.price)} 
-# [ Discount ({calculate_discount}%) ]"""
            else:
                price_lock = f"{await Misc.format_price(product.price)}"

        embed_message = nextcord.Embed(
            color=nextcord.Color.green(),
        ).set_image(self.data["thumbnail"])

        channel_proof = interaction.guild.get_channel(proof_send.channel_id)
        if not channel_proof:
            return await InteractionResponse().response_error(
                interaction,
                f"send product `{code}`",
                self.data["emoji_cross"],
                f"mention admin to enable proof log",
            )

        try:
            if product.category == "non-script" and file_object:
                embed_message.title = f"Successfully Send `{product.code}`"
                embed_message.timestamp = created_at
                embed_message.description = f"""-# {member.mention} successfully send `{product.code}`
{self.data['emoji_arrow']} Amount : {amount}
{self.data['emoji_arrow']} Price : {price_lock}"""
                await member.send(
                    embed=embed_message,
                    file=nextcord.File(file_object, f"{code}.txt"),
                )
            else:
                embed_message.title = f"Successfully Send `{product.code}`"
                embed_message.timestamp = created_at
                embed_message.description = f"""-# {member.mention} successfully send `{product.code}`
{self.data['emoji_arrow']} Amount : {amount}
{self.data['emoji_arrow']} Price : {price_lock}"""
                await member.send(embed=embed_message)
                for sc in last_item:
                    file_data = BytesIO(sc.item)
                    file_data.seek(0)
                    await member.send(file=nextcord.File(file_data, f"{sc.file_name}"))
        except nextcord.HTTPException:
            if product.category == "non-script" and file_object:
                embed_message.title = f"Failed Send `{product.code}`"
                embed_message.timestamp = created_at
                embed_message.description = f"""-# {member.mention} failed send `{product.code}`
{self.data['emoji_arrow']} Amount : {amount}
{self.data['emoji_arrow']} Price : {price_lock}"""
                file_object.seek(0)
                await channel_proof.send(
                    embed=embed_message,
                    file=nextcord.File(file_object, f"{code}.txt"),
                )
            else:
                embed_message.title = f"Failed Send `{product.code}`"
                embed_message.timestamp = created_at
                embed_message.description = f"""-# {member.mention} failed send `{product.code}`
{self.data['emoji_arrow']} Amount : {amount}
{self.data['emoji_arrow']} Price : {price_lock}"""
                await channel_proof.send(embed=embed_message)
                for sc in last_item:
                    file_data = BytesIO(sc.item)
                    file_data.seek(0)
                    await channel_proof.send(
                        file=nextcord.File(file_data, f"{sc.file_name}")
                    )
            return await InteractionResponse().response_error(
                interaction,
                f"send product `{code}`",
                self.data["emoji_cross"],
                f"htpp block",
            )
        except nextcord.Forbidden:
            if product.category == "non-script" and file_object:
                embed_message.title = f"Failed Send `{product.code}`"
                embed_message.timestamp = created_at
                embed_message.description = f"""-# {member.mention} failed send `{product.code}`
{self.data['emoji_arrow']} Amount : {amount}
{self.data['emoji_arrow']} Price : {price_lock}"""
                file_object.seek(0)
                await channel_proof.send(
                    embed=embed_message,
                    file=nextcord.File(file_object, f"{code}.txt"),
                )
            else:
                embed_message.title = f"Failed Send `{product.code}`"
                embed_message.timestamp = created_at
                embed_message.description = f"""-# {member.mention} failed send `{product.code}`
{self.data['emoji_arrow']} Amount : {amount}
{self.data['emoji_arrow']} Price : {price_lock}"""
                await channel_proof.send(embed=embed_message)
                for sc in last_item:
                    file_data = BytesIO(sc.item)
                    file_data.seek(0)
                    await channel_proof.send(
                        file=nextcord.File(file_data, f"{sc.file_name}")
                    )
            return await InteractionResponse().response_error(
                interaction,
                f"send product `{code}`",
                self.data["emoji_cross"],
                f"please public your dm",
            )
        else:
            item_delete = [i.created_at for i in last_item]
            await StockDatabase().delete("bulk_delete", item=item_delete)

        embed_message.title = f"Successfully Send `{product.code}`"
        embed_message.timestamp = created_at
        embed_message.set_thumbnail(member.display_avatar.url)
        embed_message.description = f"""-# {member.mention} successfully send `{product.code}`
{self.data['emoji_arrow']} Amount : {amount}
{self.data['emoji_arrow']} Price : {price_lock}"""
        if product.category == "non-script" and file_object:
            file_object.seek(0)
            await channel_proof.send(
                embed=embed_message,
                file=nextcord.File(file_object, f"{code}.txt"),
            )
        else:
            await channel_proof.send(embed=embed_message)
            for sc in last_item:
                file_data = BytesIO(sc.item)
                file_data.seek(0)
                await channel_proof.send(
                    file=nextcord.File(file_data, f"{sc.file_name}")
                )

        await InteractionResponse().response_success(
            interaction,
            f"send product `{code}`",
            self.data["emoji_tick"],
        )

    @nextcord.slash_command(description="to buy a product")
    @application_checks.check(CustomCheck().check_maintenance)
    async def buy(self, interaction: nextcord.Interaction):
        modal = BuyModal(self.bot)
        await interaction.response.send_modal(modal)


def setup(bot):
    bot.add_cog(ProductSlashCommand(bot))
