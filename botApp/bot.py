#author: Justin Yamamoto
#date: 9/11/2022
#Creates a connection to Discord: Creates an instance
#of Client, which represents a connection of Discord

import os
import discord
from dotenv import load_dotenv

from aiohttp import request

#allows your bot to actually function as a bot
#bot is a subclass of Client
from discord.ext import commands 
from discord import Embed

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') #get DISCORD_TOKEN from .env file
GUILD = os.getenv('DISCORD_GUILD') #gets DISCORD_GUILD from .env file

intents = discord.Intents.all()
#client = discord.Client(intents=intents)

#setup the bot, the command prefix is !
botObj = commands.Bot(command_prefix='!', intents = intents)

#on_ready() is called when client 
#is ready for further action 
#essentially this is what happens when the bot connects 
#it's an "event", as indicated by the client.event wrapper
#an event is something that happens on Discord that you can
#use to trigger a bot action
@botObj.event
async def on_ready():
 print(f'{botObj.user.name} has connected to Discord!') #successful connection
 
 #print all guilds the bot is in
 #uses discord.utills.get, which takes two parameters
 #where you serach, what you search for
 guild = discord.utils.get(botObj.guilds, name = GUILD)
 print(
     f'{botObj.user.name} is connected to the following guild: \n'
     f'{guild.name}(id: {guild.id})'
 
 )
 
 #get all members of the server using Discord API
 members = '\n - '.join([member.name for member in guild.members])
 print(f'Guild Members:\n - {members}')

#Calls an Animal API to get a random fact about an animal
#Animals available: Dog, Cat, Panda, Fox, Bird, Koal, Red Panda, Raccoon, Kangaroo
@botObj.command(name='fact',brief = 'use !help fact for more info', help='gets a random fact about your specificed animal (dog, cat, panda, fox, bird, koala, raccoon, kangaroo)')
async def fact(ctx, animal: str):
 if animal.lower() in ("dog", "cat", "panda", "bird", "fox", "koala", "raccoon", "kangaroo"): #animal is one of the ones listed 
  URL = f"https://some-random-api.ml/animal/{animal.lower()}" #get the appropiate api depending the animal
  async with request("GET", URL) as response:
   if response.status == 200: #200 = information found
    data = await response.json()
    embed = Embed(title=f"{animal.title()} fact", description = data["fact"]) #an Embed is a box-like area for the text
    await ctx.send(embed = embed)
   else:
    await ctx.send("API returned a {}")
 else:
  await ctx.send("That animal is not available")

#Calls an Animal API to get a random image about an animal
#Animals available: Dog, Cat, Panda, Fox, Bird, Koala
@botObj.command(name='image',brief = 'use !help image for more info', help='gets a random image about your specificed animal (dog, cat, panda, fox, bird, koala, raccoon, kangaroo)')
async def image(ctx, animal: str):
 if animal.lower() in ("dog", "cat", "panda", "fox", "koala", "raccoon", "kangaroo"): #animal is one of the ones listed 
  URL = f"https://some-random-api.ml/img/{animal.lower()}" #get the appropiate api depending the animal
  async with request("GET", URL) as response:
   if response.status == 200: #200 = information found
    data = await response.json()
    image_link = data["link"] #for images, get that data separate then link it
    embed = Embed(title=f"{animal.title()} image", description = "Image") #an Embed is a box-like area for the text / image
    embed.set_image(url = image_link)
    await ctx.send(embed = embed)
   else:
    await ctx.send("API returned a {}")

 elif animal.lower() == 'bird':
  URL = f"https://some-random-api.ml/img/birb"
  async with request("GET", URL) as response:
   if response.status == 200: #200 = information found
    data = await response.json()
    image_link = data["link"]
    embed = Embed(title="Bird Image", description = "Image") #an Embed is a box-like area for the text
    embed.set_image(url = image_link)
    await ctx.send(embed = embed)
   else:
    await ctx.send("API returned a {}")

 else:
  await ctx.send("That animal is not available")

#Here is how Discord handles errors 
@botObj.event
async def on_error(event, *args, **kwargs):
 with open('err.log', 'a') as f:
  if event == 'on_message':
   f.write(f'Unhandled message: {args[0]}\n')
  else:
   raise

botObj.run(TOKEN)
