import discord
import asyncio
import datetime
import re
import pickle

from classes import *

def dump(obj):
    for attr in dir(obj):
        print("obj.%s = %s" % (attr, getattr(obj, attr)))

client = discord.Client()
player = Player(Playlists())

async def commands_quit(message, args):
    with open('playlist', 'wb') as output:
        pickle.dump(player.playlists, output, pickle.HIGHEST_PROTOCOL)
    await client.send_message(message.channel, "Goodbye!")
    client.close()

async def commands_lists(message, args):
    await client.send_message(message.channel, player.playlists.getPlaylists())

async def commands_songs(message, args):
    if player.playlists.currentPlaylist == None:
        await client.send_message(message.channel, 'No playlist selected')
        return
    await client.send_message(message.channel, player.playlists.getCurrentPlaylist().getSongs())

async def commands_pause(message, args):
    player.player.pause()

async def commands_unpause(message, args):
    player.player.resume()

async def commands_queue(message, args):
    if len(args) != 1:
        await client.send_message(message.channel, 'Invalid syntax: !enqueue <yt-url>')
        return
    player.enqueue(args[0])


async def commands_help(message, args):
    cArr = [["!help", "Prints this message"],
            ["!quit", "Saves the playlists and quits the bot"],
            ["!lists", "Shows all the available playlists"],
            ["!songs", "Shows all the songs in the currently selected playlist"],
            ["!pause", "Pauses the song that is currently playing"],
            ["!unpause", "Resumes playing the song if it was paused"],
            ["!queue", "Will add songs to a queue, the songs in the queue will have priority over the normal playlist songs and thus play before continuing those playlist songs"],
            ["!join", "Will try to join you in a voice channel"],
            ["!next", "Will stop currently playing song and play the next one in the queue or playlist"],
            ["!volume", "Will adjust the player's volume"],
            ["!addsong", "Adds a song to the currently selected playlist"],
            ["!remove", "Removes the song currently playing from the currently selected playlist"],
            ["!autoplay", "Will automatically play the next song in the queue or playlist if the current one is finished"],
            ["!stop", "Will stop playing music, this will also disable autoplay if it was enabled"],
            ["!cpp", "Changes the currently selected playlist"]]

    helpstring = "Commands:\n\n"
    for element in cArr:
        helpstring += "***"+element[0]+"*** - "+element[1]+"\n"

    await client.send_message(message.channel, helpstring)

async def commands_join(message, args):
    if player.voice != None:
        player.voice = None

    chan = ""
    for channel in client.get_all_channels():
        for member in channel.voice_members:
            if member == message.author:
                chan = channel
                break
        if chan != "":
            break

    if chan == "":
        await client.send_message(message.channel, "Unable to join your voicechannel")
        return

    player.voice = await client.join_voice_channel(chan)

async def commands_next(message, args):
    if player.voice == None:
        await client.send_message(message.channel, 'Not connected to a voice channel.')
        return

    await player.playsong(message.channel)

async def commands_volume(message, args):
    if len(args) != 1:
        await client.send_message(message.channel, 'Invalid syntax: !volume <0-2>')
        return
    try:
        player.volume = float(args[0])
        if player.player != None:
            player.player.volume = player.volume
    except ValueError:
        await client.send_message(message.channel, 'You may only enter numerical values.')

async def commands_addsong(message, args):
    if player.playlists.currentPlaylist == None:
        await client.send_message(message.channel, 'No playlist selected')
        return

    arr = message.content.split()
    if len(args) != 1:
        await client.send_message(message.channel, 'Invalid syntax: !addsong <youtube song url>')
        return

    player.playlists.addSong(args[0])

async def commands_remove(message, args):
    player.playlists.getCurrentPlaylist().removeCurrentSong()

async def commands_autoplay(message, args):
    if player.player != None and not player.player.is_done():
        player.player.stop()

    player.autoplay = True
    await player.playsong(message.channel)

async def commands_stop(message, args):
    player.autoplay = False
    player.player.stop()

async def commands_stop(message, args):
    if len(args) != 1:
        await client.send_message(message.channel, 'Invalid syntax: !ccp <name>')
        return

    playlist = player.playlists.findPlaylist(args[0])
    if playlist == None:
        await client.send_message(message.channel, 'Creating new playlist: '+arr[1])
        player.playlists.addPlaylist(Playlist(aargs[0]))
    else:
        player.playlists.currentPlaylist = args[0]
        await client.send_message(message.channel, 'Current playlist: '+player.playlists.currentPlaylist)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    #read last updated time from file
    global lastUpdate
    file = open("lasttime", "r").readline().strip()
    print(file)
    lastUpdate = datetime.datetime.fromtimestamp(1483228800) # jan 1 2017
    if (file) != "":
        lastUpdate = datetime.datetime.strptime(file, '%Y-%m-%d')

    #read all playlists from file
    with open('playlist', 'rb') as input:
        player.playlists = pickle.load(input)

@client.event
async def on_message(message):
    msgArray = message.content.split()
    cmd = msgArray[0]
    args = msgArray[1:]

    if   cmd == '!quit':
        await commands_quit(message, args)
    elif cmd == '!lists':
        await commands_lists(message, args)
    elif cmd == '!songs':
        await commands_songs(message, args)
    elif cmd == '!pause':
        await commands_pause(message, args)
    elif cmd == '!unpause':
        await commands_unpause(message, args)
    elif cmd == '!queue':
        await commands_queue(message, args)
    elif cmd == '!help':
        await commands_help(message, args)
    elif cmd == '!join':
        await commands_join(message, args)
    elif cmd == '!next':
        await commands_next(message, args)
    elif cmd == '!volume':
        await commands_volume(message, args)
    elif cmd == '!addsong':
        await commands_addsong(message, args)
    elif cmd == '!remove':
        await commands_remove(message, args)
    elif cmd == '!autoplay':
        await commands_autoplay(message, args)
    elif cmd == '!stop':
        await commands_stop(message, args)
    elif cmd == '!ccp':
        await commands_stop(message, args)


with open('password', 'r') as f:
    email = f.readline().strip()
    passw = f.readline().strip()
    client.run(email, passw)
