import discord
import asyncio
import datetime
import re
import pickle
import youtube_dl

def dump(obj):
    for attr in dir(obj):
        print("obj.%s = %s" % (attr, getattr(obj, attr)))

class Playlist:
    def __init__(self, name):
        self.name = name
        self.songs = []
        self.num = 0

    def addSong(self, link):
        for link in re.findall('^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$', link):
            strLink = ''.join(link)
            if strLink not in self.songs:
                self.songs.append(strLink)

    def addSongs(self, links):
        for link in links:
            self.addSong(link)

    def getSongs(self):
        strSongs = "Songs"
        for song in self.songs:
            strSongs += "\n" + song
        return strSongs

    def getNumSongs(self):
        return len(self.songs)

    def getNextSong(self):
        if self.num == self.getNumSongs():
            self.num = 0
        self.num+=1
        return self.songs[self.num-1]

    def removeCurrentSong(self):
        self.songs.remove(self.songs[self.num-1])

'''
   Player class contains the voice connection and ytdl player.
   Playlists is a list of playlist classes
   Autoplay will automatically play new songs if the old one is done when turned on
   Enqueueing a song will play the song after the current song is done playing,
    clearing the queue as quick as possible
'''
class Player:
    voice = None
    player = None
    playlists = None
    volume = 1
    autoplay = False

    def __init__(self, ps):
        self.playlists = ps
        self.queue = []

    def enqueue(self, song):
<<<<<<< HEAD
        for link in re.findall('^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$', song):
            strLink = ''.join(link)
            self.queue.append(strLink)

    def dequeue(self):
=======
        self.queue.append(song)

    def dequeue(self, song):
>>>>>>> 018eed4a831ac1814541251632cced68bd1a06cc
        if len(self.queue) == 0:
            return ""

        song = self.queue[0]
        self.queue.remove(song)
        return song

    async def playsong(self, chan):
        while True:
            if player.player != None and not player.player.is_done():
                player.player.stop()

            if len(self.queue) == 0:
                playlist = self.playlists.getCurrentPlaylist()
                song = playlist.getNextSong()
            else:
                song = self.dequeue()

<<<<<<< HEAD
            self.player = await self.voice.create_ytdl_player(song)
            self.player.volume = self.volume

            await client.send_message(chan, "Now playing: "+self.player.title)
            self.player.start()

            #hoi
            print("test")

            await asyncio.sleep(self.player.duration)
            while not self.player.is_done():
                await asyncio.sleep(2)
=======
            await client.send_message(chan, "Now playing "+song)

            self.player = await self.voice.create_ytdl_player(song)
            self.player.volume = self.volume
            self.player.start()

            await asyncio.sleep(self.player.duration)
>>>>>>> 018eed4a831ac1814541251632cced68bd1a06cc

            if self.autoplay == False:
                break

<<<<<<< HEAD

=======
>>>>>>> 018eed4a831ac1814541251632cced68bd1a06cc
class Playlists:
    def __init__(self):
        self.currentPlaylist = None
        self.playlists = []

    def addPlaylist(self, playlist):
        self.playlists.append(playlist)

    def findPlaylist(self, name):
        for playlist in self.playlists:
            if playlist.name == name:
                return playlist
        return None

    def getPlaylists(self):
        lists = "Playlists:"
        for playlist in self.playlists:
            lists += "\n" + playlist.name
        return lists

    def getCurrentPlaylist(self):
        if self.currentPlaylist == None:
            return None
        return self.findPlaylist(self.currentPlaylist)

    def addSong(self, song):
        playlist = self.findPlaylist(self.currentPlaylist)
        if playlist != None:
            playlist.addSong(song)

lastUpdate = 0
client = discord.Client()
player = Player(Playlists())

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
async def on_message(message):

    if message.content.startswith('!quit'):
        with open('playlist', 'wb') as output:
            pickle.dump(player.playlists, output, pickle.HIGHEST_PROTOCOL)

    elif message.content.startswith('!lists'):
        await client.send_message(message.channel, player.playlists.getPlaylists())

    elif message.content.startswith('!songs'):
        if player.playlists.currentPlaylist == None:
            await client.send_message(message.channel, 'No playlist selected')
            return

        await client.send_message(message.channel, player.playlists.getCurrentPlaylist().getSongs())

    elif message.content.startswith('!pause'):
<<<<<<< HEAD
        player.player.pause()

    elif message.content.startswith('!unpause'):
        player.player.resume()

    elif message.content.startswith('!queue'):
        arr = message.content.split()
        if len(arr) != 2:
            await client.send_message(message.channel, 'Invalid syntax: !enqueue <yt-url>')
            return
        player.enqueue(arr[1])

    elif message.content.startswith('!join'):
        await join_user_channel(message.channel, message.author)
=======
        print("TODO: Pausing")

    elif message.content.startswith('!unpause'):
        print("TODO: Unpausing")

    elif message.content.startswith('!join'):
        join_user_channel(message.channel, message.author)
>>>>>>> 018eed4a831ac1814541251632cced68bd1a06cc

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
<<<<<<< HEAD
    client.run(f.readline().strip(), f.readline().strip())
=======
    client.run(f.readline(), f.readline())
>>>>>>> 018eed4a831ac1814541251632cced68bd1a06cc
