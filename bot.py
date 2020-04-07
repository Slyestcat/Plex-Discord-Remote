import os
import random

import plexapi
from discord.ext import commands

from plexapi.server import PlexServer
baseurl = 'http://192.168.1.149:32400'
token = 'XC9BUftGQAfynjnqSg9u'
plex = PlexServer(baseurl, token)

TOKEN = 'Njk2ODI1MTYyMDIwMTU5NTcx.XousXg.fjvr47F4hFYLDvkTf6MXuEr_gVY'
   
bot = commands.Bot(command_prefix='$')

plexClient = "OSRSWIN10"

@bot.command(name='pause', help='Pauses the currently playing movie')
async def pause(ctx):
    client = plex.client(plexClient)
    client.pause()
    
@bot.command(name='resume', help='Resumes the currently playing movie')
async def pause(ctx):
    client = plex.client(plexClient)
    client.play()
    
@bot.command(name='stop', help='Stops the currently playing movie')
async def pause(ctx):
    client = plex.client(plexClient)
    client.stop()
    
@bot.command(name='previous', help='Returns to the previous title')
async def pause(ctx):
    client = plex.client(plexClient)
    client.skipPrevious()

@bot.command(name='next', help='Skips to the next title')
async def pause(ctx):
    client = plex.client(plexClient)
    client.skipNext()
    
@bot.command(name='fastforward', help='Skips to the next title')
async def pause(ctx):
    client = plex.client(plexClient)
    client.stepForward()
    
@bot.command(name='rewind', help='Skips to the next title')
async def pause(ctx):
    client = plex.client(plexClient)
    client.stepBack()
 
@bot.command(name='play', help='Plays a movie')
async def search(ctx, pClient, movie_title = None):
    if movie_title is None:
        await ctx.send("Please follow the syntax `$search <title>`")
    else:
        movie = plex.library.section('Movies').get(movie_title)
        client = plex.client(pClient)
        client.playMedia(movie)
        await ctx.send("**Playing Movie:** *" + movie_title + "*")
        
@bot.command(name='search', help='Searches for a movie')
async def search(ctx, movie_title = None):
    if movie_title is None:
        await ctx.send("Please follow the syntax `$search <title>`")
    else:
        searchlist = []
        movies = plex.library.section('Movies')
        for video in movies.search(movie_title):
            searchlist.append(video.title)
        if not searchlist:
            await ctx.send("**Cannot find a title containing** `" + movie_title + "`")
        else:
            await ctx.send("**Available Titles**" + '\n' + "```" + '\n'.join(map(str, searchlist)) + "```")

@bot.command(name='clients', help='Lists all connected clients')
async def search(ctx):
    searchlist = []
    for client in plex.clients():
        searchlist.append(client.title)
    if not searchlist:
        await ctx.send("**Cannot find clients**")
    else:
        await ctx.send("**Available Clients**" + '\n' + "```" + '\n'.join(map(str, searchlist)) + "```")


bot.run(TOKEN)