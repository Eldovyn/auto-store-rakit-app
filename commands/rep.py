import nextcord
from nextcord.ext import commands, application_checks
from utils import Misc, CustomCheck, Webhook, ImageNotAllow, InteractionResponse
import requests
from io import BytesIO
import yaml
from databases import Reputation as ReputationDatabase


class RepSlashCommand(commands.Cog):
    from utils.config import data

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="for rep commands")
    @application_checks.check(CustomCheck().check_maintenance)
    @application_checks.check(CustomCheck().check_channel_rep)
    async def rep(
        self,
        interaction: nextcord.Interaction,
        message: str = nextcord.SlashOption(name="message", required=True),
        stars: str = nextcord.SlashOption(
            name="stars",
            required=True,
            choices=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
        ),
        image: nextcord.Attachment = nextcord.SlashOption(name="image", required=False),
    ):
        await InteractionResponse.response_loading(interaction, ephemeral=False)
        if image:
            response = requests.get(image.url)
            image_type = await Misc.get_image_type(BytesIO(response.content))
            if not image_type or image_type not in ("JPEG", "PNG"):
                raise ImageNotAllow(image_type)
            image_bytes = await image.read()
        created_at = interaction.created_at
        reputation_id = 1
        if data_rep := await ReputationDatabase().get("guild"):
            reputation_id = data_rep[-1].reputation_id + 1
        await ReputationDatabase().insert(
            reputation_id,
            message,
            stars,
            created_at.timestamp(),
            image_bytes if image else None,
            interaction.user.id,
        )
        if message_user := await interaction.edit_original_message(
            embed=nextcord.Embed(
                title=f"Reputation {interaction.guild.name} #{reputation_id}",
                color=nextcord.Color.green(),
                timestamp=created_at,
            )
            .add_field(name="Message", value=message, inline=True)
            .add_field(name="Stars", value=stars, inline=True)
            .set_thumbnail(interaction.guild.icon.url)
            .set_footer(text=f"Rep from: {interaction.user.name}")
            .set_image(url=image.url if image else None)
        ):
            if data_rep := await ReputationDatabase().get(
                "reputation_id", reputation_id=reputation_id
            ):
                await ReputationDatabase().update(
                    "add_message_id_user",
                    message_id_user=message_user.id,
                    reputation_id=reputation_id,
                )
        await Webhook().send_reputation(
            interaction.guild,
            self.data,
            f"Rep from: {interaction.user.name}",
            message,
            stars,
            created_at,
            image.url if image else None,
            reputation_id,
        )


def setup(bot):
    bot.add_cog(RepSlashCommand(bot))
