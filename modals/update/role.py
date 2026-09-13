import nextcord
from databases import Product as ProductDatabase
import yaml
from utils import InteractionResponse


class UpdateRoleModal(nextcord.ui.Modal):
    from utils.config import data

    def __init__(self, code):
        super().__init__("Update Role", timeout=None)

        self.role_id = nextcord.ui.TextInput(
            label="Role ID",
            custom_id="role_id",
            min_length=1,
            max_length=50,
        )
        self.add_item(self.role_id)

        self.confirm_role_id = nextcord.ui.TextInput(
            label="Confirm Role ID",
            custom_id="confirm_role_id",
            min_length=1,
            max_length=50,
        )
        self.add_item(self.confirm_role_id)

        self.code = code

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await InteractionResponse().response_loading(interaction)
        try:
            role_id = int(self.role_id.value)
            int(self.confirm_role_id.value)
        except:
            return await InteractionResponse().response_error(
                interaction,
                f"update role `{self.code}`",
                self.data["emoji_cross"],
                f"role id must be number",
            )
        if self.role_id.value != self.confirm_role_id.value:
            return await InteractionResponse().response_error(
                interaction,
                f"update role id `{self.code}`",
                self.data["emoji_cross"],
                "role id not match",
            )
        if not (role := interaction.guild.get_role(role_id)):
            return await InteractionResponse().response_error(
                interaction,
                f"update role id `{self.code}`",
                self.data["emoji_cross"],
                f"role id `{role_id}` not found",
            )
        if not (product := await ProductDatabase().get("code", code=self.code)):
            return await InteractionResponse().response_error(
                interaction,
                f"update role id `{self.code}`",
                self.data["emoji_cross"],
                f"role id `{role_id}` not found",
            )
        await ProductDatabase().update("role", code=self.code, role=role.id)
        await InteractionResponse().response_success(
            interaction,
            f"update role id `{self.code}`",
            self.data["emoji_tick"],
        )
