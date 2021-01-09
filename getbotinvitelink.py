import os
import discord
from discord.ext import commands
from settings import Settings

bot = discord.Client()

settings = Settings.get()
TOKEN = os.getenv('DGSM_TOKEN', settings['token'])

@bot.event
async def on_ready():
    print(f'https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=268954704&scope=bot')
    await bot.close()

bot.run(TOKEN)
