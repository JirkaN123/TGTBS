import discord
import discord.ui
import discord.colour
import json
import time 

from colorama import Back, Fore, Style
from discord.ext import commands

with open("data.json", "r") as f:
    configData = json.load(f)

token = configData["token"]
prefix = configData["prefix"]
role = configData["role"]

prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC",
time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
Name = (Fore.BLUE + " VerifiSys" + Fore.WHITE)

bot = commands.Bot(command_prefix= prefix, intents=discord.Intents.all())

class VerifiSystem(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)

    @bot.event
    async def on_ready():
        await bot.change_presence(status=discord.Status.online, activity=discord.Game("Verifikaci"))
        bot.add_view(VerifiSystem())

        print(prfx + Name + " Bot ID " + Fore.YELLOW + str(bot.user.id))
        print(prfx + Name + " Slash CMDs Synced " + Fore.YELLOW + str(len("0")) + " Commands")

    @discord.ui.button(label="Verify",custom_id="Verify",style= discord.ButtonStyle.success)
    async def verify(self, interaction, button):
        user = interaction.user
        if role not in [y.id for y in user.roles]:
            await user.add_roles(user.guild.get_role(role))
            await user.send("Jsi verifikovaní!")
            print(prfx + Name + Fore.GREEN + " [+] One user was verified on Discord.")
        else:
            await user.send("Jiš jsi už verifikovaní!")
            print(prfx + Name + Fore.GREEN + " [+] One user is stupid and try second verified.")

@bot.command()
@commands.has_permissions(administrator=True)
async def initialize(ctx):
    embed = discord.Embed(title= "Verifikovat", description = "Klikni pro verifikaci.",color= discord.Color.blue())
    await ctx.send(embed = embed, view = VerifiSystem())
  
bot.run(token)