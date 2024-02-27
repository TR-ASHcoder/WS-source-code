
import keep_alive
import DiscordUtils
from discord.utils import get
import requests
import discord
from discord.ext import commands
import os
import random
from googleapiclient.discovery import build
import giphy_client
from giphy_client.rest import ApiException
import urllib
import json
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
from discord_slash import SlashCommand
#from craiyon import Craiyon 
import time
import asyncio
import base64
import aiohttp

intents = discord.Intents.default()

gif_key = os.environ['GIF KEY']
api_key = os.environ['KEY']
client = commands.Bot(command_prefix='!', intents=intents)
slash = SlashCommand(client, sync_commands=True)
client.remove_command("help")


@client.event
async def on_ready():
    print('online')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='for /help'))


# -- animals --

@slash.slash(description="sends raccoons ( comes with fact )")
async def raccoon(ctx):
    r = requests.get("https://some-random-api.com/animal/raccoon")
    res = r.json()

    em = discord.Embed(title="your raccoon  🦝",
                       color=discord.Color.from_rgb(10, 10, 10))
    em.set_image(url=res['image'])
    em.set_footer(text=f"fact: {res['fact']}")
    await ctx.send(embed=em)


@slash.slash(description="sends dogs ( comes with fact )")
async def dog(ctx): 
    r = requests.get("https://some-random-api.com/animal/dog")
    res = r.json()

    em = discord.Embed(title="your dog  🐶",
                       color=discord.Color.from_rgb(112, 65, 0))
    em.set_image(url=res['image'])
    em.set_footer(text=f"fact: {res['fact']}")
    await ctx.send(embed=em)


@slash.slash(description="sends birds ( comes with fact )")
async def bird(ctx):
    r = requests.get("https://some-random-api.com/animal/bird")
    res = r.json()

    em = discord.Embed(title="your bird  🐦", color=discord.Color.random())

    em.set_image(url=res['image'])
    em.set_footer(text=f"fact: {res['fact']}")
    await ctx.send(embed=em)


@slash.slash(description="sends cats ( comes with fact )")
async def cat(ctx):
    r = requests.get("https://some-random-api.com/animal/cat")
    res = r.json()

    em = discord.Embed(title="your cat  😺",
                       color=discord.Color.from_rgb(223, 5, 235))
    em.set_image(url=res['image'])
    em.set_footer(text=f"fact: {res['fact']}")
    await ctx.send(embed=em)


@slash.slash(description="sends pandas ( comes with fact )")
async def panda(ctx):
    r = requests.get("https://some-random-api.com/animal/panda")
    res = r.json()

    em = discord.Embed(title="your panda  🐼",
                       color=discord.Color.from_rgb(252, 252, 252))
    em.set_image(url=res['image'])
    em.set_footer(text=f"fact: {res['fact']}")
    await ctx.send(embed=em)


@slash.slash(description="sends some roos ( comes with fact )")
async def kangaroo(ctx):
    r = requests.get("https://some-random-api.com/animal/kangaroo")
    res = r.json()

    em = discord.Embed(title="ya roo mate  🦘",
                       color=discord.Color.from_rgb(79, 46, 5))
    em.set_image(url=res['image'])
    em.set_footer(text=f"fact: {res['fact']}")
    await ctx.send(embed=em)


@slash.slash(description="sends foxes ( comes with fact )")
async def fox(ctx):
    r = requests.get("https://some-random-api.com/animal/fox")
    res = r.json()

    em = discord.Embed(title="your fox  :fox:",
                       color=discord.Color.from_rgb(247, 2, 2))
    em.set_image(url=res['image'])
    em.set_footer(text=f"fact: {res['fact']}")
    await ctx.send(embed=em)


@slash.slash(description="sends koalas ( comes with fact )")
async def koala(ctx):
    r = requests.get("https://some-random-api.com/animal/koala")
    res = r.json()

    em = discord.Embed(title="ya koala mate  🐨",
                       color=discord.Color.from_rgb(135, 135, 134))
    em.set_image(url=res['image'])
    em.set_footer(text=f"fact: {res['fact']}")
    await ctx.send(embed=em)




# -- animals --

# -- other --

@slash.slash(description="generate a image using a really shit A.I")
async def generate(ctx: commands.Context, *, prompt: str):
  ETA = int(time.time() + 60)
  message = await ctx.send(f"take a break, this will take a while... \nimage will generate <t:{ETA}:R>")
  async with aiohttp.request("POST", "https://backend.craiyon.com/generate", json={"prompt": prompt}) as resp:
    r = await resp.json()
    images = r['images']
  image = BytesIO(base64.decodebytes(images[0].encode("utf-8")))    
  return await message.edit(content=f"your prompt was `{prompt}`", file=discord.File(image, "generatedImage.png"))


@slash.slash(description="searchs image of choice, has 27 min slowdown ")
@commands.cooldown(3, 1620, commands.BucketType.user)
async def search(ctx, *, search):
    ran = random.randint(-1, 9)
    resourse = build("customsearch", "v1", developerKey=api_key).cse()

    result = resourse.list(q=f"{search}",
                           cx="bcc252b6fe419f954",
                           searchType="image").execute()
    url = result["items"][ran]["link"]

    em = discord.Embed(title=f"you searched for `{search.title()}`",
                       color=discord.Color.green())
    em.set_image(url=url)
    em.set_footer(text=f"Image Link: \n{url}")
    await ctx.send(embed=em)
@search.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        ETA = int(time.time() + 1620)
        em = discord.Embed(title=f"WOAH TF!",
                           color=discord.Color.from_rgb(255, 0, 0))
        em.add_field(
            name=f"You're on a cooldown\nTry again <t:{ETA}:R> ".format(
                error.retry_after),
            value="chil the fuk out <:tfyousay:991629847707267073>")
    await ctx.send(embed=em)



@slash.slash(description="searchs gif of choice")
async def gif(ctx, *, gif):

    api_instance = giphy_client.DefaultApi()

    try:
        api_responce = api_instance.gifs_search_get(gif_key, gif, rating='R')
        lst = list(api_responce.data)
        giff = random.choice(lst)

        #await ctx.send(giff.embed_url)

    except ApiException as e:
        print("worked lol")

    em = discord.Embed(title=f"you searched for `{gif}`",
                       color=discord.Color.from_rgb(52, 97, 235))
    em.set_image(url=f'https://media.giphy.com/media/{giff.id}/giphy.gif')
    em.set_footer(text=f"Gif Link: \nhttps://giphy.com/gifs/{giff.id}")

    await ctx.send(embed=em)


@slash.slash(description="put text into a image")
async def text(ctx, *, text="say something"):
    img = Image.open("white.png")
    font = ImageFont.truetype("fart.TTF", 100)
    draw = ImageDraw.Draw(img)

    draw.text((87, 605), text, (0, 0, 0), font=font)
    img.save("text.png")

    await ctx.send(file=discord.File("text.png"))


@slash.slash(description="i fear no man")
async def fear(ctx, *, text="say something"):
    img = Image.open("fear.png")
    font = ImageFont.truetype("arial.ttf", 20)
    draw = ImageDraw.Draw(img)

    draw.text((273, 525), text, (0, 0, 0), font=font)
    img.save("man.png")

    await ctx.send(file=discord.File("man.png"))



@slash.slash(description="make your self or anyone wanted")
async def wanted(ctx, user: discord.User = None):
    if user == None:
        user = ctx.author

    img = Image.open("wanted.jpg")
    data = BytesIO(await user.avatar_url.read())
    pfp = Image.open(data)

    pfp = pfp.resize((717, 957))
    img.paste(pfp, (621, 853))

    img.save("profile.jpg")

    await ctx.send(file=discord.File("profile.jpg"))


@slash.slash(description="make any image have a rainbow border")
async def rainbow(ctx, url):
    https = 'https', 'http'
    if url.startswith(https):
        await ctx.send(f'https://some-random-api.ml/canvas/lgbt?avatar={url}')


@slash.slash(description="inverts a image")
async def invert(ctx, url):
    https = 'https', 'http'
    if url.startswith(https):
        await ctx.send(f'https://some-random-api.ml/canvas/invert?avatar={url}'
                       )




@slash.slash(description="makes any image black and white ")
async def greyscale(ctx, url):
    https = 'https', 'http'
    if url.startswith(https):
        await ctx.send(
            f'https://some-random-api.ml/canvas/greyscale?avatar={url}')


@slash.slash(description="blurs a image")
async def blur(ctx, url):
    https = 'https', 'http'
    if url.startswith(https):
        await ctx.send(
            f'https://some-random-api.ml/canvas/pixelate?avatar={url}')


@slash.slash(description="get anyones pfp")
async def avatar(ctx, user: discord.User = None):
    if user == None:
        user = ctx.author

    em = discord.Embed(title=f"`{user}`'s pfp",
                       color=discord.Color.from_rgb(47, 51, 51))
    em.set_image(url=f"{user.avatar_url}")
    await ctx.send(embed=em)


@slash.slash(description="get anyones banner, user must have a custom banner to work ( img only )")
async def banner(ctx, user: discord.User = None):
    if user == None:
        user = ctx.author
    req = await client.http.request(
        discord.http.Route("GET", "/users/{uid}", uid=user.id))
    banner_id = req["banner"]
    if banner_id:
        banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=1024.gif"

    em = discord.Embed(title=f"`{user}`'s banner",
                       color=discord.Color.from_rgb(47, 51, 51))
    em.set_image(url=f"{banner_url}")
    await ctx.send(embed=em)

  

@slash.slash(description="sends memes")
async def meme(ctx):
  async with aiohttp.ClientSession() as cs:
    async with cs.get("https://www.reddit.com/r/dankmemes.json") as r:
      memes = await r.json()

      #memeTITLE = memes["title"]

      em = discord.Embed(title = "Subreddit: *r/dankmemes*")
      em.set_image(url = memes['data']['children'][random.randint(0, 30)]['data']['url']) 
      em.set_footer(text= f"! this is a temp meme command !")
      await ctx.send(embed= em)


# -- other --


@slash.slash(description="info about the bot and me")
async def info(ctx):
    em = discord.Embed(title='Info / Bot:', color=discord.Color.green())
    em.add_field(name=":information_source: `Version`:",
                 value="v5.0",
                 inline=False)
    em.add_field(name=":computer: `Lang`:",
                 value="discord.py [ v1.7.3 ]",
                 inline=False)

    em.add_field(
        name=":notepad_spiral: `Credits`:",
        value=
        "coder: ***TR ASH#7081***,\npfp: ***Ak needs help#1874***\ntesters: ***Teh llama#3430***, ***ali.mp4#2925***, ***fat glob of meat#5919***",
        inline=False)
    em.add_field(name="💬 `support server`:",
                 value="https://discord.gg/TkJhJBMQkQ",
                 inline=False)
    em.add_field(name="<:rept:1033530866099560449> `Source code`:",
                 value="https://replit.com/@tr-ash/WS#main.py",
                 inline=False)

    #----------------------------------------------------------------
    em2 = discord.Embed(title='Info / Me:', color=discord.Color.green())
    em2.add_field(name="<:github:1028443531351687168> `Github`:",
                  value="https://github.com/TR-ASHcoder",
                  inline=False)
    em2.add_field(name="<:youtube:1028444539008077946> `Youtube`:",
                  value="https://www.youtube.com/@TR_ASH__/",
                  inline=False)
    em2.add_field(name="<:twat:1044927223171387402> `Twitter`:",
                  value="https://twitter.com/TR_ASH____",
                  inline=False)
    em2.add_field(name="<:insta:1045064248763617432> `insta`:",
                  value="https://www.instagram.com/tr___ash___/",
                  inline=False)
    em2.add_field(name="<:web:1028445187866890250> `Website`:",
                  value="https://myshittylinkssite.netlify.app/",
                  inline=False)
    em2.add_field(name="<:steam:1028445587290476684> `Steam`:",
                  value="https://steamcommunity.com/id/TRASSS/",
                  inline=False)

    paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx)
   # paginator.add_reaction('⏮️', "first")
    paginator.add_reaction('⏪', "back")
    paginator.add_reaction('⏩', "next")
    #paginator.add_reaction('⏭️', "last")
    embeds = [em, em2]
    await paginator.run(embeds)

@slash.slash(description="get the full list of commands")
async def help(ctx):
  await ctx.send("https://wordcommands.netlify.app/")
    





keep_alive.keep_alive()
try:
  client.run(os.environ['TOKEN'])
except discord.errors.HTTPException:
  print("client has died\nrestarting now lol")
  os.system('kill 1')
  os.system('python restarter.py')
  