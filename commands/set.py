import nextcord
from nextcord.ext import commands, application_checks
from databases import (
    Deposit as DepositDatabase,
    ChannelDonate as ChannelDonateDatabase,
    Giveaway as GiveawayDatabase,
    Leaderboard as LeaderboardDatabase,
    Player as PlayerDatabase,
    Product as ProductDatabase,
    LiveStock as LiveStockDatabase,
    Maintenance as MaintenanceDatabase,
    Goodbye as GoodbyeDatabase,
    Welcome as WelcomeDatabase,
    SendLog as SendLogDatabase,
    BuyGet as BuyGetDatabase,
    Discount as DiscountDatabase,
    Purchase as PurchaseDatabase,
    RateDL as RateDlDatabase,
    ReputationChannel as ReputationChannelDatabase,
    Verification as VerificationDatabase,
    ModeLiveStockDatabase,
    QrisChannel as QrisChannelDatabase,
)
import datetime
import yaml
from utils import (
    CustomCheck,
    Misc,
    TimeConverter,
    GenerateEmbeds,
    DataNotFound,
    Webhook,
    InteractionResponse,
)
from modals import GrowID as GrowIDModal
from ui import DropdownLiveEmbed, ButtonLiveEmbed, Verification as VerificationView
from typing import Union
import asyncio
from datetime import timedelta
import random
from io import BytesIO
import os
import re


class Set(commands.Cog):
    from utils.config import data as data_content

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="set",
        description="to setup bot auto store",
    )
    @application_checks.check(CustomCheck().check_admin)
    async def set(self, interaction: nextcord.Interaction):
        pass

    @set.subcommand(description="to set log qris channel", inherit_hooks=True)
    async def qris(
        self,
        interaction: nextcord.Interaction,
        channel: Union[nextcord.TextChannel, nextcord.Thread] = nextcord.SlashOption(
            description="channel for qris log", required=False
        ),
    ):
        await InteractionResponse.response_loading(interaction)
        channel = channel or interaction.channel
        await QrisChannelDatabase().insert(interaction.guild_id, channel.id)
        await InteractionResponse().response_success(
            interaction,
            f"set qris log channel to {channel.mention}",
            self.data_content["emoji_tick"],
        )

    @set.subcommand(
        description="to set mode live stock",
        inherit_hooks=True,
        name="mode-live-stock",
    )
    async def modelivestock(
        self,
        interaction: nextcord.Interaction,
        mode: str = nextcord.SlashOption(
            description="mode live stock",
            required=True,
            choices={
                "dropdown": "dropdown",
                "button": "button",
            },
        ),
    ):
        await InteractionResponse.response_loading(interaction)
        await ModeLiveStockDatabase().insert(mode)
        await InteractionResponse().response_success(
            interaction,
            f"set mode live stock to `{mode}`",
            self.data_content["emoji_tick"],
        )

    @set.subcommand(description="to set verification role", inherit_hooks=True)
    async def verification(
        self,
        interaction: nextcord.Interaction,
        role: nextcord.Role = nextcord.SlashOption(
            description="verification role", required=True
        ),
        channel: Union[nextcord.TextChannel, nextcord.Thread] = nextcord.SlashOption(
            description="channel for verification role", required=False
        ),
    ):
        await InteractionResponse.response_loading(interaction)
        channel = channel or interaction.channel
        view = VerificationView()
        message = await channel.send(
            embed=nextcord.Embed(
                description="click button to verification",
                color=nextcord.Color.green(),
            ),
            view=view,
        )
        if verif := await VerificationDatabase().get("guild"):
            if msg := interaction.guild.get_channel(
                verif.channel_id
            ).get_partial_message(verif.message_id):
                await msg.delete()
        await VerificationDatabase().insert(
            role_id=role.id,
            message_id=message.id,
            channel_id=message.channel.id,
        )
        await InteractionResponse().response_success(
            interaction,
            f"set verification role to {message.jump_url}",
            self.data_content["emoji_tick"],
        )

    @set.subcommand(description="for user reputation commands", inherit_hooks=True)
    async def reputation(
        self,
        interaction: nextcord.Interaction,
        channel: Union[nextcord.TextChannel, nextcord.Thread] = nextcord.SlashOption(
            description="reputation log channel", required=False
        ),
    ):
        await InteractionResponse.response_loading(interaction)
        channel = channel or interaction.channel
        await ReputationChannelDatabase().insert(channel.id)
        await InteractionResponse().response_success(
            interaction,
            f"set reputation log to {channel.mention}",
            self.data_content["emoji_tick"],
        )

    @set.subcommand(description="to set rate diamond lock", inherit_hooks=True)
    async def dl(
        self,
        interaction: nextcord.Interaction,
        price: float = nextcord.SlashOption(
            description="price", required=True, min_value=1
        ),
    ):
        await InteractionResponse.response_loading(interaction)
        rupiah = await Misc().format_rupiah(price)
        await RateDlDatabase().insert(price, nextcord.utils.utcnow().timestamp())
        await InteractionResponse().response_success(
            interaction,
            f"set diamond lock to `{rupiah}`",
            self.data_content["emoji_tick"],
        )

    @set.subcommand(description="to set purchase log", inherit_hooks=True)
    async def purcashe(
        self,
        interaction: nextcord.Interaction,
        channel: Union[nextcord.TextChannel, nextcord.Thread] = nextcord.SlashOption(
            description="purchase log channel", required=False
        ),
    ):
        await InteractionResponse.response_loading(interaction)
        channel = channel or interaction.channel
        await PurchaseDatabase().insert(channel.id)
        await InteractionResponse().response_success(
            interaction,
            f"set purchase log to {channel.mention}",
            self.data_content["emoji_tick"],
        )

    @set.subcommand(
        description="to set channel proof product buyer", inherit_hooks=True
    )
    async def send(
        self,
        interaction: nextcord.Interaction,
        channel: Union[nextcord.TextChannel, nextcord.Thread] = nextcord.SlashOption(
            description="proof product log channel", required=False
        ),
    ):
        await InteractionResponse.response_loading(interaction)
        channel = channel or interaction.channel
        await SendLogDatabase().insert(channel.id)

        await InteractionResponse().response_success(
            interaction,
            f"set proof log to {channel.mention}",
            self.data_content["emoji_tick"],
        )

    @set.subcommand(
        description="to set buy minimum product to get product",
        name="free-product",
        inherit_hooks=True,
    )
    async def free_product(
        self,
        interaction: nextcord.Interaction,
        code: str = nextcord.SlashOption(description="product code", required=True),
        min_buy: int = nextcord.SlashOption(
            description="min buy", required=True, default=1, min_value=1
        ),
        get_product: int = nextcord.SlashOption(
            description="amount to get product", required=True, default=1, min_value=1
        ),
        duration: str = nextcord.SlashOption(
            description="duration of free product",
            required=False,
        ),
    ):
        await InteractionResponse.response_loading(interaction)
        if not duration or duration == "0":
            seconds = 0
        else:
            seconds = await TimeConverter().convert(interaction, duration)
        code = code.upper()
        await BuyGetDatabase().insert(
            code,
            min_buy,
            get_product,
            (
                (
                    nextcord.utils.utcnow() + datetime.timedelta(seconds=seconds)
                ).timestamp()
                if seconds
                else 0
            ),
        )

        await InteractionResponse().response_success(
            interaction,
            f"set min buy to `{min_buy}` and get product to `{get_product}` for `{code}`",
            self.data_content["emoji_tick"],
        )

    @set.subcommand(description="to set price discount", inherit_hooks=True)
    async def discount(
        self,
        interaction: nextcord.Interaction,
        code: str = nextcord.SlashOption(description="code product", required=True),
        price: int = nextcord.SlashOption(
            description="price world lock of discount", required=True, min_value=0
        ),
        duration: str = nextcord.SlashOption(
            description="duration of discount", required=False
        ),
    ):
        await InteractionResponse.response_loading(interaction)
        code = code.upper()
        if not (product := await ProductDatabase().get("code", code=code)):
            return await InteractionResponse().response_error(
                interaction,
                f"set discount to `{code}`",
                self.data_content["emoji_cross"],
                f"product `{code}` not found",
            )
        if product.price <= price:
            return await InteractionResponse().response_error(
                interaction,
                f"set discount to `{code}`",
                self.data_content["emoji_cross"],
                "price discount must be lower than price product",
            )
        if not duration or duration == "0":
            seconds = 0
        else:
            seconds = await TimeConverter().convert(interaction, duration)
        calculate_discount = await Misc().calculate_discount(product.price, price)
        await DiscountDatabase().insert(
            code,
            price,
            nextcord.utils.utcnow().timestamp(),
            (
                (
                    nextcord.utils.utcnow() + datetime.timedelta(seconds=seconds)
                ).timestamp()
                if seconds
                else 0
            ),
        )
        await InteractionResponse().response_success(
            interaction,
            f"set discount to `{calculate_discount}%` for `{code}`",
            self.data_content["emoji_tick"],
        )
        if seconds <= 300 and seconds != 0:
            await asyncio.sleep(seconds)
            await DiscountDatabase().delete("product", code=code)

    @set.subcommand(description="to set growid")
    @application_checks.check(CustomCheck().check_maintenance)
    async def growid(
        self,
        interaction: nextcord.Interaction,
    ):
        modal = GrowIDModal(self.bot)
        await interaction.response.send_modal(modal)

    @set.subcommand(description="to update balance user", inherit_hooks=True)
    async def balance(
        self,
        interaction: nextcord.Interaction,
        update: str = nextcord.SlashOption(
            description="update type",
            choices={"add": "add", "sub": "sub", "replace": "replace"},
            required=True,
        ),
        amount: int = nextcord.SlashOption(
            description="amount of balance", required=True
        ),
        member: nextcord.Member = nextcord.SlashOption(
            description="member for balance", required=False
        ),
    ):
        await InteractionResponse.response_loading(interaction)
        member = member or interaction.user
        if amount <= 0:
            return await InteractionResponse().response_error(
                interaction,
                f"update balance",
                self.data_content["emoji_cross"],
                "amount must be greater than 0",
            )
        if not (
            user_balance := await PlayerDatabase().get(
                "discord_id", discord_id=member.id
            )
        ):
            raise DataNotFound("player", member.id)
        if update == "add":
            result = await PlayerDatabase().update(
                "discord_id",
                discord_id=member.id,
                amount=user_balance.world_lock + amount,
                updated_at=nextcord.utils.utcnow().timestamp(),
            )
        elif update == "replace":
            result = await PlayerDatabase().update(
                "discord_id",
                discord_id=member.id,
                amount=amount,
                updated_at=nextcord.utils.utcnow().timestamp(),
            )
        else:
            result = await PlayerDatabase().update(
                "discord_id",
                discord_id=member.id,
                amount=user_balance.world_lock - amount,
                updated_at=nextcord.utils.utcnow().timestamp(),
            )
        await InteractionResponse().response_success(
            interaction,
            f"{update} `{amount} world lock` to `{result.growid}`",
            self.data_content["emoji_tick"],
        )
        await Webhook().update_balance(
            interaction.guild,
            "Update",
            self.data_content,
            update,
            amount,
            result.growid,
            member.mention,
            interaction.created_at,
        )

    @set.subcommand(description="to set welcome log", inherit_hooks=True)
    async def welcome(
        self,
        interaction: nextcord.Interaction,
        channel: Union[nextcord.TextChannel, nextcord.Thread] = nextcord.SlashOption(
            description="welcome log channel", required=False
        ),
    ):
        await InteractionResponse.response_loading(interaction)
        channel = channel or interaction.channel
        await WelcomeDatabase().insert(channel.id)
        await InteractionResponse().response_success(
            interaction,
            f"set welcome log to {channel.mention}",
            self.data_content["emoji_tick"],
        )

    @set.subcommand(description="to set goodbye log", inherit_hooks=True)
    async def goodbye(
        self,
        interaction: nextcord.Interaction,
        channel: Union[nextcord.TextChannel, nextcord.Thread] = nextcord.SlashOption(
            description="welcome log channel", required=False
        ),
    ):
        await InteractionResponse.response_loading(interaction)
        channel = channel or interaction.channel
        await GoodbyeDatabase().insert(channel.id)
        await InteractionResponse().response_success(
            interaction,
            f"set goodbye log to {channel.mention}",
            self.data_content["emoji_tick"],
        )

    @set.subcommand(description="to set bot is in maintenance", inherit_hooks=True)
    async def maintenance(self, interaction: nextcord.Interaction):
        await InteractionResponse.response_loading(interaction)
        result = await MaintenanceDatabase().insert(
            nextcord.utils.utcnow().timestamp(), True
        )
        await InteractionResponse().response_success(
            interaction,
            f"set maintenance to `{result.status}`",
            self.data_content["emoji_tick"],
        )

    @set.subcommand(
        description="to set live stock channel", name="live-stock", inherit_hooks=True
    )
    async def live_stock(
        self,
        interaction: nextcord.Interaction,
        channel: Union[nextcord.TextChannel, nextcord.Thread] = nextcord.SlashOption(
            description="live stock log channel", required=False
        ),
    ):
        await InteractionResponse.response_loading(interaction)
        channel = channel or interaction.channel
        updated_at = nextcord.utils.utcnow().timestamp()
        if mode_live_stock := await ModeLiveStockDatabase().get("guild"):
            if mode_live_stock.mode == "dropdown":
                view = DropdownLiveEmbed(self.bot)
            else:
                view = ButtonLiveEmbed(self.bot)
        else:
            if self.data_content["mode"] == "dropdown":
                view = DropdownLiveEmbed(self.bot)
            else:
                view = ButtonLiveEmbed(self.bot)
        status = None
        try:
            channel_donation_status = interaction.guild.get_channel(
                self.data_content["channel_id_status"]
            )
            message_donation = await channel_donation_status.fetch_message(
                self.data_content["message_id_status"]
            )
        except:
            pass
        else:
            if message_donation.embeds:
                embed = message_donation.embeds[0]
                description = embed.description
                pattern = r"Status\s*:\s*(\w+)"
                match = re.search(pattern, description) if description else None
                status = match.group(1) if match else None
        status_embed = await GenerateEmbeds().generate_stats(
            interaction.guild, self.data_content["thumbnail"], status
        )
        if product := await ProductDatabase().get("all"):
            embed = await GenerateEmbeds().generate_live_stock(
                product[: self.data_content["live_stock_embed"]],
                interaction.guild,
                self.data_content["thumbnail"],
            )
            message = await channel.send(embeds=[status_embed, embed], view=view)
        else:
            embed = await GenerateEmbeds().generate_live_stock(
                [], interaction.guild, self.data_content["thumbnail"]
            )
            message = await channel.send(embeds=[status_embed, embed], view=view)
        if live_stock := await LiveStockDatabase().get("guild"):
            if msg := interaction.guild.get_channel(
                live_stock.channel_id
            ).get_partial_message(live_stock.message_id):
                await msg.delete()
        await LiveStockDatabase().insert(
            guild_id=interaction.guild_id,
            message_id=message.id,
            channel_id=message.channel.id,
            updated_at=updated_at,
        )
        await InteractionResponse().response_success(
            interaction,
            f"set live stock to {message.jump_url}",
            self.data_content["emoji_tick"],
        )

    @set.subcommand(description="to set leaderboard channel", inherit_hooks=True)
    async def leaderboard(
        self,
        interaction: nextcord.Interaction,
        channel: Union[nextcord.TextChannel, nextcord.Thread] = nextcord.SlashOption(
            description="leaderboard log channel", required=False
        ),
    ):
        await InteractionResponse.response_loading(interaction)
        channel = channel or interaction.channel
        updated_at = nextcord.utils.utcnow().timestamp()

        if mode_live_stock := await ModeLiveStockDatabase().get("guild"):
            view = (
                DropdownLiveEmbed(self.bot)
                if mode_live_stock.mode == "dropdown"
                else ButtonLiveEmbed(self.bot)
            )
        else:
            view = (
                DropdownLiveEmbed(self.bot)
                if self.data_content["mode"] == "dropdown"
                else ButtonLiveEmbed(self.bot)
            )

        if leaderboard := await PlayerDatabase().get("leaderboard"):
            embed = await GenerateEmbeds().generate_leaderboard(
                leaderboard[: self.data_content["leaderboard_embed"]],
                interaction.guild,
                self.data_content["thumbnail"],
            )
            message = await channel.send(embed=embed, view=view)
        else:
            embed = await GenerateEmbeds().generate_leaderboard(
                [], interaction.guild, self.data_content["thumbnail"]
            )
            message = await channel.send(embed=embed, view=view)

        if live_stock := await LeaderboardDatabase().get("guild"):
            channel = interaction.guild.get_channel(live_stock.channel_id)
            if channel:
                try:
                    msg = channel.get_partial_message(live_stock.message_id)
                    await msg.delete()
                except:
                    pass

        await LeaderboardDatabase().insert(
            guild_id=interaction.guild_id,
            message_id=message.id,
            channel_id=message.channel.id,
            updated_at=updated_at,
        )
        await InteractionResponse().response_success(
            interaction,
            f"set leaderboard to {message.jump_url}",
            self.data_content["emoji_tick"],
        )

    @set.subcommand(description="to set giveaway", inherit_hooks=True)
    async def giveaway(
        self,
        interaction: nextcord.Interaction,
        description: str = nextcord.SlashOption(
            description="giveaway description", required=True
        ),
        duration: str = nextcord.SlashOption(
            description="giveaway duration", required=True
        ),
        role: nextcord.Role = nextcord.SlashOption(
            description="giveaway role ping", required=True
        ),
        item: nextcord.Attachment = nextcord.SlashOption(
            description="giveaway item", required=True
        ),
        hoster: nextcord.Member = nextcord.SlashOption(
            description="giveaway hoster", required=False
        ),
        channel: Union[nextcord.TextChannel, nextcord.Thread] = nextcord.SlashOption(
            description="giveaway target channel", required=False
        ),
    ):
        await InteractionResponse.response_loading(interaction)
        channel = channel or interaction.channel
        hoster = hoster or interaction.user
        duration = await TimeConverter().convert(interaction, duration)
        created_at = nextcord.utils.utcnow()
        giveaway_end = (created_at + timedelta(seconds=duration)).timestamp()
        message = await channel.send(
            f"**giveaway start {role.mention}, host by {hoster.mention} <t:{int(created_at.timestamp())}:R>**",
            embed=nextcord.Embed(
                title="Giveaway",
                description=f"{description}",
                color=nextcord.Color.green(),
            )
            .add_field(name="Hosted By", value=f"{hoster.mention}", inline=True)
            .add_field(
                name="Giveaway ID", value=f"{created_at.timestamp()}", inline=True
            )
            .set_thumbnail(interaction.guild.icon.url)
            .set_footer(text=f"Duration: {duration}"),
        )
        await message.add_reaction("🎉")
        try:
            _, file_extension = os.path.splitext(item.filename)
        except:
            return await InteractionResponse().response_error(
                interaction,
                "set giveaway",
                self.data_content["emoji_cross"],
                "item file not found",
            )
        await InteractionResponse().response_success(
            interaction,
            f"set giveaway to {message.jump_url}",
            self.data_content["emoji_tick"],
        )
        result = await GiveawayDatabase().insert(
            message.guild.id,
            message.channel.id,
            message.id,
            role.id,
            hoster.id,
            await item.read(),
            f"{created_at}{file_extension}",
            created_at.timestamp(),
            giveaway_end,
            description,
        )
        if duration <= 300:
            await asyncio.sleep(duration)
            giveaway_message = await interaction.channel.fetch_message(message.id)
            users = [user async for user in giveaway_message.reactions[0].users()]
            users = [
                user for user in users if user != self.bot.user or user.id != hoster.id
            ]
            message_edit = await message.edit(
                f"**Giveaway Ended**",
            )
            if len(users) == 0:
                return await message.reply("**no one win, please try again later**")
            user_winner = random.choice(users)
            await message_edit.reply(f"**winner is : {user_winner.mention}**")
            file_data = BytesIO(result.item)
            file_data.seek(0)
            await user_winner.send(
                f"**congrats {user_winner.mention}, you win giveaway `{result.description}`**",
                file=nextcord.File(file_data, f"{result.file_name}"),
            )
            await GiveawayDatabase().delete("created_at", created_at=result.created_at)

    @set.subcommand(description="to set donate log channel", inherit_hooks=True)
    async def donate(
        self,
        interaction: nextcord.Interaction,
        lock: Union[nextcord.TextChannel, nextcord.Thread] = nextcord.SlashOption(
            description="lock log channel", required=True
        ),
        saweria: Union[nextcord.TextChannel, nextcord.Thread] = nextcord.SlashOption(
            description="saweria log channel", required=True
        ),
        trakteer: Union[nextcord.TextChannel, nextcord.Thread] = nextcord.SlashOption(
            description="trakteer log channel", required=True
        ),
        sociabuzz: Union[nextcord.TextChannel, nextcord.Thread] = nextcord.SlashOption(
            description="sociabuzz log channel", required=True
        ),
        transfer: Union[nextcord.TextChannel, nextcord.Thread] = nextcord.SlashOption(
            description="transfer log channel", required=True
        ),
    ):
        await InteractionResponse.response_loading(interaction)
        await ChannelDonateDatabase.insert(
            lock.id, saweria.id, trakteer.id, sociabuzz.id, transfer.id
        )
        await InteractionResponse().response_success(
            interaction,
            f"set donate balance channel",
            self.data_content["emoji_tick"],
        )

    @set.subcommand(description="set deposit", inherit_hooks=True)
    async def deposit(
        self,
        interaction: nextcord.Interaction,
        world: str = nextcord.SlashOption(
            description="world deposit growtopia", required=True
        ),
        owner: str = nextcord.SlashOption(
            description="owner deposit growtopia", required=True
        ),
        bot: str = nextcord.SlashOption(
            description="bot deposit growtopia", required=True
        ),
        trakteer: str = nextcord.SlashOption(
            description="trakteer link deposit", required=False
        ),
        saweria: str = nextcord.SlashOption(
            description="saweria link deposit", required=False
        ),
        sociabuzz: str = nextcord.SlashOption(
            description="sociabuzz link deposit", required=False
        ),
    ):
        await InteractionResponse.response_loading(interaction)
        await DepositDatabase().insert(world, owner, bot, saweria, trakteer, sociabuzz)
        await interaction.followup.send(
            embed=nextcord.Embed(
                description=f"""**successfully set deposit**
```yml
World: {world}
Owner: {owner}
Bot: {bot}```""",
                color=nextcord.Color.green(),
            ),
            ephemeral=True,
        )
        if trakteer:
            await interaction.followup.send(
                embed=nextcord.Embed(
                    description=f"**trakteer link : {trakteer}**",
                    color=nextcord.Color.green(),
                ),
                ephemeral=True,
            )
        if saweria:
            await interaction.followup.send(
                embed=nextcord.Embed(
                    description=f"**saweria link : {saweria}**",
                    color=nextcord.Color.green(),
                ),
                ephemeral=True,
            )
        if sociabuzz:
            await interaction.followup.send(
                embed=nextcord.Embed(
                    description=f"**sociabuzz link : {sociabuzz}**",
                    color=nextcord.Color.green(),
                ),
                ephemeral=True,
            )
        await InteractionResponse().response_success(
            interaction,
            f"set deposit",
            self.data_content["emoji_tick"],
        )


def setup(bot):
    bot.add_cog(Set(bot))
