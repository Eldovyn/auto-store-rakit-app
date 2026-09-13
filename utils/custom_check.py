import nextcord
from databases import (
    Maintenance as MaintenanceDatabase,
    ReputationChannel as ReputationChannelDatabase,
)
from .custom_error import OnMaintenance, ChannelNotAllow, DisableQris
import yaml
from nextcord.ext import application_checks


class CustomCheck:
    from utils.config import data

    @staticmethod
    async def check_admin(interaction: nextcord.Interaction):
        for role in interaction.user.roles:
            if role.id in CustomCheck.data["role_admin"]:
                return True
        raise application_checks.ApplicationMissingAnyRole(
            CustomCheck.data["role_admin"]
        )

    @staticmethod
    async def check_maintenance(interaction: nextcord.Interaction):
        if (
            data := await MaintenanceDatabase().get(
                "maintenance", guild_id=interaction.guild.id
            )
        ) and data.status:
            raise OnMaintenance()
        return True

    @staticmethod
    async def check_channel_rep(interaction: nextcord.Interaction):
        if data := await ReputationChannelDatabase().get("guild"):
            if not data.channel_id == interaction.channel.id:
                raise ChannelNotAllow(interaction.channel)
            return True
        return True
