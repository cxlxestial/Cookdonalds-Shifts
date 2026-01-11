import discord
from discord import app_commands
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

SHIFT_ROLE_NAME = "Shift Management"

def has_shift_role(member: discord.Member):
    return discord.utils.get(member.roles, name=SHIFT_ROLE_NAME) is not None

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot online as {bot.user}")

@bot.tree.command(name="shift_create", description="Create a new shift")
async def shift_create(
    interaction: discord.Interaction,
    start_time: str,
    end_time: str,
    host: str,
    co_host: str,
    supervisor: str
):
    if not has_shift_role(interaction.user):
        await interaction.response.send_message(
            "❌ You need the Shift Management role.",
            ephemeral=True
        )
        return

    embed = discord.Embed(
        title="🕒 Shift Created",
        color=discord.Color.blue()
    )
    embed.add_field(name="Start Time", value=start_time)
    embed.add_field(name="End Time", value=end_time)
    embed.add_field(name="Host", value=host)
    embed.add_field(name="Co-Host", value=co_host)
    embed.add_field(name="Supervisor", value=supervisor)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="shift_edit", description="Edit a shift")
@app_commands.choices(status=[
    app_commands.Choice(name="Planned", value="Planned"),
    app_commands.Choice(name="Active", value="Active"),
    app_commands.Choice(name="Cancelled", value="Cancelled")
])
async def shift_edit(
    interaction: discord.Interaction,
    start_time: str,
    end_time: str,
    host: str,
    co_host: str,
    supervisor: str,
    status: app_commands.Choice[str]
):
    if not has_shift_role(interaction.user):
        await interaction.response.send_message(
            "❌ You need the Shift Management role.",
            ephemeral=True
        )
        return

    embed = discord.Embed(
        title="✏️ Shift Updated",
        color=discord.Color.green()
    )
    embed.add_field(name="Status", value=status.value)
    embed.add_field(name="Start Time", value=start_time)
    embed.add_field(name="End Time", value=end_time)
    embed.add_field(name="Host", value=host)
    embed.add_field(name="Co-Host", value=co_host)
    embed.add_field(name="Supervisor", value=supervisor)

    await interaction.response.send_message(embed=embed)

bot.run(os.getenv("TOKEN"))
