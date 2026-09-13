import nextcord
import yaml


class InteractionResponse:
    from utils.config import data

    @staticmethod
    async def response_loading(interaction: nextcord.Interaction, ephemeral=True):
        await interaction.response.send_message(
            embed=nextcord.Embed(
                description=f"**{InteractionResponse.data['emoji_loading']} process your transaction**",
                color=nextcord.Color.yellow(),
            ),
            ephemeral=ephemeral,
        )

    @staticmethod
    async def response_success(
        interaction: nextcord.Interaction, message: str, emoji: str, view=None
    ):
        if view is not None and not isinstance(view, nextcord.ui.View):
            view = None

        await interaction.edit_original_message(
            embed=nextcord.Embed(
                description=f"""{emoji} success {message}""",
                color=nextcord.Color.green(),
            ),
            view=view,
        )

    @staticmethod
    async def response_error(
        interaction: nextcord.Interaction,
        message: str,
        emoji: str,
        error: str,
        view=None,
    ):
        if view is not None and not isinstance(view, nextcord.ui.View):
            view = None

        await interaction.edit_original_message(
            embed=nextcord.Embed(
                description=f"""{emoji} failed {message}
-# {error}""",
                color=nextcord.Color.red(),
            ),
            view=view,
        )
