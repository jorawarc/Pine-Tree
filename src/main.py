
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")  # load env variables
bot = commands.Bot(command_prefix='!')


@bot.command()
async def game(ctx):
    pass


@bot.command()
async def champion(ctx):
    pass


@bot.command()
async def build(ctx):
    pass


if __name__ == '__main__':
    bot.run(os.getenv('TOKEN'))
