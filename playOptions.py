import asyncio
import os
import time
import yt_dlp as yt_dlp
import discord
from pytube import Playlist
songsList = []

# download audio function
async def download_audio_only(url,output_file):
   
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': "music/1.mp3",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        if os.path.exists(output_file):
            os.remove(output_file)
        await ydl.download([url])

   
# download function
async def Download(link):
    try:
        video_url = link
        audio_folder = "music" 
        if not os.path.exists(audio_folder):
            os.makedirs(audio_folder)
        output_file = os.path.join(audio_folder, "1.mp3")

        await download_audio_only(video_url,output_file)
    except:
        print("An error has occurred")
    print("Download is completed successfully")


#functions for the buttons
async def pauseSong(id,players):
    botConnected:discord.VoiceClient = players[id] 
    botConnected.pause()

async def resumeSong(id,players):
    botConnected:discord.VoiceClient = players[id] 
    botConnected.resume()

async def stopSong(id,players):
    botConnected:discord.VoiceClient = players[id] 
    botConnected.stop()
    await botConnected.disconnect()
    
async def playNext(id,players):
    botConnected:discord.VoiceClient = players[id] 
    botConnected.stop()
    
async def playOne(ctx,players,url):
    
    await ctx.send("connecting... please wait")
    channel = ctx.message.author.voice.channel
    botConnected:discord.VoiceClient= None

    if(len(players)==0):
        botConnected = await channel.connect()
        players[channel.id] = botConnected
    else:
        botConnected = players[channel.id]
    
    if(botConnected.is_playing()):
        await ctx.send(f"song added to the queue position {len(songsList)}")
    else:
        await play(ctx=ctx,botConnected=botConnected)
  
    view = discord.ui.View()
    button = discord.ui.Button(label="resume")
    button2 = discord.ui.Button(label="pause")
    button3 = discord.ui.Button(label="stop")
    button4 = discord.ui.Button(label="next")
    button5 = discord.ui.Button(label="show queue")

    view.add_item(button)
    view.add_item(button2)
    view.add_item(button3)
    view.add_item(button4)
    view.add_item(button5)

    async def pause(interaction):
        await interaction.response.send_message(f"pausing...")
        await pauseSong(channel.id,players)
    button2.callback = pause;  

    async def resume(interaction):
        await interaction.response.send_message(f"resuming...")
        await resumeSong(channel.id,players)
    button.callback = resume;  

    async def stop(interaction):
        await interaction.response.send_message(f"stoping...")
        await stopSong(channel.id,players)
    button3.callback = stop; 

    async def next(interaction):
        await interaction.response.send_message(f"playing next song...")
        await playNext(channel.id,players)
    button4.callback = next;  

    async def queue(interaction):
        await showQueue(ctx=ctx)
    button5.callback = queue;  

    await ctx.send(view=view)

async def playAll(ctx,players,url):
    p = Playlist(url=url)
    for url in p:
        songsList.append(url)
    await playOne(ctx=ctx,players=players,url=songsList[0])


def popAndPlay(ctx,botConnected:discord.VoiceClient,source):
    discord.FFmpegPCMAudio.cleanup(source)
    songsList.pop(0)
    print(songsList)
    if(songsList):
        corno = play(ctx=ctx,botConnected=botConnected)
        playnext = asyncio.run_coroutine_threadsafe(coro=corno,loop=botConnected.loop)
        try:
            playnext.result()
        except:
            pass
    else:
        botConnected.stop()

    return "Async function completed!"

async def play(ctx,botConnected:discord.VoiceClient):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    await ctx.send("downloading... please wait")
    await Download(songsList[0])
    await ctx.send("playing... please wait")
    source = discord.FFmpegPCMAudio("./music/1.mp3")
    botConnected.play(source,after=lambda e: popAndPlay(ctx=ctx,botConnected=botConnected,source=source))

async def nextPlay(ctx,botConnected:discord.VoiceClient):
    botConnected.stop()

async def showQueue(ctx):
    await ctx.send("!!ALL SONGS IN THE QUEUE:!!")
    for song in songsList:
        await ctx.send(f"o- {song}")
        