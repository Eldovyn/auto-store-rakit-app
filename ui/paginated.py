import nextcord
import yaml


class Paginated(nextcord.ui.View):
    from utils.config import data

    def __init__(self, embeds):
        super().__init__()
        self.embeds = embeds
        self.current_page = 0

    @nextcord.ui.button(
        style=nextcord.ButtonStyle.secondary,
        custom_id="first_page_button",
    )
    async def first_page_button(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await interaction.response.defer()
        if self.current_page != 0:
            self.current_page = 0
        if self.current_page == 0:
            button.disabled = True
            self.previous_button.disabled = True
            self.last_page_button.disabled = False
            self.next_button.disabled = False
        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            embed=self.embeds[self.current_page],
            view=self,
        )

    @nextcord.ui.button(
        style=nextcord.ButtonStyle.primary,
        custom_id="previous_page_button",
    )
    async def previous_button(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await interaction.response.defer()
        if self.current_page > 0:
            self.current_page -= 1
        if self.current_page == 0:
            button.disabled = True
            self.first_page_button.disabled = True
            self.last_page_button.disabled = False
            self.next_button.disabled = False
        if self.current_page < len(self.embeds) - 1:
            self.last_page_button.disabled = False
            self.next_button.disabled = False
        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            embed=self.embeds[self.current_page],
            view=self,
        )

    @nextcord.ui.button(
        style=nextcord.ButtonStyle.primary,
        custom_id="next_page_button",
    )
    async def next_button(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await interaction.response.defer()
        if self.current_page < len(self.embeds) - 1:
            self.current_page += 1
        if self.current_page == len(self.embeds) - 1:
            button.disabled = True
            self.last_page_button.disabled = True
            self.previous_button.disabled = False
            self.first_page_button.disabled = False
        if self.current_page > 0:
            self.previous_button.disabled = False
            self.first_page_button.disabled = False
        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            embed=self.embeds[self.current_page],
            view=self,
        )

    @nextcord.ui.button(
        style=nextcord.ButtonStyle.secondary,
        custom_id="last_page_button",
    )
    async def last_page_button(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await interaction.response.defer()
        if self.current_page != len(self.embeds) - 1:
            self.current_page = len(self.embeds) - 1

        if self.current_page == len(self.embeds) - 1:
            button.disabled = True
            self.next_button.disabled = True
            self.previous_button.disabled = False
            self.first_page_button.disabled = False

        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            embed=self.embeds[self.current_page],
            view=self,
        )

    async def disable_buttons(self):
        self.first_page_button.disabled = True
        self.previous_button.disabled = True
        if len(self.embeds) == 1:
            self.last_page_button.disabled = True
            self.next_button.disabled = True
        await self.set_emoji()

    async def set_emoji(self):
        for child in self.children:
            if isinstance(child, nextcord.ui.Button):
                child.emoji = self.data["pagination"][child.custom_id]
