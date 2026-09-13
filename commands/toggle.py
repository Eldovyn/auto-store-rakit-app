import nextcord
from nextcord.ext import commands, application_checks
from utils import CustomCheck, InteractionResponse
from databases import (
    EnableWelcome as EnableWelcomeDatabase,
    EnableGoodbye as EnableGoodbyeDatabase,
    EnableSaweria as EnableSaweriaDatabase,
    EnableSociabuzz as EnableSociabuzzDatabase,
    EnableTrakteer as EnableTrakteerDatabase,
    EnableVerification as EnableVerificationDatabase,
    EnableDonate as EnableDonateDatabase,
    EnableTransfer as EnableTransferDatabase,
)
import yaml


class Toggle(commands.Cog):
    from utils.config import data

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="toggle",
        description="toggle to disable/enable events",
    )
    @application_checks.check(CustomCheck().check_admin)
    async def toggle(self, interaction: nextcord.Interaction):
        pass

    @toggle.subcommand(
        name="on-join",
        description="to disable/enable welcome and goodbye message",
        inherit_hooks=True,
    )
    async def on_join(
        self,
        interaction: nextcord.Interaction,
        category: str = nextcord.SlashOption(
            name="category", choices=["welcome", "goodbye"]
        ),
    ):
        await InteractionResponse.response_loading(interaction)
        if category == "welcome":
            result = await EnableWelcomeDatabase().insert()
        else:
            result = await EnableGoodbyeDatabase().insert()
        await interaction.followup.send(
            embed=nextcord.Embed(
                description=f"**{category} log status as {'`enable`' if result.status else '`disable`'}**",
                color=nextcord.Color.green(),
            ),
            ephemeral=True,
        )
        await InteractionResponse.response_success(
            interaction, "show toggle on-join log", self.data["emoji_tick"]
        )

    @toggle.subcommand(
        name="donate",
        description="to disable/enable donate message",
        inherit_hooks=True,
    )
    async def donate(
        self,
        interaction: nextcord.Interaction,
        category: str = nextcord.SlashOption(
            name="category",
            choices=["saweria", "trakteer", "sociabuzz", "world-lock", "transfer"],
        ),
    ):
        await InteractionResponse.response_loading(interaction)
        if category == "saweria":
            result = await EnableSaweriaDatabase().insert()
        elif category == "trakteer":
            result = await EnableTrakteerDatabase().insert()
        elif category == "sociabuzz":
            result = await EnableSociabuzzDatabase().insert()
        elif category == "world-lock":
            result = await EnableDonateDatabase().insert()
        else:
            result = await EnableTransferDatabase().insert()
        await interaction.followup.send(
            embed=nextcord.Embed(
                description=f"**{'transfer' if category == 'transfer' else f'{category} donate'} log status as {'`enable`' if result.status else '`disable`'}**",
                color=nextcord.Color.green(),
            ),
            ephemeral=True,
        )
        await InteractionResponse.response_success(
            interaction, "show toggle donate log", self.data["emoji_tick"]
        )

    @toggle.subcommand(
        name="verification",
        description="to disable/enable verification message",
        inherit_hooks=True,
    )
    async def verification(self, interaction: nextcord.Interaction):
        await InteractionResponse.response_loading(interaction)
        result = await EnableVerificationDatabase().insert()
        await interaction.followup.send(
            embed=nextcord.Embed(
                description=f"**verification status as {'`enable`' if result.status else '`disable`'}**",
                color=nextcord.Color.green(),
            ),
            ephemeral=True,
        )
        await InteractionResponse.response_success(
            interaction, "show toggle verification log", self.data["emoji_tick"]
        )


def setup(bot):
    bot.add_cog(Toggle(bot))
