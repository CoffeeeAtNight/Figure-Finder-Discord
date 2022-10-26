# bot.py
# Imports
import os
import this
import discord
import requests
from storage import Storage
from dotenv import load_dotenv
from discord.ext import commands
from bs4 import BeautifulSoup

# General configurations
load_dotenv()
storage = Storage()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client(intents=discord.Intents.all())
client = commands.Bot(intents=discord.Intents.all(), command_prefix="?")

# Inital console print
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

### Maybe let user toggle the sites between FIGUYA and ALLBLUE later on
### 

@client.command()
async def search(ctx, searchTerm, page):
    if(page is ""):
        page = "1"

    URL = f"{storage.targetUrl}{searchTerm}&p={page}"
    print(f"Request for: {URL}")
    website = requests.get(URL)
    results = BeautifulSoup(website.content, 'html.parser')     # Parse response to an usable object

    figureEmbeds = startFigureFetch(results)                     # Get the figures from the Website

    await ctx.send("Did it!")
    for singleEmbed in figureEmbeds:
        await ctx.send(embed = singleEmbed)


def startFigureFetch(results):
    figureEmbeds = []

    productBoxes = results.find_all('div', class_= storage.productBox)

    for productBox in productBoxes:
        ###### Figure Image ######
        figureImg = (productBox.find('span', class_= storage.productImg).find('img'))
        currentFigureImgUrl = buildImgSource(figureImg)
        if(currentFigureImgUrl is "skip"):
           continue
            
        ###### Generals ######
        figureName = (productBox.find('span', class_= storage.productTitle).text)
        figurePrice = (productBox.find('span', class_= storage.productPrice).text)
        figurePriceFiltered = figurePrice[:figurePrice.index("€")] + "€"
        
        ###### Figure Status ######

        figureEmbeds.append(buildEmbedForFigure(figureName, currentFigureImgUrl, figurePriceFiltered))
        
    return figureEmbeds
        

def buildEmbedForFigure(figureName, figureImg, figurePrice):
    embed = discord.Embed(
                title = figureName, 
                color = 0xF8C8DC,
            )

    embed.add_field(
                name = f'Price {figurePrice}', 
                value = '—————————————————', 
                inline = False
            )
    embed.add_field(
                name = 'Status', 
                value = 'Test', 
                inline = True
            )

    embed.set_image(url = figureImg)

    return embed


### Helper functions
def buildImgSource(figureImg):
    if(figureImg.get('srcset') is not None):
        imgUrl = extractFirstSourceSetUrl(figureImg.get('srcset'))
    elif(figureImg.get('src') is not None):
        if(not figureImg.get('src').startswith('/')):
            imgUrl = figureImg.get('src')
        else:
            imgUrl = 'skip'
    else: 
        imgUrl = 'skip'
    
    return imgUrl

def extractFirstSourceSetUrl(sourceUrl):
    resultUrl = sourceUrl[:sourceUrl.index(",")]
    return resultUrl




client.run(TOKEN)
