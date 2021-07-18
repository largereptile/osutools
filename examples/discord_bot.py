import osutools
import discord
from discord.ext import commands

osu = osutools.OsuClientV1("token")
bot = commands.Bot(command_prefix="!")


@bot.command(name="profile")
async def profile(ctx, *, username):
    user = osu.fetch_user(username=username)
    embed = discord.Embed(title=f"osu! Profile for {user.username}")
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="Rank", value=f"#{user.rank}")
    embed.add_field(name="pp", value=f"{user.pp}")
    embed.add_field(name="Accuracy", value=f"{round(user.accuracy, 2)}%")
    embed.add_field(name="Playcount", value=f"{user.play_count}")
    await ctx.send(embed=embed)

bot.run("token2")
