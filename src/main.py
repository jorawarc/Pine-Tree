
import os
from riot_games import DataDragon
from warzone import Warzone
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")  # load env variables
bot = commands.Bot(command_prefix='>')

LOL = DataDragon()
WZ = Warzone(os.getenv('DEV_EMAIL'), os.getenv('DEV_PASS'))


@bot.command(pass_context=True)
async def lol(ctx, *args):
    """
    League of Legends `lol`
    """
    valid_commands = {cd.__name__: cd}
    if args and args[0] in valid_commands.keys():
        function, params = args[0], args[1:]
        s = valid_commands[function](*params)
        await ctx.send(s)


def cd(champion: str) -> str:
    """
         - Champion cooldowns: `cd <champion>`
    """
    format_champ = champion.lower().capitalize()
    cooldowns = LOL.get_champion_cool_down(format_champ)
    output = f"```\n" \
             f"{format_champ}`s Spell Cooldowns"\
             f"Q: {cooldowns['q']}\n" \
             f"W: {cooldowns['w']}\n" \
             f"E: {cooldowns['e']}\n" \
             f"R: {cooldowns['r']}" \
             f"```"
    return output


@bot.command(pass_context=True)
async def wz(ctx, *args):
    """
    Warzone `wz`
    """
    valid_commands = {post.__name__: post}
    if args and args[0] in valid_commands.keys():
        function, params = args[0], args[1:]
        s = await valid_commands[function](*params)
        await ctx.send(s)


async def post(username: str) -> str:
    """
        - Post lobby stats: `post <username>`
    """
    start_time, player, group = await WZ.post_game_stats(username, output_data=True)
    output = f"```\n" \
             f"Game start time {start_time}\n" \
             f"{player[['kdRatio', 'kills', 'deaths', 'damageDone', 'player']].to_string()}\n\n" \
             f"{group[group['team'] == player['team'].iloc[0]].to_string()}\n\n" \
             f"{group.head(5).to_string()}\n" \
             f"```"
    return output


@bot.command()
async def sb(ctx):
    pass


@bot.command()
async def pine(ctx):
    league = [cd]
    warzone = [post]
    league_string = "League of Legends Commands (prefixed with `lol`): {}".format("\n".join([i.__doc__ for i in league]))
    wz_string = "Warzone Commands (prefixed with `wz`): {}".format("\n".join([i.__doc__ for i in warzone]))
    output = "Pine Tree supports the following commands: \n{}".format("\n".join([league_string, wz_string]))
    await ctx.send(output)


if __name__ == '__main__':
    bot.run(os.getenv('TOKEN'))
