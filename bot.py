import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True  # Required to read the message text
bot = commands.Bot(command_prefix="!", intents=intents)

# Set the exact numeric ID of the user you want to target
TARGET_USER_ID = 1322783159049261157  

@bot.event
async def on_ready():
    print(f"Bot logged in and active as {bot.user}")

@bot.event
async def on_message(message):
    # Ignore messages sent by bots to prevent infinite looping
    if message.author.bot:
        return

    # Check if the message came from your specific target
    if message.author.id == TARGET_USER_ID:
        try:
            # 1. Delete their original text immediately
            await message.delete()

            # 2. Find an existing bot webhook or create a new one in this channel
            channel = message.channel
            webhooks = await channel.webhooks()
            webhook = next((wh for wh in webhooks if wh.name == "GlobalMimic"), None)
            
            if not webhook:
                webhook = await channel.create_webhook(name="GlobalMimic")

            # 3. Re-post their exact message content using their current name and avatar
            await webhook.send(
                content=message.content,
                username=message.author.display_name,
                avatar_url=message.author.display_avatar.url
            )
            
        except discord.Forbidden:
            print("Permission Error: Ensure the bot has 'Manage Messages' and 'Manage Webhooks' enabled in this channel.")
        except discord.HTTPException as e:
            print(f"Network or API Error: {e}")

    # Allows standard commands to still function if you add them later
    await bot.process_commands(message)

# Paste your private bot token from the Discord Developer Portal here
bot.run("MTUyMDIxMDU5OTU2NzU1NjgyMQ.G2ZIu8.Yq5FO8WhOqN3rsxU39X9TVjuXwxpKN6-opI2sU")
