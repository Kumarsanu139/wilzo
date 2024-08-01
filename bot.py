import os
from dotenv import load_dotenv
import discord
from discord import app_commands
from datetime import datetime, timedelta
from keep_alive import keep_alive

# Load environment variables
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Wilzo GAMING"))

client = MyClient(intents=intents)

@client.tree.command(name="say")
@app_commands.describe(message="The message you want the bot to say")
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.send_message("Message sent!", ephemeral=True)
    await interaction.channel.send(message)

@client.tree.command(name="ban")
@app_commands.describe(member="The member to ban", reason="Reason for the ban")
@app_commands.default_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    await member.ban(reason=reason)
    await interaction.response.send_message(f"{member.mention} has been banned. Reason: {reason}", ephemeral=True)

@client.tree.command(name="kick")
@app_commands.describe(member="The member to kick", reason="Reason for the kick")
@app_commands.default_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    await member.kick(reason=reason)
    await interaction.response.send_message(f"{member.mention} has been kicked. Reason: {reason}", ephemeral=True)

@client.tree.command(name="timeout")
@app_commands.describe(member="The member to timeout", duration="Timeout duration in minutes", reason="Reason for the timeout")
@app_commands.default_permissions(moderate_members=True)
async def timeout(interaction: discord.Interaction, member: discord.Member, duration: int, reason: str = None):
    await member.timeout(datetime.utcnow() + timedelta(minutes=duration), reason=reason)
    await interaction.response.send_message(f"{member.mention} has been timed out for {duration} minutes. Reason: {reason}", ephemeral=True)

@client.tree.command(name="create_embed")
@app_commands.describe(title="Embed title", description="Embed description", color="Embed color (in hexadecimal)")
async def create_embed(interaction: discord.Interaction, title: str, description: str, color: str = "000000"):
    try:
        embed = discord.Embed(title=title, description=description, color=int(color, 16))
        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("Embed sent!", ephemeral=True)
    except ValueError:
        await interaction.response.send_message("Invalid color. Please use a valid hexadecimal color code.", ephemeral=True)

# Get the token from .env file
TOKEN = os.getenv('DISCORD_TOKEN')

# Run the client with keep_alive
if TOKEN is not None:
    print(f"Token: {TOKEN}")
    keep_alive()
    client.run(TOKEN)
else:
    print("No token found in .env file. Please check your environment variable setup.")
