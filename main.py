import discord
from discord.ext import commands
import aiohttp
import requests
import json
from utils.credentials import get_bot_token

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents, help_command=None)


@bot.event
async def on_ready():
    print(f"{bot.user} que pasa guapo!")
    bot.get_guild(165698427819130881).fetch_members()


def get_quote_inspire():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote


@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return

    if ctx.content.startswith('$hi'):
        await ctx.channel.send('Hola!')

    if ctx.content.startswith('$diego!'):
        await ctx.channel.send(file=discord.File('hola-jose.jpg'))

    if ctx.content.startswith('$inspire'):
        quote = get_quote_inspire()
        await ctx.channel.send(quote)

    if ctx.content.startswith('$dog'):
        await dog(ctx)


@bot.command()
async def help(ctx):
    try:
        await ctx.channel.send('ROFOLE')
    except Exception as e:
        print(e.args)


@bot.command()
async def dog(ctx):
    try:
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/dog')
            dog_json = await request.json()

            request2 = await session.get('https://some-random-api.ml/facts/dog')
            fact_json = await request2.json()

            embed = discord.Embed(color=discord.Color.purple())
            embed.set_image(url=dog_json['link'])
            embed.set_footer(text=fact_json['fact'])
            await ctx.channel.send(embed=embed)
    except Exception as e:
        print(e.args)


bot.run(get_bot_token())
