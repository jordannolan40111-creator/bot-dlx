import discord
from discord.ext import commands
import os
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# ---------- READY ----------

@bot.event
async def on_ready():
    print(f"Bot connecté : {bot.user}")

# ---------- NOUVEAU MEMBRE ----------

@bot.event
async def on_member_join(member):

    # ROLE MEMBRE AUTO
    role = discord.utils.get(member.guild.roles, name="membre")
    if role:
        await member.add_roles(role)

    # SALON BIENVENUE
    channel = discord.utils.get(member.guild.text_channels, name="Bienvenue")
    regles = discord.utils.get(member.guild.text_channels, name="Règles")

    if channel:
        await channel.send(
            f"🔥 Bienvenue {member.mention} chez **DLX eSport** !\n"
            f"📜 Lis les règles ici → {regles.mention if regles else 'Règles'}\n"
            f"📝 Pense à faire ta présentation."
        )

# ---------- QUITTE ----------

@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name="Au revoir")
    if channel:
        await channel.send(f"{member.name} a quitté DLX 👋")

# ---------- ANTI INSULTES ----------

bad_words = ["pute","fdp","connard","salope"]

@bot.event
async def on_message(message):

    if message.author.bot:
        return

    for word in bad_words:
        if word in message.content.lower():
            await message.delete()
            await message.channel.send(
                f"{message.author.mention} ⚠️ message supprimé (langage interdit)"
            )
            return

    await bot.process_commands(message)

# ---------- COMMANDE TEST ----------

@bot.command()
async def ping(ctx):
    await ctx.send("DLX BOT OK 🟢")


bot.run(os.getenv("TOKEN"))
