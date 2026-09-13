import nextcord
from nextcord import ButtonStyle
from databases import (
    Verification as VerificationDatabase,
    EnableVerification as EnableVerificationDatabase,
)
import yaml
from utils import InteractionResponse


class Verification(nextcord.ui.View):
    from utils.config import data as data_content

    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label="verify",
        style=ButtonStyle.green,
        custom_id="verify",
        emoji=data_content["emoji_verify"],
    )
    async def verify(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await InteractionResponse.response_loading(interaction)
        if (
            status := await EnableVerificationDatabase().get("guild")
        ) and not status.status:
            return await interaction.edit_original_message(
                content="verification not available", embed=None
            )
        if data := await VerificationDatabase().get(
            "message_id", message_id=interaction.message.id
        ):
            role = interaction.guild.get_role(data.role_id)
            if role in interaction.user.roles:
                return await interaction.edit_original_message(
                    content="you are already verification", embed=None
                )
            try:
                await interaction.user.add_roles(role)
            except:
                return await interaction.edit_original_message(
                    content="you are failed verification", embed=None
                )
            return await interaction.edit_original_message(
                content=f"thank you {interaction.user.mention}, you are successfully verification",
                embed=None,
            )
