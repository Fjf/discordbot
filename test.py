import discord
import asyncio
import datetime
import re
import pickle

from classes import *
from commands import *

def dump(obj):
    for attr in dir(obj):
        print("obj.%s = %s" % (attr, getattr(obj, attr)))

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
