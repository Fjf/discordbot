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
    await client.send_message(message.channel, '!p')

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
