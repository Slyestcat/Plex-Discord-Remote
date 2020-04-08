import os
import asyncio
import plexapi
import discord

from discord.ext import commands
from plexapi.server import PlexServer
baseurl = 'http://192.168.1.149:32400'
token = 'XC9BUftGQAfynjnqSg9u'
plex = PlexServer(baseurl, token)

TOKEN = 'Njk2ODI1MTYyMDIwMTU5NTcx.XousXg.fjvr47F4hFYLDvkTf6MXuEr_gVY'
   
bot = commands.Bot(command_prefix='$')

plexClient = "OSRSWIN10"
roleID = 697273095769292900

def pred(m):
    return m.author == message.author and m.channel == message.channel

@bot.command(name='pause', help='Pauses the currently playing movie')
@commands.has_any_role(*[roleID]) 
async def pause(ctx):
    client = plex.client(plexClient)
    client.pause()
    
@bot.command(name='resume', help='Resumes the currently playing movie')
@commands.has_any_role(*[roleID]) 
async def resume(ctx):
    client = plex.client(plexClient)
    client.play()
    
@bot.command(name='stop', help='Stops the currently playing movie')
@commands.has_any_role(*[roleID]) 
async def stop(ctx):
    client = plex.client(plexClient)
    client.stop()
    
@bot.command(name='previous', help='Returns to the previous title')
@commands.has_any_role(*[roleID]) 
async def previous(ctx):
    client = plex.client(plexClient)
    client.skipPrevious()

@bot.command(name='next', help='Skips to the next title')
@commands.has_any_role(*[roleID])
async def next(ctx):
    client = plex.client(plexClient)
    client.skipNext()
    
@bot.command(name='fastforward', help='Skips to the next title')
@commands.has_any_role(*[roleID]) 
async def fastforward(ctx):
    client = plex.client(plexClient)
    client.stepForward()
    
@bot.command(name='rewind', help='Skips to the next title')
@commands.has_any_role(*[roleID]) 
async def rewind(ctx):
    client = plex.client(plexClient)
    client.stepBack()
 
@bot.command(name='play', help='Plays a movie')
async def play(ctx, movie_title = None):
    if movie_title is None:
        await ctx.send("Please follow the syntax `$search <title>`")
    else:
        searchlist = []
        searchlistFormatted = []
        movies = plex.library.section('Movies')
        for video in movies.search(movie_title):
            searchlist.append(video.title)
        if not searchlist:
            await ctx.send("**Cannot find a title containing** `" + movie_title + "`")
        else:
            for i, item in enumerate(searchlist,1):
                searchlistFormatted.append(str(i) + '. ' + item)
            await ctx.send("**Available Titles, select the number of the corresponding title to play**" + '\n' + "```" + '\n'.join(map(str, searchlistFormatted)) + "```")
            try:
                msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60.0)
            except asyncio.TimeoutError:
                await ctx.send('**You took too long...**')
            else:
                movieNum = int(msg.content) - 1
                client = plex.client(plexClient)
                cars = plex.library.section('Movies').get(searchlist[movieNum])
                client.playMedia(cars)
                await ctx.send("**Playing Movie:** *" + searchlist[movieNum] + "*")
            
        
@bot.command(name='search', help='Searches for a movie')
@commands.has_any_role(*[roleID])
async def search(ctx, movie_title = None):
    if movie_title is None:
        await ctx.send("Please follow the syntax `$search <title>`")
    else:
        searchlist = []
        searchlistFormatted = []
        movies = plex.library.section('Movies')
        for video in movies.search(movie_title):
            searchlist.append(video.title)
        if not searchlist:
            await ctx.send("**Cannot find a title containing** `" + movie_title + "`")
        else:
            for i, item in enumerate(searchlist,1):
                searchlistFormatted.append(str(i) + '. ' + item)
            await ctx.send("**Available Titles**" + '\n' + "```" + '\n'.join(map(str, searchlistFormatted)) + "```")


@bot.command(name='clients', help='Lists all connected clients')
@commands.has_any_role(*[roleID])
async def search(ctx):
    searchlist = []
    for client in plex.clients():
        searchlist.append(client.title)
    if not searchlist:
        await ctx.send("**Cannot find clients**")
    else:
        await ctx.send("**Available Clients**" + '\n' + "```" + '\n'.join(map(str, searchlist)) + "```")


bot.run(TOKEN)
