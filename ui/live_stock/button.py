import nextcord
from nextcord import ButtonStyle
from databases import (
    Player as PlayerDatabase,
    Deposit as DepositDatabase,
    Product as ProductDatabase,
    Stock as StockDatabase,
    Discount as DiscountDatabase,
    RateDL as RateDlDatabase,
    BuyGet as BuyGetDatabase,
    EnableDonate,
    EnableSaweria,
    EnableSociabuzz,
    EnableTrakteer,
    Maintenance as MaintenanceDatabase,
)
from modals import GrowID as GrowIDModal, Buy as BuyModal
import yaml
from ..growid import GrowID as GrowIDView
from utils import Misc, InteractionResponse
from ..paginated import Paginated as PaginatedView
from modals import Qris as QrisModal


class ButtonLiveEmbed(nextcord.ui.View):
    from utils.config import data as data_content

    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @nextcord.ui.button(
        label="Rate DL",
        style=ButtonStyle.green,
        custom_id="rate_dl",
        emoji=data_content["emoji_diamond_lock"],
    )
    async def rate_dl(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await InteractionResponse.response_loading(interaction)
        if (
            data := await MaintenanceDatabase().get(
                "maintenance", guild_id=interaction.guild.id
            )
        ) and data.status:
            return await InteractionResponse().response_error(
                interaction,
                f"show rate dl",
                self.data_content["emoji_cross"],
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
                interaction, "show rate dl", self.data_content["emoji_tick"]
            )
        await InteractionResponse.response_error(
            interaction,
            "show rate dl",
            self.data_content["emoji_cross"],
            "rate dl not available",
        )

    @nextcord.ui.button(
        label="Qris Payment",
        style=ButtonStyle.green,
        custom_id="qris_payment",
        emoji=data_content["emoji_qris"],
    )
    async def qris_payment(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        if (
            data := await MaintenanceDatabase().get(
                "maintenance", guild_id=interaction.guild.id
            )
        ) and data.status:
            await InteractionResponse.response_loading(interaction)
            return await InteractionResponse().response_error(
                interaction,
                f"create qris",
                self.data_content["emoji_cross"],
                "bot is on maintenance",
            )
        if not (rdl := await RateDlDatabase().get()):
            await InteractionResponse.response_loading(interaction)
            return await InteractionResponse().response_error(
                interaction,
                f"create qris",
                self.data_content["emoji_cross"],
                "mention admin to set rate dl",
            )
        rupiah = await Misc().format_rupiah(rdl.rate)
        modal = QrisModal(self.bot, rupiah, rdl.rate)
        await interaction.response.send_modal(modal)

    @nextcord.ui.button(
        label="Buy",
        style=ButtonStyle.green,
        custom_id="buy_button",
        emoji=data_content["emoji_buy"],
    )
    async def buy_button(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        if (
            data := await MaintenanceDatabase().get(
                "maintenance", guild_id=interaction.guild.id
            )
        ) and data.status:
            await InteractionResponse.response_loading(interaction)
            return await InteractionResponse().response_error(
                interaction,
                f"buy product",
                self.data_content["emoji_cross"],
                "bot is on maintenance",
            )
        modal = BuyModal(self.bot)
        await interaction.response.send_modal(modal)

    @nextcord.ui.button(
        label="Stock",
        style=ButtonStyle.green,
        custom_id="stock_button",
        emoji=data_content["emoji_product"],
    )
    async def stock(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await InteractionResponse.response_loading(interaction)
        if (
            data := await MaintenanceDatabase().get(
                "maintenance", guild_id=interaction.guild.id
            )
        ) and data.status:
            return await InteractionResponse().response_error(
                interaction,
                f"show stock product",
                self.data_content["emoji_cross"],
                "bot is on maintenance",
            )
        if not (product := await ProductDatabase().get("all")):
            return await InteractionResponse().response_error(
                interaction,
                f"show stock product",
                self.data_content["emoji_cross"],
                "stock not available",
            )
        paginated_arr = await Misc.split_array(
            product, self.data_content["product_page"]
        )

        embeds = []
        for idx, page in enumerate(paginated_arr):
            embed = (
                nextcord.Embed(
                    title=f"Stock Product",
                    color=nextcord.Color.green(),
                )
                .set_image(self.data_content["thumbnail"])
                .set_thumbnail(interaction.guild.icon.url)
                .set_footer(text=f"{interaction.guild.name}")
            )
            for i, value in enumerate(page):
                stock = await StockDatabase().get("code", code=value.code)
                price = f"0 {self.data_content['emoji_world_lock']}"
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
                    name=f"{self.data_content['emoji_crown']} {value.title} {self.data_content['emoji_crown']}",
                    value=f"""{self.data_content["emoji_arrow"]} Description : {value.description}
{self.data_content['emoji_arrow']} Code : {value.code} 
{self.data_content['emoji_arrow']} Min Buy : {value.min_buy}
{self.data_content['emoji_arrow']} Stock : {self.data_content['emoji_cross'] if not stock else f'{len(stock)} {self.data_content["emoji_tick"]}'}
{self.data_content['emoji_arrow']} Price : {price}
{f'''-# [ {promotion} ]
{self.data_content["emoji_line"] * 6 if not i == len(page) - 1 else ""}''' if promotion else self.data_content["emoji_line"] * 6 if not i == len(page) - 1 else ''}""",
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

    @nextcord.ui.button(
        label="Set GrowID",
        style=ButtonStyle.green,
        custom_id="growid_button",
        emoji=data_content["emoji_bot"],
    )
    async def set_growid(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        if (
            data := await MaintenanceDatabase().get(
                "maintenance", guild_id=interaction.guild.id
            )
        ) and data.status:
            await InteractionResponse.response_loading(interaction)
            return await InteractionResponse().response_error(
                interaction,
                f"set growid",
                self.data_content["emoji_cross"],
                "bot is on maintenance",
            )
        modal = GrowIDModal(self.bot)
        await interaction.response.send_modal(modal)

    @nextcord.ui.button(
        label="Balance",
        style=ButtonStyle.green,
        custom_id="balance_button",
        emoji=data_content["emoji_balance"],
    )
    async def balance(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await InteractionResponse.response_loading(interaction)
        if (
            data := await MaintenanceDatabase().get(
                "maintenance", guild_id=interaction.guild.id
            )
        ) and data.status:
            return await InteractionResponse().response_error(
                interaction,
                f"show balance",
                self.data_content["emoji_cross"],
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
                self.data_content["emoji_cross"],
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
            interaction, "show balance", self.data_content["emoji_tick"]
        )

    @nextcord.ui.button(
        label="Leaderboard",
        style=ButtonStyle.green,
        custom_id="leaderboard_button",
        emoji=data_content["emoji_leaderboard"],
    )
    async def leaderboard(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):

        await InteractionResponse.response_loading(interaction)
        if (
            data := await MaintenanceDatabase().get(
                "maintenance", guild_id=interaction.guild.id
            )
        ) and data.status:
            return await InteractionResponse().response_error(
                interaction,
                f"show leaderboard",
                self.data_content["emoji_cross"],
                "bot is on maintenance",
            )
        if not (product := await PlayerDatabase().get("leaderboard")):
            return await InteractionResponse().response_error(
                interaction,
                f"show leaderboard",
                self.data_content["emoji_cross"],
                "leaderboard not available",
            )
        paginated_arr = await Misc.split_array(
            product, self.data_content["leaderboard_page"]
        )

        embeds = []
        for idx, page in enumerate(paginated_arr):
            embed = (
                nextcord.Embed(
                    title=f"Leaderboard",
                    color=nextcord.Color.green(),
                )
                .set_image(self.data_content["thumbnail"])
                .set_thumbnail(interaction.guild.icon.url)
                .set_footer(text=f"{interaction.guild.name}")
            )
            for i, value in enumerate(page):
                balance = f"0 {self.data_content['emoji_world_lock']}"
                if value.world_lock > 0:
                    balance = f"{await Misc.format_price(value.world_lock)} "
                embed.add_field(
                    name=f"""{self.data_content['emoji_crown']} {value.growid} {self.data_content['emoji_crown']}""",
                    value=f"""{self.data_content['emoji_arrow']} Total Buy : {value.total_buy}
{self.data_content['emoji_arrow']} World Lock : {balance}
{f'{self.data_content["emoji_line"] * 6}' if i == 9 else ''}""",
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

    @nextcord.ui.button(
        label="Deposit",
        style=ButtonStyle.green,
        custom_id="deposit_button",
        emoji=data_content["emoji_coin"],
    )
    async def deposit(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await InteractionResponse.response_loading(interaction)
        if (
            data := await MaintenanceDatabase().get(
                "maintenance", guild_id=interaction.guild.id
            )
        ) and data.status:
            return await InteractionResponse().response_error(
                interaction,
                f"show deposit",
                self.data_content["emoji_cross"],
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
                        ).set_image(self.data_content["thumbnail"]),
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
                        ).set_image(self.data_content["thumbnail"]),
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
                        ).set_image(self.data_content["thumbnail"]),
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
                        ).set_image(self.data_content["thumbnail"]),
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
                self.data_content["emoji_tick"],
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
            self.data_content["emoji_tick"],
            "deposit not available",
            view=view,
        )

    @nextcord.ui.button(
        label="How To Buy",
        style=ButtonStyle.green,
        custom_id="how_to_buy_button",
        emoji=data_content["emoji_question"],
    )
    async def how_to_buy(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):

        await InteractionResponse.response_loading(interaction)
        if (
            data := await MaintenanceDatabase().get(
                "maintenance", guild_id=interaction.guild.id
            )
        ) and data.status:
            return await InteractionResponse().response_error(
                interaction,
                f"show leaderboard",
                self.data_content["emoji_cross"],
                "bot is on maintenance",
            )
        await interaction.followup.send(
            embed=nextcord.Embed(
                title=f"How To Buy Product At {interaction.guild.name}",
                color=nextcord.Color.green(),
                description=f"""{self.data_content['emoji_arrow']} first make sure you have registered growid
{self.data_content['emoji_arrow']} then click deposit then donate wls
{self.data_content['emoji_arrow']} then please press the buy or use / buy button
{self.data_content['emoji_arrow']} then enter the product code, number of products, and payment category
{self.data_content['emoji_arrow']} then please check dm if the purchase is successful
{self.data_content['emoji_arrow']} the item will be sent via dm bot

**note :**
{self.data_content['emoji_arrow']} for payment only 2 are available, lock (growtopia currency) and rupiah (Indonesian currency)
{self.data_content['emoji_arrow']} make sure your dm settings are not private
{self.data_content['emoji_arrow']} no rep = no warranty
""",
            )
            .set_image(self.data_content["thumbnail"])
            .set_thumbnail(interaction.guild.icon.url),
            ephemeral=True,
        )
        await InteractionResponse.response_success(
            interaction,
            "show how to buy",
            self.data_content["emoji_tick"],
        )

    async def disable_buttons(self):
        for child in self.children:
            if isinstance(child, nextcord.ui.Button):
                child.disabled = True
                child.style = ButtonStyle.gray
