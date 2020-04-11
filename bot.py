import os
import asyncio
import plexapi
import discord

from discord.ext import commands
from plexapi.server import PlexServer
baseurl = 'http://192.168.1.149:32400'
token = 'XC9BUftGQAfynjnqSg9u' #TODO: set plex data in another file
plex = PlexServer(baseurl, token)

TOKEN = 'Njk2ODI1MTYyMDIwMTU5NTcx.XousXg.fjvr47F4hFYLDvkTf6MXuEr_gVY' #TODO: set bot token in another file
   
bot = commands.Bot(command_prefix='$') #TODO: switch all "$" flags to be dynamic in bot responses

plexClient = "OSRSWIN10" #TODO: set client in another file
roleID = 697273095769292900 #TODO: set roleID in another file

def pred(m):
    return m.author == message.author and m.channel == message.channel
    
def get_ms(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600000 + int(m) * 60000 + int(s) * 1000



@bot.command(name='pause', help='Pauses the currently playing movie')
@commands.has_any_role(*[roleID]) 
async def pause(ctx):
    client = plex.client(plexClient)
    client.pause()
    await ctx.send("Paused the currently playing movie.")
    
@bot.command(name='resume', help='Resumes the currently playing movie')
@commands.has_any_role(*[roleID]) 
async def resume(ctx):
    client = plex.client(plexClient)
    client.play()
    await ctx.send("Resumed the currently playing movie.")
    
@bot.command(name='stop', help='Stops the currently playing movie')
@commands.has_any_role(*[roleID]) 
async def stop(ctx):
    client = plex.client(plexClient)
    client.stop()
    await ctx.send("Stopped the currently playing movie.")
    
@bot.command(name='previous', help='Returns to the previous title in the queue')
@commands.has_any_role(*[roleID]) 
async def previous(ctx):
    client = plex.client(plexClient)
    client.skipPrevious()
    await ctx.send("Returned to the previous movie in the queue.")
    
@bot.command(name='next', help='Skips to the next title in the queue')
@commands.has_any_role(*[roleID])
async def next(ctx):
    client = plex.client(plexClient)
    client.skipNext()
    await ctx.send("Skipped to the next movie in the queue.")
    
@bot.command(name='fforward', help='Skips forward a chunk')
@commands.has_any_role(*[roleID]) 
async def fastforward(ctx,x = None):
    if x is None:
        await ctx.send("Please follow the syntax `$fforward <int>`")
    else:
        xInt = int(x)
        while (xInt > 0):
            client = plex.client(plexClient)
            client.stepForward()
            xInt = xInt - 1
        await ctx.send("Fast forwarded **" + x + "** chunks.")
        
@bot.command(name='rewind', help='Skips back a chunk')
@commands.has_any_role(*[roleID]) 
async def rewind(ctx,x = None):
    if x is None:
        await ctx.send("Please follow the syntax `$rewind <int>`")
    else:
        xInt = int(x)
        while (xInt > 0):
            client = plex.client(plexClient)
            client.stepForward()
            xInt = xInt - 1
        await ctx.send("Rewound **" + x + "** chunks.")

@bot.command(name='skipto', help='Skips to a desired time')
@commands.has_any_role(*[roleID]) 
async def rewind(ctx,x = None):
    if x is None:
        await ctx.send("Please follow the syntax `$skipto <00:00:00>`")
    else:
        try:
            client = plex.client(plexClient)
            ms = get_ms(x)
            client.seekTo(ms)
            await ctx.send("Skipped to **" + x + "**.")
        except ValueError:
            await ctx.send("Please follow the syntax `$skipto <00:00:00>`")

@bot.command(name='subtitles', help='Sets the subtitle stream, 0 is none') #TODO: Remove this command
@commands.has_any_role(*[roleID]) 
async def rewind(ctx,x):
    client = plex.client(plexClient)
    client.setSubtitleStream(x)
    await ctx.send("Enabled subtitle stream `" + x + "`")
    
@bot.command(name='getsubtitles', help='Gets the availble subtitles for the specified movie') #TODO: allow used to select subtitle stream from this command
@commands.has_any_role(*[roleID]) 
async def rewind(ctx,x = None):
    embed=discord.Embed(title="Available Subtitles", color=0x00ff08)
    embed.set_footer(text="Please use the $subtitles command to enable a subtitles stream.")
    embed2=discord.Embed(title="Available Titles", color=0x00ff08)
    embed2.set_footer(text="Please enter the number of the title you would like to see the subtitle options for.")
    if x is None:
        await ctx.send("Please follow the syntax `$getsubtitles <title>`")    
    else:
        searchlist = []
        searchlistFormatted = []
        subtitlelist = []
        movies = plex.library.section('Movies')
        for video in movies.search(x):
            searchlist.append(video.title)
        if not searchlist:
            await ctx.send("Cannot find a title containing `" + x + "`")
        else:
            for i, item in enumerate(searchlist):
                searchlistFormatted.append(str(i+1) + '. ' + item)
            embed2.add_field(name="Movies", value="```" + '\n'.join(map(str, searchlistFormatted)) + "```", inline=True)
            await ctx.send(embed=embed2)
            try:
                msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60.0)
            except asyncio.TimeoutError:
                await ctx.send('You took too long...')
            else:
                movieNum = int(msg.content)
                movies = plex.library.section("Movies")
                for movie in movies.get(searchlist[movieNum]):
                    movie = movie.reload()
                    langCode = None
                    for subtitle in movie.subtitleStreams():
                        subtitlelist.append(subtitle.id)
                        embed.add_field(name=subtitle.languageCode, value=subtitle.id, inline=True)
                if not subtitlelist:
                    await ctx.send("No subtitles availble for `" + movie.title + "`")
                else:                        
                    await ctx.send(embed=embed)               

@bot.command(name='playlist', help='Gets the availble subtitles.') #TODO: add playlist options/movie queuing
@commands.has_any_role(*[roleID]) 
async def rewind(ctx):
    for media_list in [list for list in plex.playlist('moviebot').items()]:
        print(''.join([x.file for x in media_list.iterParts()]))

@bot.command(name='play', help='Plays a movie') #TODO: add catch if movie is paused and output text to tell user to use $resume to resume the movie
async def play(ctx, movie_title = None):
    embed=discord.Embed(title="Available Titles", description="Select the number of the corresponding title to play.", color=0x00ff08)
    embed.set_footer(text="Please enter the number of the title you would like to play.")
    if movie_title is None:
        await ctx.send("Please follow the syntax `$play <title>`")    
    else:
        searchlist = []
        searchlistFormatted = []
        movies = plex.library.section('Movies')
        for video in movies.search(movie_title):
            searchlist.append(video.title)
        if not searchlist:
            await ctx.send("Cannot find a title containing `" + movie_title + "`")
        else:
            for i, item in enumerate(searchlist):
                searchlistFormatted.append(str(i+1) + '. ' + item)
            embed.add_field(name="Movies", value="```" + '\n'.join(map(str, searchlistFormatted)) + "```", inline=True)
            await ctx.send(embed=embed)
            try:
                msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60.0)
            except asyncio.TimeoutError:
                await ctx.send('You took too long...')
            else:
                movieNum = int(msg.content)
                client = plex.client(plexClient)
                cars = plex.library.section('Movies').get(searchlist[movieNum])
                client.playMedia(cars)
                embed2=discord.Embed(title=searchlist[movieNum], description="is now playing", color=0xffdd00)
                await ctx.send(embed=embed2)

@bot.command(name='search', help='Searches for a movie') #TODO: add request command that ties into radarr/sonarr
@commands.has_any_role(*[roleID])
async def search(ctx, movie_title = None):
    embed=discord.Embed(title="Available Titles", description="Currently available titles.", color=0x00ff08)
    if movie_title is None:
        await ctx.send("Please follow the syntax `$search <title>`")
    else:
        searchlist = []
        searchlistFormatted = []
        movies = plex.library.section('Movies')
        for video in movies.search(movie_title):
            searchlist.append(video.title)
        if not searchlist:
            await ctx.send("Cannot find a title containing `" + movie_title + "`")
        else:
            for i, item in enumerate(searchlist):
                searchlistFormatted.append(str(i+1) + '. ' + item)
        embed.add_field(name="Movies", value="```" + '\n'.join(map(str, searchlistFormatted[0:10])) + "```", inline=True)
        await ctx.send(embed=embed)

@bot.command(name='recentlyadded', help='Outputs the recently added movies') #TODO: add latest release titles (ie last 10 movies from 2020)
@commands.has_any_role(*[roleID])
async def search(ctx):
    embed=discord.Embed(title="Recently Added Titles", description="10 most recently added titles to the plex server.", color=0x00ff08)
    searchlist = []
    searchlistFormatted = []
    movies = plex.library.section('Movies')
    for video in movies.recentlyAdded():
        searchlist.append(video.title)
    else:
        for i, item in enumerate(searchlist):
            searchlistFormatted.append(str(i+1) + '. ' + item)
        embed.add_field(name="Movies", value="```" + '\n'.join(map(str, searchlistFormatted[0:10])) + "```", inline=True)
        await ctx.send(embed=embed)

@bot.command(name='reload', help='Reloads the plex client') #TODO: figure out what this actually does
@commands.has_any_role(*[roleID]) 
async def rewind(ctx):
    client = plex.client(plexClient)
    client.reload()
    
    
# @bot.command(name='clients', help='Lists all connected clients') #debugging command
# @commands.has_any_role(*[roleID])
# async def search(ctx):
    # searchlist = []
    # for client in plex.sessions():
        # searchlist.append(client.title)
    # if not searchlist:
        # await ctx.send("**Cannot find clients**")
    # else:
        # await ctx.send("**Available Clients**" + '\n' + "```" + '\n'.join(map(str, searchlist)) + "```")


bot.run(TOKEN)
