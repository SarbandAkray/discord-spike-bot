from dotenv import dotenv_values
import discord
from discord.ext import commands
import yt_dlp as yt_dlp
import playOptions
config = dotenv_values(".env")


#to save all bot instents in voice channels
players = {}

#creating the bot
bot = commands.Bot(command_prefix="!",intents=discord.Intents.all())
bot.remove_command("help")
token = config.get("TOKEN")



# commands
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Commands")
    embed.add_field(name="!play", value="!play (YOUTUBE URL) --> plays a youtube song", inline=False)
    embed.add_field(name="!pause", value="!pause --> pauses the song", inline=False)
    embed.add_field(name="!resume", value="!resume --> resumes a paused song", inline=False)
    embed.add_field(name="!stop", value="!stop --> stops the song and kicks it out of the channel", inline=False)
    embed.add_field(name="!next", value="!next --> plays the next song in the queue", inline=False)
    embed.add_field(name="!queue", value="!queue --> shows all the songs in the queue", inline=False)
    await ctx.send(content=None, embed=embed)

@bot.command()
async def play(ctx:commands.Context, url:str = "nothing"):
    if(url == "nothing" or "start_radio" in url):
        await ctx.send("please use !help to write the right command and dont use youtube mix please")
    else:
        if(ctx.author.voice):
            if("playlist" in url):
               await playOptions.playAll(ctx=ctx,players=players,url=url)
            else:
                playOptions.songsList.append(url)
                await playOptions.playOne(ctx=ctx,players=players,url=url)
            
        else:
            await ctx.send("plesae connect to a voice channel")

@bot.command()
async def pause(ctx:commands.Context):
    channel = ctx.message.author.voice.channel
    botConnected:discord.VoiceClient = players[channel.id] 
    botConnected.pause()
   
@bot.command()
async def resume(ctx:commands.Context):
    channel = ctx.message.author.voice.channel
    botConnected:discord.VoiceClient = players[channel.id] 
    botConnected.resume()

@bot.command()
async def stop(ctx:commands.Context):
    channel = ctx.message.author.voice.channel
    botConnected:discord.VoiceClient = players[channel.id] 
    botConnected.stop()

@bot.command()
async def next(ctx):
    channel = ctx.message.author.voice.channel
    botConnected:discord.VoiceClient = players[channel.id] 
    await playOptions.nextPlay(ctx=ctx,botConnected=botConnected)
    await ctx.send("next song is being played")


@bot.command()
async def queue(ctx):
    channel = ctx.message.author.voice.channel
    await playOptions.showQueue(ctx=ctx)

#events
@bot.event
async def on_message(message):
    # print(message.content)
    await bot.process_commands(message)

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel is None and member==bot.user:
        print("Bot has been Disconnected")
        players.clear()
        # time.sleep(2)
        # shutil.rmtree('./music/')

bot.run(token)




