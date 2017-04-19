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
    currentPlayer = 0

    def __init__(self, ps):
        self.playlists = ps
        self.queue = []

    def enqueue(self, song):
        for link in re.findall('^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$', song):
            strLink = ''.join(link)
            self.queue.append(strLink)

    def dequeue(self):
        if len(self.queue) == 0:
            return ""

        song = self.queue[0]
        self.queue.remove(song)
        return song

    async def playsong(self, chan):
        while True:
            if self.player != None and not self.player.is_done():
                self.player.stop()

            if len(self.queue) == 0:
                playlist = self.playlists.getCurrentPlaylist()
                song = playlist.getNextSong()
            else:
                song = self.dequeue()

            self.currentPlayer+=1
            num = self.currentPlayer

            self.player = await self.voice.create_ytdl_player(song)
            self.player.volume = self.volume
            await client.send_message(chan, "Now playing: "+self.player.title)
            self.player.start()

            await asyncio.sleep(self.player.duration)
            while not self.player.is_done():
                if num != self.currentPlayer:
                    break
                await asyncio.sleep(2)

            if self.autoplay == False or num != self.currentPlayer:
                break

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
