import nextcord
from databases import (
    Stock as StockDatabase,
    Discount as DiscountDatabase,
    BuyGet as BuyGetDatabase,
    History as HistoryDatabase,
    RateDL as RateDlDatabase,
    LiveStock as LiveStockDatabase,
    Leaderboard as LeaderboardDatabase,
)
import yaml
from utils import Misc


class GenerateEmbeds:
    from utils.config import data as data_content

    @staticmethod
    async def generate_leaderboard(data, guild, thumbnail):
        created_at = nextcord.utils.utcnow()
        if data:
            embed = (
                nextcord.Embed(
                    title=f"{GenerateEmbeds.data_content['emoji_live']} Leaderboard Player <t:{int(created_at.timestamp())}:R> {GenerateEmbeds.data_content['emoji_live']}",
                    color=nextcord.Color.green(),
                )
                .set_image(thumbnail)
                .set_thumbnail(guild.icon.url)
                .set_footer(text=f"{guild.name}")
            )
        else:
            embed = nextcord.Embed(
                title=f"{GenerateEmbeds.data_content['emoji_live']} Leaderboard Player <t:{int(created_at.timestamp())}:R> {GenerateEmbeds.data_content['emoji_live']}",
                description="**Leaderboard not available**",
                color=nextcord.Color.red(),
            ).set_footer(text=f"{guild.name}")

        for index, item in enumerate(data):
            balance = f"{await Misc.format_price(0)}"
            if item.world_lock > 0:
                balance = f"{await Misc.format_price(item.world_lock)}"

            total_buy = (
                f"{item.total_buy}{GenerateEmbeds.data_content['emoji_tick']}"
                if item.total_buy > 0
                else GenerateEmbeds.data_content["emoji_cross"]
            )

            embed.add_field(
                name=f"""{GenerateEmbeds.data_content['emoji_crown']} {item.growid} {GenerateEmbeds.data_content['emoji_crown']}""",
                value=f"""{GenerateEmbeds.data_content['emoji_arrow']} Total Buy : {total_buy}
    {GenerateEmbeds.data_content['emoji_arrow']} World Lock : {balance}
    {f'{GenerateEmbeds.data_content["emoji_line"] * 6}' if not index == len(data) - 1 else ''}""",
                inline=False,
            )

        await LeaderboardDatabase().update("player", updated_at=created_at.timestamp())
        return embed

    @staticmethod
    async def generate_live_stock(data, guild, thumbnail):
        created_at = nextcord.utils.utcnow()
        if data:
            embed = (
                nextcord.Embed(
                    title=f"{GenerateEmbeds.data_content['emoji_live']} Live Stock <t:{int(created_at.timestamp())}:R> {GenerateEmbeds.data_content['emoji_live']}",
                    color=nextcord.Color.green(),
                )
                .set_image(thumbnail)
                .set_thumbnail(guild.icon.url)
                .set_footer(text=f"{guild.name}")
            )
        else:
            embed = nextcord.Embed(
                title=f"{GenerateEmbeds.data_content['emoji_live']} Live Stock Product <t:{int(created_at.timestamp())}:R> {GenerateEmbeds.data_content['emoji_live']}",
                description="**stock not available**",
                color=nextcord.Color.red(),
            ).set_footer(text=f"{guild.name}")
        for index, item in enumerate(data):
            stock = await StockDatabase().get("code", code=item.code)
            price = f"{await Misc.format_price(0)}"
            promotion = None
            if pm := await BuyGetDatabase().get("code", code=item.code):
                promotion = f"Buy {pm.min_buy} Get {pm.get_product}"
            if item.price and item.price != 0:
                if disc := await DiscountDatabase().get(
                    "product", code=item.code.upper()
                ):
                    if disc.price:
                        calculate_discount = await Misc.calculate_discount(
                            item.price, disc.price
                        )
                        price = f"{await Misc.format_price(disc.price)} `Discount ({calculate_discount}%)`"
                else:
                    price = f"{await Misc.format_price(item.price)}"
            embed.add_field(
                name=f"{GenerateEmbeds.data_content['emoji_crown']} {item.title} {GenerateEmbeds.data_content['emoji_crown']}",
                value=f"""{GenerateEmbeds.data_content["emoji_arrow"]} Description : {item.description}
{GenerateEmbeds.data_content['emoji_arrow']} Code : {item.code}
{GenerateEmbeds.data_content['emoji_arrow']} Min Buy : {item.min_buy}
{GenerateEmbeds.data_content['emoji_arrow']} Stock : {GenerateEmbeds.data_content['emoji_cross'] if not stock else f'{len(stock)} {GenerateEmbeds.data_content["emoji_tick"]}'}
{GenerateEmbeds.data_content['emoji_arrow']} Price : {price}
{f'''-# [ {promotion} ]
{GenerateEmbeds.data_content["emoji_line"] * 6 if not index == len(data) - 1 else ""}''' if promotion else GenerateEmbeds.data_content["emoji_line"] * 6 if not index == len(data) - 1 else ''}""",
                inline=False,
            )
        await LiveStockDatabase().update("product", updated_at=created_at.timestamp())
        return embed

    @staticmethod
    async def generate_stats(guild, thumbnail, donation):
        total_history = 0
        total_buyer = 0
        if history := await HistoryDatabase().get("all"):
            total_history = len(history)
            total_buyer = len(set([i.player.growid for i in history]))
        if rate_dl := await RateDlDatabase().get():
            rupiah = await Misc.format_rupiah(rate_dl.rate)
        if donation:
            if donation == "Online":
                status = f"Online {GenerateEmbeds.data_content['emoji_online']}"
            else:
                status = f"Offline {GenerateEmbeds.data_content['emoji_offline']}"
        else:
            status = f"Offline {GenerateEmbeds.data_content['emoji_offline']}"
        embed = nextcord.Embed(
            title=f"{GenerateEmbeds.data_content['emoji_live']} {guild.name} Status {GenerateEmbeds.data_content['emoji_live']}",
            description=f"""{GenerateEmbeds.data_content['emoji_arrow']} Total Purchase : {total_history}
{GenerateEmbeds.data_content['emoji_arrow']} Total Buyer : {total_buyer}
{GenerateEmbeds.data_content['emoji_arrow']} Rate DL : {rupiah if rate_dl else 'Not Set'}
{GenerateEmbeds.data_content['emoji_arrow']} Status Donation : {status}""",
            color=nextcord.Color.green(),
        ).set_image(thumbnail)
        return embed
