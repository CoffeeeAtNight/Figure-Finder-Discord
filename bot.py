# bot.py
import os

import discord
import requests
from storage import Storage
from dotenv import load_dotenv
from discord.ext import commands
from bs4 import BeautifulSoup

load_dotenv()
storage = Storage()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client(intents=discord.Intents.all())
client = commands.Bot(intents=discord.Intents.all(), command_prefix="%")

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

### Change target site to FIGUYA.DE
### Maybe let user toggle the sites between FIGUYA and ALLBLUE later on
### 


@client.command()
async def fetchPage(ctx, arg):
    URL = storage.URL + arg    # Set the searching url with the given argument as query param
    website = requests.get(URL)
    results = BeautifulSoup(website.content, 'html.parser')     # Parse response to an usable object

    figureEmbeds = startFigureFetch(results)                     # Get the figures from the Website

    await ctx.send("Did it!")
    for singleEmbed in figureEmbeds:
        await ctx.send(embed = singleEmbed)

    

def startFigureFetch(results):
    figureEmbeds = []
    productBoxes = results.find_all('div', class_='product--box')

    for productBox in productBoxes:
        figureName = (productBox.find('span', class_='tooltipp'))
        figureEmbeds.append(buildEmbedForFigures(figureName.text))

    return figureEmbeds
        
    
    
    

def buildEmbedForFigures(figureName):
    embed = discord.Embed(
                title = "Found Figure:", 
                color = 0xF8C8DC,
            )

    embed.add_field(
                name = figureName, 
                value = "120.99€", 
                inline = False
            )

    embed.set_image(url = "https://www.allblue-world.de/media/image/71/6c/73/monkey-d-ruffy_600x600.jpg")

    return embed




client.run(TOKEN)
