import nextcord
import yaml
from databases import (
    Qris as QrisDatabase,
    RateDL as RateDlDatabase,
    QrisChannel as QrisChannelDatabase,
    Player as PlayerDatabase,
    EnableQris as EnableQrisDatabase,
    Maintenance as MaintenanceDatabase,
)
from utils import QrisPayment, Misc, DataNotFound, InteractionResponse
from mongoengine import errors


class Qris(nextcord.ui.Modal):
    from utils.config import data

    def __init__(self, bot, rupiah, rate):
        super().__init__("Qris Deposit", timeout=None)

        self.rupiah_input = nextcord.ui.TextInput(
            label=f"Rupiah ({rupiah})",
            min_length=2,
            max_length=50,
            default_value=rate,
            custom_id="rupiah",
        )
        self.add_item(self.rupiah_input)

        self.rupiah_confirm = nextcord.ui.TextInput(
            label=f"Confirm Rupiah ({rupiah})",
            min_length=2,
            max_length=50,
            default_value=rate,
            custom_id="rupiah_confirm",
        )
        self.add_item(self.rupiah_confirm)

        self.bot = bot
        self.rupiah = rupiah
        self.rate = rate

        self.qris_payment = QrisPayment()

    async def callback(self, interaction: nextcord.Interaction) -> None:
        from ui import QrisPayment as QrisPaymentView

        await InteractionResponse().response_loading(interaction)
        if (
            data := await MaintenanceDatabase().get(
                "maintenance", guild_id=interaction.guild.id
            )
        ) and data.status:
            return await InteractionResponse().response_error(
                interaction,
                f"create qris",
                self.data["emoji_cross"],
                "bot is on maintenance",
            )
        if (disable := await EnableQrisDatabase().get("guild")) and not disable.status:
            return await InteractionResponse().response_error(
                interaction,
                f"create qris",
                self.data["emoji_cross"],
                "qris payment is disable/not available",
            )
        if not (ch := await QrisChannelDatabase().get("guild")) or not (
            qris_log := interaction.guild.get_channel(ch.channel_id)
        ):
            return await InteractionResponse().response_error(
                interaction,
                f"create qris",
                self.data["emoji_cross"],
                "mention admin to set qris channel",
            )
        if self.rupiah_input.value != self.rupiah_confirm.value:
            return await InteractionResponse().response_error(
                interaction,
                f"create qris",
                self.data["emoji_cross"],
                "rupiah not match",
            )
        if not (rdl := await RateDlDatabase().get()):
            return await InteractionResponse().response_error(
                interaction,
                f"create qris",
                self.data["emoji_cross"],
                "mention admin to set rate dl",
            )
        try:
            amount = int(self.rupiah_input.value)
        except:
            return await InteractionResponse().response_error(
                interaction,
                f"create qris",
                self.data["emoji_cross"],
                "amount must be number",
            )

        if amount <= 0:
            return await InteractionResponse().response_error(
                interaction,
                f"create qris",
                self.data["emoji_cross"],
                "amount must be greater than 0",
            )
        world_lock = await Misc().calculate_rate_dl(rdl.rate, amount)
        if world_lock <= 0:
            return await InteractionResponse().response_error(
                interaction,
                f"create qris",
                self.data["emoji_cross"],
                "the top up amount you entered is too small",
            )
        unique_code = await self.qris_payment.create_code()
        created_at = nextcord.utils.utcnow().timestamp()
        rupiah = await Misc().format_rupiah(amount)
        try:
            await QrisDatabase().insert(
                interaction.user.id, unique_code, amount, created_at
            )
        except DataNotFound:
            growid = await Misc().create_growid()
            player = await PlayerDatabase().insert(
                interaction.user.id, growid, created_at, created_at
            )
            await QrisDatabase().insert(
                player.discord_id, unique_code, amount, created_at
            )
        except errors.NotUniqueError:
            result = await QrisDatabase().get(
                "discord_id", discord_id=interaction.user.id
            )
            await QrisDatabase().delete("unique_code", unique_code=result.unique_code)
            await QrisDatabase().insert(
                interaction.user.id, unique_code, amount, created_at
            )
            user = await self.bot.fetch_user(interaction.user.id)
            dm_channel = await user.create_dm()
            if result.message_id:
                message = await dm_channel.fetch_message(result.message_id)
                if message.embeds:
                    embed = message.embeds[0]
                    if embed:
                        rupiah = await Misc().format_rupiah(result.amount)
                        embed.description = f"""{result.unique_code} <t:{int(result.created_at)}:R>

{self.data['emoji_arrow']} Amount : {rupiah}
{self.data['emoji_arrow']} World Lock : {world_lock}
{self.data['emoji_arrow']} Status : Canceled"""
                        embed.set_image(url=None)
                        await message.edit(embed=embed, view=None)
                        if not (ch := await QrisChannelDatabase().get("guild")):
                            return await interaction.edit_original_message(
                                embed=nextcord.Embed(
                                    description=f"**failed to cancel qris**",
                                    color=nextcord.Color.red(),
                                ),
                            )
                        if not (channel := await self.bot.fetch_channel(ch.channel_id)):
                            return await interaction.edit_original_message(
                                embed=nextcord.Embed(
                                    description=f"**failed to cancel qris**",
                                    color=nextcord.Color.red(),
                                ),
                            )
                        await channel.send(
                            embed=nextcord.Embed(
                                title=f"Qris Payment Information",
                                description=f"""{result.unique_code} <t:{int(result.created_at)}:R>

{self.data['emoji_arrow']} Status : Canceled
{self.data['emoji_arrow']} Amount : {rupiah}
{self.data['emoji_arrow']} User : {interaction.user.mention}""",
                                color=nextcord.Color.green(),
                            ).set_image(self.data["thumbnail"]),
                        )
        api_qris = await self.qris_payment.create_qris(unique_code, f"{amount}")
        if api_qris["status_code"] != "201":
            await QrisDatabase().delete("unique_code", unique_code=unique_code)
            return await InteractionResponse().response_error(
                interaction,
                f"create qris",
                self.data["emoji_cross"],
                "failed send qris payment to your dm",
            )
        message = await interaction.user.send(
            embed=nextcord.Embed(
                title=f"Qris Payment Information",
                description=f"""{api_qris['order_id']} <t:{int(created_at)}:R>

{self.data['emoji_arrow']} Amount : {rupiah}
{self.data['emoji_arrow']} World Lock : {world_lock} world lock
{self.data['emoji_arrow']} Status : Pending""",
                color=nextcord.Color.green(),
            )
            .set_image(api_qris["actions"][0]["url"])
            .set_footer(text=f"{interaction.guild.name}"),
            view=QrisPaymentView(self.bot),
        )
        await QrisDatabase().update(
            "message_id", message_id=message.id, unique_code=unique_code
        )
        await InteractionResponse().response_success(
            interaction,
            f"send qris payment to your dm",
            self.data["emoji_tick"],
        )
        await qris_log.send(
            embed=nextcord.Embed(
                title=f"Qris Payment Information",
                description=f"""{api_qris['order_id']} <t:{int(created_at)}:R>

{self.data['emoji_arrow']} Status : Create
{self.data['emoji_arrow']} Amount : {rupiah}
{self.data['emoji_arrow']} User : {interaction.user.mention}""",
                color=nextcord.Color.green(),
            ).set_image(self.data["thumbnail"])
        )
