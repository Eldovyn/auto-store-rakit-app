import nextcord
from nextcord.ext import commands, application_checks
import yaml
from utils import CustomCheck, DataNotFound, InteractionResponse
import os
from modals import (
    UpdatePriceModal,
    UpdateDiscountModal,
    UpdateFreeProductModal,
    UpdateCodeModal,
    UpdateRoleModal,
    UpdateDescriptionModal,
    UpdateMinBuyModal,
    UpdateTitleModal,
)
from databases import (
    Product as ProductDatabase,
    Stock as StockDatabase,
)
import re
from models import StockModel, ProductModel


class Update(commands.Cog):
    from utils.config import data

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="update",
        description="to update bot auto store",
    )
    @application_checks.check(CustomCheck().check_admin)
    async def update(self, interaction: nextcord.Interaction):
        pass

    @update.subcommand(
        description="to update stock product in database",
        inherit_hooks=True,
    )
    async def stock(self, interaction: nextcord.Interaction):
        pass

    @stock.subcommand(
        description="to update stock product without file in database",
        name="non-file",
        inherit_hooks=True,
    )
    async def non_file(
        self,
        interaction: nextcord.Interaction,
        code: str = nextcord.SlashOption(description="product code", required=True),
        category: str = nextcord.SlashOption(
            description="category update",
            required=True,
            choices={
                "add": "add",
                "remove": "remove",
                "clear": "clear",
                "edit": "edit",
            },
        ),
        item: str = nextcord.SlashOption(description="item product", required=False),
    ):
        await interaction.response.send_message(
            embed=nextcord.Embed(
                description=f"**{self.data['emoji_loading']} process your transaction**",
                color=nextcord.Color.yellow(),
            ),
            ephemeral=True,
        )
        if not (prod := await ProductDatabase().get("code", code=code.upper())):
            raise DataNotFound("product", code.upper())
        if prod.category == "script":
            return await InteractionResponse().response_error(
                interaction,
                f"process your transaction",
                self.data["emoji_cross"],
                "script product not allowed",
            )
        if category == "clear":
            await StockDatabase().delete("clear", code=prod.code)
        elif category == "edit":
            match = re.search(r"item:\s*(.*?)\s*new_item:\s*(.*)", item)
            item_text = match.group(1) if match else None
            new_item_text = match.group(2) if match else None
            if not item_text or not new_item_text:
                return await interaction.edit_original_message(
                    embed=nextcord.Embed(
                        description="**item product not found**",
                        color=nextcord.Color.red(),
                    ),
                )
            await StockDatabase().update(
                "edit", code=prod.code, item=item_text, new_item=new_item_text
            )
        else:
            if not item:
                return await InteractionResponse().response_error(
                    interaction,
                    f"process your transaction",
                    self.data["emoji_cross"],
                    "item product not found",
                )
            if category == "add":
                await StockDatabase().insert(
                    prod.code,
                    None,
                    item,
                    nextcord.utils.utcnow().timestamp(),
                )
            else:
                if item_remove := await StockDatabase().get(
                    "item", code=prod.code, item=item
                ):
                    await StockDatabase().delete(
                        "code",
                        code=item_remove.product.code,
                        item=item_remove.item,
                        created_at=item_remove.created_at,
                    )
                else:
                    return await InteractionResponse().response_error(
                        interaction,
                        f"process your transaction",
                        self.data["emoji_cross"],
                        "item product not found",
                    )
        return await InteractionResponse().response_success(
            interaction,
            f"update stock product `{prod.code}`",
            self.data["emoji_tick"],
        )

    @stock.subcommand(
        description="to update stock product with file in database",
        name="with-file",
        inherit_hooks=True,
    )
    async def with_file(
        self,
        interaction: nextcord.Interaction,
        code: str = nextcord.SlashOption(description="product code", required=True),
        category: str = nextcord.SlashOption(
            description="category update",
            required=True,
            choices={
                "add": "add",
                "remove": "remove",
                "clear": "clear",
                "edit": "edit",
            },
        ),
        item: nextcord.Attachment = nextcord.SlashOption(
            description="item product", required=False
        ),
        new_item: nextcord.Attachment = nextcord.SlashOption(
            description="this is for edit script", required=False
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
        if not (prod := await ProductDatabase().get("code", code=code)):
            raise DataNotFound("product", code)
        if category == "clear":
            await StockDatabase().delete("clear", code=code)
        else:
            try:
                _, file_extension = os.path.splitext(item.filename)
            except:
                return await InteractionResponse().response_error(
                    interaction,
                    f"process your transaction",
                    self.data["emoji_cross"],
                    "item product not found",
                )
            if prod.category == "script":
                script_bytes = await item.read()
                if file_extension not in self.data["script_extensions"]:
                    return await InteractionResponse().response_error(
                        interaction,
                        f"process your transaction",
                        self.data["emoji_cross"],
                        f"`{file_extension}` not allowed",
                    )
                if category == "add":
                    await StockDatabase().insert(
                        prod.code,
                        f"{prod.title.title()}{file_extension}",
                        script_bytes,
                        nextcord.utils.utcnow().timestamp(),
                    )
                elif category == "edit":
                    if not new_item:
                        return await InteractionResponse().response_error(
                            interaction,
                            f"process your transaction",
                            self.data["emoji_cross"],
                            "item product not found",
                        )
                    new_script_bytes = await new_item.read()
                    if st := await StockDatabase().get(
                        "code", code=prod.code, item=script_bytes
                    ):
                        await StockDatabase().update(
                            "edit",
                            code=prod.code,
                            item=script_bytes,
                            new_item=new_script_bytes,
                        )
                    else:
                        return await InteractionResponse().response_error(
                            interaction,
                            f"process your transaction",
                            self.data["emoji_cross"],
                            "item product not found",
                        )
                else:
                    if item_remove := await StockDatabase().get(
                        "item", code=prod.code, item=script_bytes
                    ):
                        await StockDatabase().delete(
                            "code",
                            code=item_remove.product.code,
                            item=item_remove.item,
                            created_at=item_remove.created_at,
                        )
                    else:
                        return await InteractionResponse().response_error(
                            interaction,
                            f"process your transaction",
                            self.data["emoji_cross"],
                            "item product not found",
                        )
            else:
                if file_extension not in [".txt"]:
                    return await InteractionResponse().response_error(
                        interaction,
                        f"process your transaction",
                        self.data["emoji_cross"],
                        "bulk product only allow `.txt` file",
                    )
                file_content = await item.read()
                text_content = file_content.decode("utf-8")
                lines_array = text_content.splitlines()
                lines_array = [line for line in lines_array if line]
                if category == "add":
                    items = [
                        StockModel(
                            file_name=None,
                            item=i,
                            created_at=nextcord.utils.utcnow().timestamp(),
                            product=ProductModel.objects(code=prod.code).first(),
                        )
                        for i in lines_array
                        if i and (prod := ProductModel.objects(code=prod.code).first())
                    ]
                    await StockDatabase().insert(category="bulk", bulk_items=items)
                else:
                    for index, line in enumerate(lines_array):
                        if category == "edit":
                            match = re.search(r"item:\s*(.*?)\s*new_item:\s*(.*)", line)
                            item_text = match.group(1) if match else None
                            new_item_text = match.group(2) if match else None
                            if not item_text or not new_item_text:
                                if index == 0:
                                    return await InteractionResponse().response_error(
                                        interaction,
                                        f"process your transaction",
                                        self.data["emoji_cross"],
                                        "item product not found",
                                    )
                            await StockDatabase().update(
                                "edit",
                                code=prod.code,
                                item=item_text,
                                new_item=new_item_text,
                            )
                        else:
                            if item_remove := await StockDatabase().get(
                                "item", code=prod.code, item=line
                            ):
                                await StockDatabase().delete(
                                    "code",
                                    code=item_remove.product.code,
                                    item=item_remove.item,
                                    created_at=item_remove.created_at,
                                )
                            else:
                                if index == 0:
                                    return await InteractionResponse().response_error(
                                        interaction,
                                        f"process your transaction",
                                        self.data["emoji_cross"],
                                        "item product not found",
                                    )
        await InteractionResponse().response_success(
            interaction,
            f"update product `{code}`",
            self.data["emoji_tick"],
        )

    @update.subcommand(
        description="to update product in database",
        inherit_hooks=True,
    )
    async def product(
        self,
        interaction: nextcord.Interaction,
        code: str = nextcord.SlashOption(description="product code", required=True),
        category: str = nextcord.SlashOption(
            description="category update",
            required=True,
            choices={
                "price": "price",
                "code": "code",
                "role": "role",
                "title": "title",
                "min-buy": "min-buy",
                "discount": "discount",
                "buy-get": "buy-get",
                "description": "description",
            },
        ),
    ):
        if category == "price":
            modal = UpdatePriceModal(code.upper())
            await interaction.response.send_modal(modal)
        elif category == "code":
            modal = UpdateCodeModal(code.upper())
            await interaction.response.send_modal(modal)
        elif category == "role":
            modal = UpdateRoleModal(code.upper())
            await interaction.response.send_modal(modal)
        elif category == "min-buy":
            modal = UpdateMinBuyModal(code.upper())
            await interaction.response.send_modal(modal)
        elif category == "discount":
            modal = UpdateDiscountModal(code.upper())
            await interaction.response.send_modal(modal)
        elif category == "buy-get":
            modal = UpdateFreeProductModal(code.upper())
            await interaction.response.send_modal(modal)
        elif category == "description":
            modal = UpdateDescriptionModal(code.upper())
            await interaction.response.send_modal(modal)
        else:
            modal = UpdateTitleModal(code.upper())
            await interaction.response.send_modal(modal)

    @update.subcommand(
        description="to update profile bot",
        name="profile",
        inherit_hooks=True,
    )
    async def update_profile(
        self,
        interaction: nextcord.Interaction,
        image: nextcord.Attachment = nextcord.SlashOption(
            description="image profile", required=True
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
            _, file_extension = os.path.splitext(image.filename)
        except:
            return await InteractionResponse().response_error(
                interaction,
                f"update profile bot",
                self.data["emoji_cross"],
                "something wrong with image",
            )
        if file_extension not in [".png", ".jpg", ".jpeg"]:
            return await InteractionResponse().response_error(
                interaction,
                f"update profile bot",
                self.data["emoji_cross"],
                "image extension only png, jpg or jpeg",
            )
        try:
            await self.bot.user.edit(avatar=await image.read())
        except:
            return await InteractionResponse().response_error(
                interaction,
                f"update profile bot",
                self.data["emoji_cross"],
                "something wrong with image",
            )
        await InteractionResponse().response_success(
            interaction,
            f"update profile bot",
            self.data["emoji_tick"],
        )

    @update.subcommand(
        description="to update username bot",
        name="username",
        inherit_hooks=True,
    )
    async def update_username(
        self,
        interaction: nextcord.Interaction,
        username: str = nextcord.SlashOption(
            description="username your bot", required=True
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
            await self.bot.user.edit(username=username)
        except:
            return await InteractionResponse().response_error(
                interaction,
                f"update username bot",
                self.data["emoji_cross"],
                "something wrong with username",
            )
        await InteractionResponse().response_success(
            interaction,
            f"update username bot",
            self.data["emoji_tick"],
        )


def setup(bot):
    bot.add_cog(Update(bot))
