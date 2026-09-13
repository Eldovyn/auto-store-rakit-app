import nextcord
from nextcord.ext import commands, application_checks
from utils import CustomCheck, DuplicateData
from databases import Product as ProductDatabase
import yaml
from utils import InteractionResponse


class Create(commands.Cog):
    from utils.config import data

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="create",
        description="for create commands",
    )
    @application_checks.check(CustomCheck().check_admin)
    async def create(self, interaction: nextcord.Interaction):
        pass

    @create.subcommand(description="to add product", inherit_hooks=True, name="product")
    async def add_product(
        self,
        interaction: nextcord.Interaction,
        title: str = nextcord.SlashOption(
            description="product title", required=True, min_length=2
        ),
        description: str = nextcord.SlashOption(
            description="product description", required=True, min_length=2
        ),
        code: str = nextcord.SlashOption(
            description="product code", required=True, min_length=2, max_length=50
        ),
        role: nextcord.Role = nextcord.SlashOption(
            description="role for buyer", required=True
        ),
        category: str = nextcord.SlashOption(
            description="category of product",
            required=True,
            choices={"script": "script", "non-script": "non-script"},
        ),
        price: int = nextcord.SlashOption(
            description="price world lock", required=False, min_value=1
        ),
        min_buy: int = nextcord.SlashOption(
            description="min buy", required=False, default=1, min_value=1
        ),
    ):
        await interaction.response.send_message(
            embed=nextcord.Embed(
                description=f"**{self.data['emoji_loading']} process your transaction**",
                color=nextcord.Color.yellow(),
            ),
            ephemeral=True,
        )
        code = code.upper()
        try:
            result = await ProductDatabase().insert(
                title, description, code, role.id, category, min_buy, price
            )
        except:
            raise DuplicateData("product", code)
        await InteractionResponse().response_success(
            interaction, f"create `{code}`", self.data["emoji_tick"]
        )

    @create.subcommand(name="emoji", description="to create emoji", inherit_hooks=True)
    async def create_emoji(
        self,
        interaction: nextcord.Interaction,
        name: str = nextcord.SlashOption(description="emoji name", required=True),
        image: nextcord.Attachment = nextcord.SlashOption(
            description="image to create emoji", required=True
        ),
    ):
        await interaction.response.send_message(
            embed=nextcord.Embed(
                description=f"**{self.data['emoji_loading']} process your transaction**",
                color=nextcord.Color.yellow(),
            ),
            ephemeral=True,
        )
        try:
            emoji = await interaction.guild.create_custom_emoji(
                name=name, image=await image.read()
            )
            await InteractionResponse().response_success(
                interaction, f"create emoji `{emoji}`", self.data["emoji_tick"]
            )
        except nextcord.HTTPException:
            await InteractionResponse().response_error(
                interaction, "create emoji", self.data["emoji_cross"], "http block"
            )
        except nextcord.Forbidden:
            await InteractionResponse().response_error(
                interaction,
                "create emoji",
                self.data["emoji_cross"],
                "missing permissions create emoji",
            )


def setup(bot):
    bot.add_cog(Create(bot))
