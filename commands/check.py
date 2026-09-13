import nextcord
from nextcord.ext import commands, application_checks
from utils import CustomCheck, DataNotFound, InteractionResponse
import yaml
from databases import (
    ChannelDonate as ChannelDonateDatabase,
    Verification as VerificationDatabase,
    Welcome as WelcomeDatabase,
    Goodbye as GoodbyeDatabase,
    LiveStock as LiveStockDatabase,
    Leaderboard as LeaderboardDatabase,
    ReputationChannel as ReputationChannelDatabase,
    Purchase as PurchaseDatabase,
    Maintenance as MaintenanceDatabase,
    EnableSaweria as EnableSaweriaDatabase,
    EnableDonate as EnableDonateDatabase,
    EnableSociabuzz as EnableSociabuzzDatabase,
    EnableTrakteer as EnableTrakteerDatabase,
    EnableTransfer as EnableTransferDatabase,
    EnableWelcome as EnableWelcomeDatabase,
    EnableGoodbye as EnableGoodbyeDatabase,
    EnableVerification as EnableVerificationDatabase,
)


class CheckSlashCommands(commands.Cog):
    from utils.config import data

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="check",
        description="check setup auto store",
    )
    @application_checks.check(CustomCheck().check_admin)
    async def check_setup(self, interaction: nextcord.Interaction):
        pass

    @check_setup.subcommand(
        name="status", description="check setup auto store", inherit_hooks=True
    )
    async def status_setup(self, interaction: nextcord.Interaction):
        pass

    @status_setup.subcommand(
        description="to show status verify", inherit_hooks=True, name="verify"
    )
    @application_checks.check(CustomCheck().check_admin)
    async def verify_status(self, interaction: nextcord.Interaction):
        await InteractionResponse.response_loading(interaction)
        if result := await EnableVerificationDatabase().get("guild"):
            await interaction.followup.send(
                embed=nextcord.Embed(
                    description=f"**verification status is {'`enable`' if result.status else '`disable`'}**",
                    color=(
                        nextcord.Color.green()
                        if result.status
                        else nextcord.Color.red()
                    ),
                ),
                ephemeral=True,
            )
        else:
            await interaction.followup.send(
                embed=nextcord.Embed(
                    description=f"**verification status is {'`enable`' if result.status else '`disable`'}**",
                    color=(
                        nextcord.Color.green()
                        if result.status
                        else nextcord.Color.red()
                    ),
                ),
                ephemeral=True,
            )
        await InteractionResponse.response_success(
            interaction, "check verification status", self.data["emoji_tick"]
        )

    @status_setup.subcommand(
        name="donate",
        description="to show disable/enable donate log",
        inherit_hooks=True,
    )
    async def donate_log(
        self,
        interaction: nextcord.Interaction,
        category: str = nextcord.SlashOption(
            name="category",
            choices=["saweria", "trakteer", "sociabuzz", "world-lock", "transfer"],
        ),
    ):
        await InteractionResponse.response_loading(interaction)
        if category == "saweria":
            if result := await EnableSaweriaDatabase().get("guild"):
                await interaction.followup.send(
                    embed=nextcord.Embed(
                        description=f"**saweria donate log status is {'`enable`' if result.status else '`disable`'}**",
                        color=(
                            nextcord.Color.green()
                            if result.status
                            else nextcord.Color.red()
                        ),
                    ),
                    ephemeral=True,
                )
            else:
                await interaction.followup.send(
                    embed=nextcord.Embed(
                        description=f"**saweria donate log status is `enable`**",
                        color=nextcord.Color.green(),
                    ),
                    ephemeral=True,
                )
        elif category == "sociabuzz":
            if result := await EnableSociabuzzDatabase().get("guild"):
                await interaction.followup.send(
                    embed=nextcord.Embed(
                        description=f"**sociabuzz donate log status is {'`enable`' if result.status else '`disable`'}**",
                        color=(
                            nextcord.Color.green()
                            if result.status
                            else nextcord.Color.red()
                        ),
                    ),
                    ephemeral=True,
                )
            else:
                await interaction.followup.send(
                    embed=nextcord.Embed(
                        description=f"**sociabuzz donate log status is `enable`**",
                        color=nextcord.Color.green(),
                    ),
                    ephemeral=True,
                )
        elif category == "trakteer":
            if result := await EnableTrakteerDatabase().get("guild"):
                await interaction.followup.send(
                    embed=nextcord.Embed(
                        description=f"**trakteer donate log status is {'`enable`' if result.status else '`disable`'}**",
                        color=(
                            nextcord.Color.green()
                            if result.status
                            else nextcord.Color.red()
                        ),
                    ),
                    ephemeral=True,
                )
            else:
                await interaction.followup.send(
                    embed=nextcord.Embed(
                        description=f"**trakteer status is `enable`**",
                        color=nextcord.Color.green(),
                    ),
                    ephemeral=True,
                )
        elif category == "world-lock":
            if result := await EnableDonateDatabase().get("guild"):
                await interaction.followup.send(
                    embed=nextcord.Embed(
                        description=f"**world-lock donate log status is {'`enable`' if result.status else '`disable`'}**",
                        color=(
                            nextcord.Color.green()
                            if result.status
                            else nextcord.Color.red()
                        ),
                    ),
                    ephemeral=True,
                )
            else:
                await interaction.followup.send(
                    embed=nextcord.Embed(
                        description=f"**world-lock donate status is `enable`**",
                        color=nextcord.Color.green(),
                    ),
                    ephemeral=True,
                )
        else:
            if result := await EnableTransferDatabase().get("guild"):
                await interaction.followup.send(
                    embed=nextcord.Embed(
                        description=f"**transfer log status is {'`enable`' if result.status else '`disable`'}**",
                        color=(
                            nextcord.Color.green()
                            if result.status
                            else nextcord.Color.red()
                        ),
                    ),
                    ephemeral=True,
                )
            else:
                await interaction.followup.send(
                    embed=nextcord.Embed(
                        description=f"**transfer log status is `enable`**",
                        color=nextcord.Color.green(),
                    ),
                    ephemeral=True,
                )
        await InteractionResponse.response_success(
            interaction, "check donate log status", self.data["emoji_tick"]
        )

    @status_setup.subcommand(
        name="on-join",
        description="to show disable/enable welcome and goodbye",
        inherit_hooks=True,
    )
    async def on_join(
        self,
        interaction: nextcord.Interaction,
        category: str = nextcord.SlashOption(
            name="category",
            choices=["welcome", "goodbye"],
        ),
    ):
        await InteractionResponse.response_loading(interaction)
        if category == "welcome":
            if result := await EnableWelcomeDatabase().get("guild"):
                await interaction.followup.send(
                    embed=nextcord.Embed(
                        description=f"**welcome log status as {'`enable`' if result.status else '`disable`'}**",
                        color=(
                            nextcord.Color.green()
                            if result.status
                            else nextcord.Color.red()
                        ),
                    ),
                    ephemeral=True,
                )
            else:
                await interaction.followup.send(
                    embed=nextcord.Embed(
                        description=f"**welcome log status as `enable`**",
                        color=nextcord.Color.green(),
                    ),
                    ephemeral=True,
                )
        else:
            if result := await EnableGoodbyeDatabase().get("guild"):
                await interaction.followup.send(
                    embed=nextcord.Embed(
                        description=f"**goodbye log status as {'`enable`' if result.status else '`disable`'}**",
                        color=(
                            nextcord.Color.green()
                            if result.status
                            else nextcord.Color.red()
                        ),
                    ),
                    ephemeral=True,
                )
            else:
                await interaction.followup.send(
                    embed=nextcord.Embed(
                        description=f"**goodbye log status as `enable`**",
                        color=nextcord.Color.green(),
                    ),
                    ephemeral=True,
                )
        await InteractionResponse.response_success(
            interaction, "check welcome/goodbye log status", self.data["emoji_tick"]
        )

    @check_setup.subcommand(
        description="to show maintenance status", name="maintenance", inherit_hooks=True
    )
    async def maintenance_status(self, interaction: nextcord.Interaction):
        await InteractionResponse.response_loading(interaction)
        if result := await MaintenanceDatabase().get("all"):
            await interaction.followup.send(
                embed=nextcord.Embed(
                    description=f"**maintenance status is `{result[0].status}`**",
                    color=nextcord.Color.green(),
                ),
                ephemeral=True,
            )
        else:
            await interaction.followup.send(
                embed=nextcord.Embed(
                    description=f"**maintenance status is `{False}`**",
                    color=nextcord.Color.green(),
                ),
                ephemeral=True,
            )
        return await InteractionResponse.response_success(
            interaction, "check maintenance status", self.data["emoji_tick"]
        )

    @check_setup.subcommand(
        description="to check setup channel purchase",
        name="purchase",
        inherit_hooks=True,
    )
    async def purchase(self, interaction: nextcord.Interaction):
        await InteractionResponse.response_loading(interaction)
        if purchase_channel := await PurchaseDatabase().get("guild"):
            if channel := interaction.guild.get_channel(purchase_channel.channel_id):
                await interaction.followup.send(
                    embed=nextcord.Embed(
                        description=f"**Purchase Log Channel : {channel.mention}**",
                        color=nextcord.Color.green(),
                    ),
                    ephemeral=True,
                )
                return await InteractionResponse.response_success(
                    interaction, "check maintenance status", self.data["emoji_tick"]
                )
        raise DataNotFound("channel purchase", interaction.guild_id)

    @check_setup.subcommand(
        description="to check setup channel leaderboard",
        name="leaderboard",
        inherit_hooks=True,
    )
    async def leaderboard(self, interaction: nextcord.Interaction):
        await InteractionResponse.response_loading(interaction)
        if lb := await LeaderboardDatabase().get("guild"):
            if channel := interaction.guild.get_channel(lb.channel_id):
                if message := await channel.fetch_message(lb.message_id):
                    await interaction.followup.send(
                        embed=nextcord.Embed(
                            description=f"**Leaderboard Log Channel : {message.jump_url}**",
                            color=nextcord.Color.green(),
                        ),
                        ephemeral=True,
                    )
                    return await InteractionResponse.response_success(
                        interaction,
                        "check leaderboard channel",
                        self.data["emoji_tick"],
                    )
        raise DataNotFound("channel leaderboard", interaction.guild_id)

    @check_setup.subcommand(
        description="to check setup channel rep", name="rep", inherit_hooks=True
    )
    async def reputation(self, interaction: nextcord.Interaction):
        await InteractionResponse.response_loading(interaction)
        if reputation := await ReputationChannelDatabase().get("guild"):
            if channel := interaction.guild.get_channel(reputation.channel_id):
                await interaction.followup.send(
                    embed=nextcord.Embed(
                        description=f"**Reputation Channel : {channel.mention}**",
                        color=nextcord.Color.green(),
                    ),
                    ephemeral=True,
                )
                return await InteractionResponse.response_success(
                    interaction, "check reputation channel", self.data["emoji_tick"]
                )
        raise DataNotFound("channel reputation", interaction.guild_id)

    @check_setup.subcommand(
        description="to check setup channel live stock",
        name="live-stock",
        inherit_hooks=True,
    )
    async def live_stock(self, interaction: nextcord.Interaction):
        await InteractionResponse.response_loading(interaction)
        if live_stock_channel := await LiveStockDatabase().get("guild"):
            if channel := interaction.guild.get_channel(live_stock_channel.channel_id):
                if message := await channel.fetch_message(
                    live_stock_channel.message_id
                ):
                    await interaction.followup.send(
                        embed=nextcord.Embed(
                            description=f"**Live Stock Log Channel : {message.jump_url}**",
                            color=nextcord.Color.green(),
                        ),
                        ephemeral=True,
                    )
                    return await InteractionResponse.response_success(
                        interaction, "check live stock channel", self.data["emoji_tick"]
                    )
        raise DataNotFound("channel live stock", interaction.guild_id)

    @check_setup.subcommand(
        description="to check setup channel goodbye", inherit_hooks=True
    )
    async def goodbye(self, interaction: nextcord.Interaction):
        await InteractionResponse.response_loading(interaction)
        if goodbye := await GoodbyeDatabase().get("guild"):
            try:
                await interaction.followup.send(
                    embed=nextcord.Embed(
                        description=f"**Goodbye Log Channel : {interaction.guild.get_channel(goodbye.channel_id).mention}**",
                        color=nextcord.Color.green(),
                    ),
                    ephemeral=True,
                )
                return await InteractionResponse.response_success(
                    interaction, "check goodbye log channel", self.data["emoji_tick"]
                )
            except:
                pass
        raise DataNotFound("channel_goodbye", interaction.guild_id)

    @check_setup.subcommand(
        description="to check setup channel welcome", inherit_hooks=True
    )
    async def welcome(self, interaction: nextcord.Interaction):
        await InteractionResponse.response_loading(interaction)
        if welcome := await WelcomeDatabase().get("guild"):
            try:
                await interaction.followup.send(
                    embed=nextcord.Embed(
                        description=f"**Welcome Log Channel : {interaction.guild.get_channel(welcome.channel_id).mention}**",
                        color=nextcord.Color.green(),
                    ),
                    ephemeral=True,
                )
                return await InteractionResponse.response_success(
                    interaction, "check welcome log channel", self.data["emoji_tick"]
                )
            except:
                pass
        raise DataNotFound("channel_welcome", interaction.guild_id)

    @check_setup.subcommand(
        description="to check setup channel verification", inherit_hooks=True
    )
    async def verification(self, interaction: nextcord.Interaction):
        await InteractionResponse.response_loading(interaction)
        if verif := await VerificationDatabase().get("guild"):
            if channel := interaction.guild.get_channel(verif.channel_id):
                if message := await channel.fetch_message(verif.message_id):
                    await interaction.followup.send(
                        embed=nextcord.Embed(
                            description=f"**Verification Channel : {message.jump_url}**",
                            color=nextcord.Color.green(),
                        ),
                        ephemeral=True,
                    )
                    return await InteractionResponse.response_success(
                        interaction,
                        "check verification channel",
                        self.data["emoji_tick"],
                    )
        raise DataNotFound("channel_verification", interaction.guild_id)

    @check_setup.subcommand(
        description="to check setup channel donate", inherit_hooks=True
    )
    async def donate(self, interaction: nextcord.Interaction):
        await InteractionResponse.response_loading(interaction)
        if channel_donate := await ChannelDonateDatabase().get():
            try:
                if channel_donate.lock:
                    await interaction.followup.send(
                        embed=nextcord.Embed(
                            description=f"**Growtopia Log Channel : {interaction.guild.get_channel(channel_donate.lock).mention}**",
                            color=nextcord.Color.green(),
                        ).set_image(self.data["thumbnail"]),
                        ephemeral=True,
                    )
            except:
                await interaction.followup.send(
                    embed=nextcord.Embed(
                        description=f"**Growtopia Log Channel : Not Found**",
                        color=nextcord.Color.red(),
                    ).set_image(self.data["thumbnail"]),
                    ephemeral=True,
                )
            try:
                if channel_donate.saweria:
                    await interaction.followup.send(
                        embed=nextcord.Embed(
                            description=f"**Saweria Log Channel : {interaction.guild.get_channel(channel_donate.saweria).mention}**",
                            color=nextcord.Color.green(),
                        ).set_image(self.data["thumbnail"]),
                        ephemeral=True,
                    )
            except:
                await interaction.followup.send(
                    embed=nextcord.Embed(
                        description=f"**Saweria Log Channel : Not Found**",
                        color=nextcord.Color.red(),
                    ).set_image(self.data["thumbnail"]),
                    ephemeral=True,
                )
            try:
                if channel_donate.trakteer:
                    await interaction.followup.send(
                        embed=nextcord.Embed(
                            description=f"**Trakteer Log Channel : {interaction.guild.get_channel(channel_donate.trakteer).mention}**",
                            color=nextcord.Color.green(),
                        ).set_image(self.data["thumbnail"]),
                        ephemeral=True,
                    )
            except:
                await interaction.followup.send(
                    embed=nextcord.Embed(
                        description=f"**Trakteer Log Channel : Not Found**",
                        color=nextcord.Color.red(),
                    ).set_image(self.data["thumbnail"]),
                    ephemeral=True,
                )
            try:
                if channel_donate.sociabuzz:
                    await interaction.followup.send(
                        embed=nextcord.Embed(
                            description=f"**Sociabuzz Log Channel : {interaction.guild.get_channel(channel_donate.sociabuzz).mention}**",
                            color=nextcord.Color.green(),
                        ).set_image(self.data["thumbnail"]),
                        ephemeral=True,
                    )
            except:
                await interaction.followup.send(
                    embed=nextcord.Embed(
                        description=f"**Sociabuzz Log Channel : Not Found**",
                        color=nextcord.Color.red(),
                    ).set_image(self.data["thumbnail"]),
                    ephemeral=True,
                )
            try:
                if channel_donate.transfer:
                    await interaction.followup.send(
                        embed=nextcord.Embed(
                            description=f"**Transfer Log Channel : {interaction.guild.get_channel(channel_donate.transfer).mention}**",
                            color=nextcord.Color.green(),
                        ).set_image(self.data["thumbnail"]),
                        ephemeral=True,
                    )
            except:
                await interaction.followup.send(
                    embed=nextcord.Embed(
                        description=f"**Transfer Log Channel : Not Found**",
                        color=nextcord.Color.red(),
                    ).set_image(self.data["thumbnail"]),
                    ephemeral=True,
                )
            return await InteractionResponse.response_success(
                interaction, "check donate channel", self.data["emoji_tick"]
            )
        raise DataNotFound("channel_donate", interaction.guild.id)


def setup(bot):
    bot.add_cog(CheckSlashCommands(bot))
