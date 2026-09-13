import nextcord
from nextcord import ButtonStyle
from databases import (
    Qris as QrisDatabase,
    QrisChannel as QrisChannelDatabase,
    RateDL as RateDlDatabase,
)
import yaml
from utils import QrisPayment as QP, Misc, InteractionResponse


class QrisPayment(nextcord.ui.View):
    from utils.config import data as data_content

    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @nextcord.ui.button(
        label="Cancel Qris",
        style=ButtonStyle.green,
        custom_id="cancel_qris",
        emoji=data_content["emoji_cross"],
    )
    async def cancel_qris(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await InteractionResponse.response_loading(interaction)

        if not (rdl := await RateDlDatabase().get()):
            return await interaction.edit_original_message(
                embed=nextcord.Embed(
                    description="**mention admin to set rate diamond lock**",
                    color=nextcord.Color.red(),
                ),
            )
        if not (
            qris := await QrisDatabase().get(
                "discord_id", discord_id=interaction.user.id
            )
        ):
            return await interaction.edit_original_message(
                embed=nextcord.Embed(
                    description=f"**failed to cancel qris**",
                    color=nextcord.Color.red(),
                ),
            )
        status_qris = await QP().check_status(qris.unique_code)
        if not status_qris["status_code"] == "201":
            return await interaction.edit_original_message(
                embed=nextcord.Embed(
                    description=f"**failed to cancel qris**",
                    color=nextcord.Color.red(),
                ),
            )
        result = await QP().cancel_qris(qris.unique_code)
        if not result["status_code"] == "200":
            return await interaction.edit_original_message(
                embed=nextcord.Embed(
                    description=f"**failed to cancel qris**",
                    color=nextcord.Color.red(),
                ),
            )
        await interaction.edit_original_message(
            embed=nextcord.Embed(
                description=f"**your qris has been canceled**",
                color=nextcord.Color.green(),
            ),
        )
        await QrisDatabase().delete("message_id", message_id=interaction.message.id)
        user = await self.bot.fetch_user(qris.player.discord_id)
        dm_channel = await user.create_dm()
        message = await dm_channel.fetch_message(qris.message_id)
        world_lock = await Misc().calculate_rate_dl(rdl.rate, qris.amount)
        rupiah = await Misc().format_rupiah(qris.amount)
        if not message:
            return await interaction.edit_original_message(
                embed=nextcord.Embed(
                    description=f"**failed to cancel qris**",
                    color=nextcord.Color.red(),
                ),
            )
        embed = message.embeds[0]
        if not embed:
            return await interaction.edit_original_message(
                embed=nextcord.Embed(
                    description=f"**failed to cancel qris**",
                    color=nextcord.Color.red(),
                ),
            )
        embed.description = f"""{status_qris['order_id']} <t:{int(qris.created_at)}:R>

{self.data_content['emoji_arrow']} Amount : {rupiah}
{self.data_content['emoji_arrow']} World Lock : {world_lock}
{self.data_content['emoji_arrow']} Status : {status_qris['transaction_status']}"""
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
                description=f"""{status_qris['order_id']} <t:{int(qris.created_at)}:R>

{self.data_content['emoji_arrow']} Status : Canceled
{self.data_content['emoji_arrow']} Amount : {rupiah}
{self.data_content['emoji_arrow']} User : {interaction.user.mention}""",
                color=nextcord.Color.green(),
            ).set_image(self.data_content["thumbnail"]),
        )

    @nextcord.ui.button(
        label="Status Qris",
        style=ButtonStyle.green,
        custom_id="status_qris",
        emoji=data_content["emoji_monitor"],
    )
    async def status_qris(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await InteractionResponse.response_loading(interaction)
        if not (rdl := await RateDlDatabase().get()):
            return await interaction.edit_original_message(
                embed=nextcord.Embed(
                    description="**mention admin to set rate diamond lock**",
                    color=nextcord.Color.red(),
                ),
            )
        if qris := await QrisDatabase().get(
            "message_id", message_id=interaction.message.id
        ):
            status_qris = await QP().check_status(qris.unique_code)
            if status_qris["status_code"] == "201":
                world_lock = await Misc().calculate_rate_dl(rdl.rate, qris.amount)
                rupiah = await Misc().format_rupiah(qris.amount)
                return await interaction.edit_original_message(
                    embed=nextcord.Embed(
                        title="Qris Payment Status",
                        description=f"""{status_qris['order_id']}

{self.data_content['emoji_arrow']} Status : {status_qris['transaction_status']}
{self.data_content['emoji_arrow']} Amount : {rupiah}
{self.data_content['emoji_arrow']} World Lock : {world_lock} world lock""",
                        color=nextcord.Color.green(),
                    ),
                )
