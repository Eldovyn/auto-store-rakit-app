import nextcord
from databases import (
    RateDL as RateDlDatabase,
    Product as ProductDatabase,
    Stock as StockDatabase,
    BuyGet as BuyGetDatabase,
    Discount as DiscountDatabase,
    Player as PlayerDatabase,
    Deposit as DepositDatabase,
    Maintenance as MaintenanceDatabase,
)
from utils import Misc, InteractionResponse
import yaml
from modals import Buy as BuyModal, GrowID as GrowIDModal
from ..growid import GrowID as GrowIDView
from ..paginated import Paginated as PaginatedView
from databases import EnableDonate, EnableSaweria, EnableSociabuzz, EnableTrakteer


class Dropdown(nextcord.ui.Select):
    from utils.config import data

    def __init__(self, bot):
        options = [
            nextcord.SelectOption(
                label="Rate DL",
                description="to show rate diamond lock",
                emoji=self.data["emoji_diamond_lock"],
            ),
            nextcord.SelectOption(
                label="Buy",
                description="to buy a product",
                emoji=self.data["emoji_buy"],
            ),
            nextcord.SelectOption(
                label="Stock",
                description="Your favourite colour is blue",
                emoji=self.data["emoji_product"],
            ),
            nextcord.SelectOption(
                label="Set GrowID",
                emoji=self.data["emoji_bot"],
                description="to set growid",
            ),
            nextcord.SelectOption(
                label="Balance",
                emoji=self.data["emoji_balance"],
                description="to show your balance",
            ),
            nextcord.SelectOption(
                label="Leaderboard",
                description="to show leaderboard",
                emoji=self.data["emoji_leaderboard"],
            ),
            nextcord.SelectOption(
                label="Deposit",
                description="to show deposit information",
                emoji=self.data["emoji_coin"],
            ),
            nextcord.SelectOption(
                label="How To Buy",
                description="to show help",
                emoji=self.data["emoji_question"],
            ),
        ]
        super().__init__(
            placeholder=f"Click This Button To Transaction",
            min_values=1,
            max_values=1,
            options=options,
        )

        self.bot = bot

    async def callback(self, interaction: nextcord.Interaction):
        if self.values[0] == "Rate DL":
            await InteractionResponse.response_loading(interaction)
            if (
                data := await MaintenanceDatabase().get(
                    "maintenance", guild_id=interaction.guild.id
                )
            ) and data.status:
                return await InteractionResponse().response_error(
                    interaction,
                    f"show rate dl",
                    self.data["emoji_cross"],
                    "bot is on maintenance",
                )
            if rdl := await RateDlDatabase().get():
                rupiah = await Misc().format_rupiah(rdl.rate)
                await interaction.followup.send(
                    embed=nextcord.Embed(
                        description=f"**Rate DL : `{rupiah}`**",
                        color=nextcord.Color.green(),
                    ),
                    ephemeral=True,
                )
                return await InteractionResponse.response_success(
                    interaction, "show rate dl", self.data["emoji_tick"]
                )
            await InteractionResponse.response_error(
                interaction,
                "show rate dl",
                self.data["emoji_cross"],
                "rate dl not available",
            )
        elif self.values[0] == "Buy":
            if (
                data := await MaintenanceDatabase().get(
                    "maintenance", guild_id=interaction.guild.id
                )
            ) and data.status:
                await InteractionResponse.response_loading(interaction)
                return await InteractionResponse().response_error(
                    interaction,
                    f"buy product",
                    self.data["emoji_cross"],
                    "bot is on maintenance",
                )
            modal = BuyModal(self.bot)
            await interaction.response.send_modal(modal)
        elif self.values[0] == "Stock":
            await InteractionResponse.response_loading(interaction)
            if (
                data := await MaintenanceDatabase().get(
                    "maintenance", guild_id=interaction.guild.id
                )
            ) and data.status:
                return await InteractionResponse().response_error(
                    interaction,
                    f"show stock product",
                    self.data["emoji_cross"],
                    "bot is on maintenance",
                )
            if not (product := await ProductDatabase().get("all")):
                return await InteractionResponse().response_error(
                    interaction,
                    f"show stock product",
                    self.data["emoji_cross"],
                    "stock not available",
                )
            paginated_arr = await Misc.split_array(product, self.data["product_page"])

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
{self.data["emoji_line"] * 6 if not i == len(page) - 1 else ""}''' if promotion else self.data["emoji_line"] * 6 if not i == len(page) - 1 else ''}""",
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
        elif self.values[0] == "Set GrowID":
            if (
                data := await MaintenanceDatabase().get(
                    "maintenance", guild_id=interaction.guild.id
                )
            ) and data.status:
                await InteractionResponse.response_loading(interaction)
                return await InteractionResponse().response_error(
                    interaction,
                    f"set growid",
                    self.data["emoji_cross"],
                    "bot is on maintenance",
                )
            modal = GrowIDModal(self.bot)
            await interaction.response.send_modal(modal)
        elif self.values[0] == "Balance":
            await InteractionResponse.response_loading(interaction)
            if (
                data := await MaintenanceDatabase().get(
                    "maintenance", guild_id=interaction.guild.id
                )
            ) and data.status:
                return await InteractionResponse().response_error(
                    interaction,
                    f"show balance",
                    self.data["emoji_cross"],
                    "bot is on maintenance",
                )
            if not (
                player := await PlayerDatabase().get(
                    "discord_id", discord_id=interaction.user.id
                )
            ):
                view = GrowIDView(self.bot)
                return await InteractionResponse().response_error(
                    interaction,
                    f"show balance",
                    self.data["emoji_cross"],
                    "you don't have an account",
                    view=view,
                )
            await interaction.followup.send(
                embed=nextcord.Embed(
                    description=f"""**balance growid `{player.growid}`**
```yml
World Lock: {player.world_lock}
Total Buy: {player.total_buy}```""",
                    color=nextcord.Color.green(),
                ).set_thumbnail(interaction.user.display_avatar.url),
                ephemeral=True,
            )
            await InteractionResponse.response_success(
                interaction, "show balance", self.data["emoji_tick"]
            )
        elif self.values[0] == "Leaderboard":
            await InteractionResponse.response_loading(interaction)
            if (
                data := await MaintenanceDatabase().get(
                    "maintenance", guild_id=interaction.guild.id
                )
            ) and data.status:
                return await InteractionResponse().response_error(
                    interaction,
                    f"show leaderboard",
                    self.data["emoji_cross"],
                    "bot is on maintenance",
                )
            if not (product := await PlayerDatabase().get("leaderboard")):
                return await InteractionResponse().response_error(
                    interaction,
                    f"show leaderboard",
                    self.data["emoji_cross"],
                    "leaderboard not available",
                )
            paginated_arr = await Misc.split_array(
                product, self.data["leaderboard_page"]
            )

            embeds = []
            for idx, page in enumerate(paginated_arr):
                embed = (
                    nextcord.Embed(
                        title=f"Leaderboard",
                        color=nextcord.Color.green(),
                    )
                    .set_image(self.data["thumbnail"])
                    .set_thumbnail(interaction.guild.icon.url)
                    .set_footer(text=f"{interaction.guild.name}")
                )
                for i, value in enumerate(page):
                    balance = f"0 {self.data['emoji_world_lock']}"
                    if value.world_lock > 0:
                        balance = f"{await Misc.format_price(value.world_lock)} "
                    embed.add_field(
                        name=f"""{self.data['emoji_crown']} {value.growid} {self.data['emoji_crown']}""",
                        value=f"""{self.data['emoji_arrow']} Total Buy : {value.total_buy}
{self.data['emoji_arrow']} World Lock : {balance}
{f'{self.data["emoji_line"] * 6}' if i == 9 else ''}""",
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
        elif self.values[0] == "Deposit":
            await InteractionResponse.response_loading(interaction)
            if (
                data := await MaintenanceDatabase().get(
                    "maintenance", guild_id=interaction.guild.id
                )
            ) and data.status:
                return await InteractionResponse().response_error(
                    interaction,
                    f"show deposit",
                    self.data["emoji_cross"],
                    "bot is on maintenance",
                )
            view = GrowIDView(self.bot)
            if data := await DepositDatabase().get("guild"):
                if data.growtopia:
                    if not (
                        (st := await EnableDonate().get("guild")) and not st.status
                    ) or not (str := await EnableDonate().get("guild")):
                        await interaction.followup.send(
                            embed=nextcord.Embed(
                                description=f"""**World Deposit {interaction.guild.name}**
```yml
World: {data.growtopia.world}
Owner: {data.growtopia.owner}
Bot: {data.growtopia.bot}```""",
                                color=nextcord.Color.green(),
                            ).set_image(self.data["thumbnail"]),
                            ephemeral=True,
                            view=(
                                view
                                if (
                                    player := PlayerDatabase().get(
                                        "discord_id", discord_id=interaction.user.id
                                    )
                                )
                                else None
                            ),
                        )
                if data.trakteer:
                    if not (
                        (st := await EnableTrakteer().get("guild")) and not st.status
                    ) or not (str := await EnableTrakteer().get("guild")):
                        await interaction.followup.send(
                            embed=nextcord.Embed(
                                description=f"**Trakteer Link : {data.trakteer}**",
                                color=nextcord.Color.green(),
                            ).set_image(self.data["thumbnail"]),
                            ephemeral=True,
                            view=(
                                view
                                if (
                                    player := PlayerDatabase().get(
                                        "discord_id", discord_id=interaction.user.id
                                    )
                                )
                                else None
                            ),
                        )
                if data.saweria:
                    if not (
                        (st := await EnableSaweria().get("guild")) and not st.status
                    ) or not (str := await EnableSaweria().get("guild")):
                        await interaction.followup.send(
                            embed=nextcord.Embed(
                                description=f"**Saweria Link : {data.saweria}**",
                                color=nextcord.Color.green(),
                            ).set_image(self.data["thumbnail"]),
                            ephemeral=True,
                            view=(
                                view
                                if (
                                    player := PlayerDatabase().get(
                                        "discord_id", discord_id=interaction.user.id
                                    )
                                )
                                else None
                            ),
                        )
                if data.sociabuzz:
                    if not (
                        (st := await EnableSociabuzz().get("guild")) and not st.status
                    ) or not (str := await EnableSociabuzz().get("guild")):
                        await interaction.followup.send(
                            embed=nextcord.Embed(
                                description=f"**Sociabuzz Link : {data.sociabuzz}**",
                                color=nextcord.Color.green(),
                            ).set_image(self.data["thumbnail"]),
                            ephemeral=True,
                            view=(
                                view
                                if (
                                    player := PlayerDatabase().get(
                                        "discord_id", discord_id=interaction.user.id
                                    )
                                )
                                else None
                            ),
                        )
                return await InteractionResponse.response_success(
                    interaction,
                    "show deposit",
                    self.data["emoji_tick"],
                    view=(
                        view
                        if (
                            player := PlayerDatabase().get(
                                "discord_id", discord_id=interaction.user.id
                            )
                        )
                        else None
                    ),
                )
            return await InteractionResponse.response_error(
                interaction,
                "show deposit",
                self.data["emoji_tick"],
                "deposit not available",
                view=view,
            )
        elif self.values[0] == "How To Buy":
            await InteractionResponse.response_loading(interaction)
            if (
                data := await MaintenanceDatabase().get(
                    "maintenance", guild_id=interaction.guild.id
                )
            ) and data.status:
                return await InteractionResponse().response_error(
                    interaction,
                    f"show leaderboard",
                    self.data["emoji_cross"],
                    "bot is on maintenance",
                )
            await interaction.followup.send(
                embed=nextcord.Embed(
                    title=f"How To Buy Product At {interaction.guild.name}",
                    color=nextcord.Color.green(),
                    description=f"""{self.data['emoji_arrow']} first make sure you have registered growid
{self.data['emoji_arrow']} then click deposit then donate wls
{self.data['emoji_arrow']} then please press the buy or use / buy button
{self.data['emoji_arrow']} then enter the product code, number of products, and payment category
{self.data['emoji_arrow']} then please check dm if the purchase is successful
{self.data['emoji_arrow']} the item will be sent via dm bot

**note :**
{self.data['emoji_arrow']} for payment only 2 are available, lock (growtopia currency) and rupiah (Indonesian currency)
{self.data['emoji_arrow']} make sure your dm settings are not private
{self.data['emoji_arrow']} no rep = no warranty
""",
                )
                .set_image(self.data["thumbnail"])
                .set_thumbnail(interaction.guild.icon.url),
                ephemeral=True,
            )
            await InteractionResponse.response_success(
                interaction,
                "show how to buy",
                self.data["emoji_tick"],
            )


class DropdownLiveEmbed(nextcord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.dropdown = Dropdown(bot)
        self.add_item(self.dropdown)

    async def disable_dropdown(self):
        self.dropdown.disabled = True
