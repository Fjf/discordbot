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

async def updatePlaylist(message):
    print("Checking after "+str(lastUpdate))
    async for log in client.logs_from(message.channel, limit=1000, after=lastUpdate):
        for link in re.findall('^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$', log.content):
            player.playlists.currentPlaylist.addSong(''.join(link) + "\n")

async def join_user_channel(msgchannel, user):
    if player.voice != None:
        player.voice = None

    chan = ""
    for channel in client.get_all_channels():
        for member in channel.voice_members:
            if member == user:
                chan = channel
                break
        if chan != "":
            break

    if chan == "":
        await client.send_message(msgchannel, "Unable to join your voicechannel")
        return

    player.voice = await client.join_voice_channel(chan)

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

    if message.content.startswith('!quit'):
        with open('playlist', 'wb') as output:
            pickle.dump(player.playlists, output, pickle.HIGHEST_PROTOCOL)
        await client.send_message(message.channel, "Goodbye!")
        client.close()

    elif message.content.startswith('!lists'):
        await client.send_message(message.channel, player.playlists.getPlaylists())

    elif message.content.startswith('!songs'):
        if player.playlists.currentPlaylist == None:
            await client.send_message(message.channel, 'No playlist selected')
            return

        await client.send_message(message.channel, player.playlists.getCurrentPlaylist().getSongs())

    elif message.content.startswith('!pause'):
        player.player.pause()

    elif message.content.startswith('!unpause'):
        player.player.resume()

    elif message.content.startswith('!queue'):
        arr = message.content.split()
        if len(arr) != 2:
            await client.send_message(message.channel, 'Invalid syntax: !enqueue <yt-url>')
            return
        player.enqueue(arr[1])

    elif message.content.startswith('!help'):
        await client.send_message(message.channel, '!p')


    elif message.content.startswith('!join'):
        await join_user_channel(message.channel, message.author)

    elif message.content.startswith('!next'):
        if player.voice == None:
            await client.send_message(message.channel, 'Not connected to a voice channel.')
            return

        await player.playsong(message.channel)

    elif message.content.startswith('!volume'):
        arr = message.content.split()
        if len(arr) != 2:
            await client.send_message(message.channel, 'Invalid syntax: !volume <0-2>')
            return
        try:
            player.volume = float(arr[1])
            if player.player != None:
                player.player.volume = player.volume
        except ValueError:
            await client.send_message(message.channel, 'You may only enter numerical values.')

    elif message.content.startswith('!addsong'):
        if player.playlists.currentPlaylist == None:
            await client.send_message(message.channel, 'No playlist selected')
            return

        arr = message.content.split()
        if len(arr) != 2:
            await client.send_message(message.channel, 'Invalid syntax: !addsong <youtube song url>')
            return

        player.playlists.addSong(arr[1])

    elif message.content.startswith('!remove'):
        player.playlists.getCurrentPlaylist().removeCurrentSong()

    elif message.content.startswith('!autoplay'):
        if player.player != None and not player.player.is_done():
            player.player.stop()

        player.autoplay = True
        await player.playsong(message.channel)

    elif message.content.startswith('!stop'):
        player.autoplay = False
        player.player.stop()

    #change current playlist
    elif message.content.startswith('!ccp'):
        arr = message.content.split()
        if len(arr) != 2:
            await client.send_message(message.channel, 'Invalid syntax: !ccp <name>')
            return

        playlist = player.playlists.findPlaylist(arr[1])
        if playlist == None:
            await client.send_message(message.channel, 'Creating new playlist: '+arr[1])
            player.playlists.addPlaylist(Playlist(arr[1]))
        else:
            player.playlists.currentPlaylist = arr[1]
            await client.send_message(message.channel, 'Current playlist: '+player.playlists.currentPlaylist)

with open('password', 'r') as f:
    email = f.readline().strip()
    passw = f.readline().strip()
    client.run(email, passw)
