from nextcord import Webhook as NextcordWebhook
import aiohttp
import nextcord


class Webhook:
    @staticmethod
    async def send_reputation(
        guild, data, footer, message, star, created_at, image, reputation_id
    ):
        webhook_url = data["webhook_reputation"]
        webhook_username = data["username_webhook"]
        async with aiohttp.ClientSession() as session:
            webhook = NextcordWebhook.from_url(webhook_url, session=session)
            embed = nextcord.Embed(
                description=f"**Reputation {guild.name} #{reputation_id}**",
                color=nextcord.Color.green(),
                timestamp=created_at,
            )
            embed.set_image(url=image)
            embed.set_footer(text=footer)
            embed.set_thumbnail(guild.icon.url)
            embed.add_field(name="Message", value=message, inline=True)
            embed.add_field(name="Stars", value=star, inline=True)
            await webhook.send(
                embed=embed, username=webhook_username, avatar_url=guild.icon.url
            )

    @staticmethod
    async def update_balance(
        guild, category, data, update, amount, growid, user, created_at
    ):
        webhook_url = data["webhook_update_balance"]
        webhook_username = data["username_webhook"]
        async with aiohttp.ClientSession() as session:
            webhook = NextcordWebhook.from_url(webhook_url, session=session)
            embed = nextcord.Embed(
                title=f"**{data['emoji_crown']} {category} Balance Log {data['emoji_crown']}**",
                color=nextcord.Color.green(),
                timestamp=created_at,
            )
            result_update = ""
            if update in ("add", "sub"):
                result_update = f"+" if update == "add" else f"-"
            embed.description = f"""**[{data['emoji_bot']}] GrowID : `{growid}` ({user})
[{data['emoji_product']}] Amount : `{result_update}{amount}` world lock**"""
            await webhook.send(
                embed=embed, username=webhook_username, avatar_url=guild.icon.url
            )
