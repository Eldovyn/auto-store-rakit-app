import nextcord
from nextcord.ext import commands
import yaml
from utils import Misc, InteractionResponse
from ui import Paginated as PaginatedView


class Help(commands.Cog):
    from utils.config import data

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="to send help command")
    async def help(
        self,
        interaction: nextcord.Interaction,
        per_page: int = nextcord.SlashOption(
            description="number of per page", required=False, min_value=1, default=5
        ),
    ):
        await InteractionResponse.response_loading(interaction)
        commands = []
        for i in interaction.client.get_all_application_commands():
            if i.children:
                for key, value in i.children.items():
                    if options := value.payload.get("options"):
                        opt = []
                        for op in options:
                            for k, v in op.items():
                                if k == "name":
                                    opt.append(f"`{v}`")
                        commands.append(
                            {
                                "command": f"{i.name} {key} {' '.join(opt)}",
                                "description": value.description,
                            }
                        )
                    else:
                        commands.append(
                            {
                                "command": f"{i.name} {key}",
                                "description": value.description,
                            }
                        )
            else:
                payload = i.get_payload(interaction.guild_id)
                opt = []
                if options := payload.get("options"):
                    for op in options:
                        for k, v in op.items():
                            if k == "name":
                                opt.append(f"`{v}`")
                    commands.append(
                        {
                            "command": f"{i.name} {' '.join(opt)}",
                            "description": i.description,
                        }
                    )
                else:
                    commands.append(
                        {
                            "command": f"{i.name}",
                            "description": i.description,
                        }
                    )
        paginated_arr = await Misc.split_array(commands, per_page)
        embeds = []
        for idx, page in enumerate(paginated_arr):
            embed = (
                nextcord.Embed(
                    title=f"Help Command {interaction.guild.name}",
                    color=nextcord.Color.green(),
                )
                .set_image(self.data["thumbnail"])
                .set_thumbnail(interaction.guild.icon.url)
            )
            for i, value in enumerate(page):
                embed.add_field(
                    name=f"{value['description']}",
                    value=f'{self.data["emoji_arrow"]} /{value["command"]}',
                    inline=False,
                )
            embeds.append(embed)

        if embeds:
            view = PaginatedView(embeds)
            await view.disable_buttons()
            await interaction.edit_original_message(
                embed=embeds[0],
                view=view,
            )


def setup(bot):
    bot.add_cog(Help(bot))
