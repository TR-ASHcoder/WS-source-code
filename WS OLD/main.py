
#╔═══╗╔╗   ╔═══╗    ╔══╗ ╔╗ ╔╗╔══╗╔╗   ╔═══╗
#║╔═╗║║║   ╚╗╔╗║    ║╔╗║ ║║ ║║╚╣╠╝║║   ╚╗╔╗║
#║║ ║║║║    ║║║║    ║╚╝╚╗║║ ║║ ║║ ║║    ║║║║
#║║ ║║║║ ╔╗ ║║║║    ║╔═╗║║║ ║║ ║║ ║║ ╔╗ ║║║║
#║╚═╝║║╚═╝║╔╝╚╝║    ║╚═╝║║╚═╝║╔╣╠╗║╚═╝║╔╝╚╝║
#╚═══╝╚═══╝╚═══╝    ╚═══╝╚═══╝╚══╝╚═══╝╚═══╝



import keep_alive
import requests
import discord
from discord.ext import commands
import os
#import aiohttp
import random
from googleapiclient.discovery import build
import giphy_client
from giphy_client.rest import ApiException
import urllib
import json
from PIL import Image, ImageFont, ImageDraw 
from io import BytesIO
import azapi

#from discord_slash import SlashCommand 

intents = discord.Intents.default()
intents.message_content = True


gif_key = os.environ['GIF KEY']
api_key = os.environ['KEY']
client = commands.Bot(command_prefix='!', intents=intents)
client.remove_command("help")


@client.event
async def on_ready():
    print('online')
    await client.change_presence(activity=discord.Game(name="in beta forever"))


# ---- COMMANDS ----





@client.command()
async def dog(ctx):
  r = requests.get("https://dog.ceo/api/breeds/image/random")
  res = r.json()

  
  em = discord.Embed(title="your dog  🐶", color=discord.Color.from_rgb(112, 65, 0))
  em.set_image(url=res['message'])
  await ctx.reply(embed = em, mention_author=False)


@client.command()
async def cat(ctx):
  r = requests.get("https://aws.random.cat/meow")
  res = r.json()

  
  
  em = discord.Embed(title="your cat  😺", color=discord.Color.from_rgb(223, 5, 235))
  em.set_image(url=res['file'])
  await ctx.reply(embed = em, mention_author=False)


@client.command()
@commands.cooldown(3,1620, commands.BucketType.user)
async def search(ctx, *, search):
  ran = random.randint(-1,9)
  resourse = build("customsearch","v1",developerKey= api_key).cse()
  
  result = resourse.list(q=f"{search}", cx="b37d65f91159a5de4",searchType="image").execute()
  url = result["items"][ran]["link"]
  
  
  
  em = discord.Embed(title=f"you searched for __*{search.title()}*__", color=discord.Color.from_rgb(0, 255, 58))
  em.set_image(url=url)
  em.set_footer(text= f"Image Link: \n{url}")
  await ctx.reply(embed = em, mention_author=False)

@search.error
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
      em = discord.Embed(title=f"WOAH TF!",
        color=discord.Color.from_rgb(255, 0, 0))
      em.add_field(name="You're on a cooldown\nTry again in `{:.1f}` seconds".format(error.retry_after),
      value="chil the fuk out <:tfyousay:991629847707267073>")
  await ctx.send(embed=em)



@client.command()
async def gif(ctx, *,q="PENIS"):

  api_instance = giphy_client.DefaultApi()

  try:
    api_responce = api_instance.gifs_search_get(gif_key, q, rating='r')
    lst = list(api_responce.data)
    giff = random.choice(lst)

    #await ctx.send(giff.embed_url)

  except ApiException as e:
    print("worked lol")


  
  
  em = discord.Embed(title=f"you searched for *__{q}__*",color=discord.Color.from_rgb(52, 97, 235))
  em.set_image(url=f'https://media.giphy.com/media/{giff.id}/giphy.gif')
  em.set_footer(text= f"Gif Link: \nhttps://giphy.com/gifs/{giff.id}")
  
  await ctx.reply(embed = em, mention_author=False)



@client.command()
async def text(ctx, *, text = "i like gay black men kissing"):
  img = Image.open("white.png")
  font = ImageFont.truetype("fart.TTF", 100)
  draw = ImageDraw.Draw(img)


  draw.text((87,605), text, (0,0,0), font=font)
  img.save("text.png")

  await ctx.reply(file = discord.File("text.png"), mention_author=False)


@client.command()
async def wanted(ctx, user: discord.User = None):
  if user == None:
    user = ctx.author

  img = Image.open("wanted.jpg")
  data = BytesIO(await user.display_avatar.read())
  pfp = Image.open(data)

  pfp = pfp.resize((717,957))
  img.paste(pfp, (621,853))
  
  img.save("profile.jpg")

  await ctx.reply(file = discord.File("profile.jpg"), mention_author=False)





@client.command()
async def meme(ctx):
  
  memeAPI = urllib.request.urlopen('https://meme-api.com/gimme')
  memeData = json.load(memeAPI)

  memeUrl = memeData['url']
  memeName = memeData['title']
  memePoster = memeData['author']
  memeSub = memeData['subreddit']
  memeLink = memeData['postLink']

  em = discord.Embed(title = memeName, url = 
 memeLink)
  em.set_image(url = memeUrl) 
  em.set_footer(text= f"Meme by: {memePoster}  |  Subreddit: {memeSub} ")
  await ctx.reply(embed= em, mention_author=False)


  

# ---- HELP ----


@client.command(aliases = ['HELP','hep','h','H'])
async def help(ctx):
  em = discord.Embed(title = "commands:", color=discord.Color.from_rgb(0, 255, 58))
  em.add_field(name = "`search:` ( has 27 min slowdown ) ", value = "searchs image of choice, eg: __!search {*image of choice*}__", inline=False)
  em.add_field(name = "`gif:`", value = "searchs gif of choice, eg: __!gif {*gif of choice*}__", inline=False)
  em.add_field(name = "`text:`", value = "put text into a image, eg: __!text {*text of choice*}__ ", inline=False)
  em.add_field(name = "`wanted:`", value = "make anyone wanted, eg: __!wanted {*@someone*}__", inline=False)
  em.add_field(name = "`cat:`", value = "sends cats", inline=False)
  em.add_field(name = "`dog:`", value = "sends dogs", inline=False)
  em.add_field(name = "`meme:`", value = "sends memes", inline=False)



  await ctx.send(embed=em)






@client.command(aliases = ['Q','q'])
async def quota(ctx):
  await ctx.send("check it nerrrrrddd")
  await ctx.send("||https://console.cloud.google.com/apis/api/customsearch.googleapis.com/quotas?project=ws12345&pageState=(%22allQuotasTable%22:(%22f%22:%22%255B%255D%22,%22s%22:%5B(%22i%22:%22effectiveLimit%22,%22s%22:%220%22),(%22i%22:%22currentPercent%22,%22s%22:%221%22),(%22i%22:%22sevenDayPeakPercent%22,%22s%22:%220%22),(%22i%22:%22currentUsage%22,%22s%22:%221%22),(%22i%22:%22sevenDayPeakUsage%22,%22s%22:%220%22),(%22i%22:%22serviceTitle%22,%22s%22:%220%22),(%22i%22:%22displayName%22,%22s%22:%220%22),(%22i%22:%22displayDimensions%22,%22s%22:%220%22)%5D))||")
  


keep_alive.keep_alive()
#
try:
  client.run(os.environ['TOKEN'])
except discord.errors.HTTPException:
  print("client has died\nrestarting now lol")
  os.system('kill 1')
  os.system('python restarter.py')
  