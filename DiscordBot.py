import discord
import os
from random import randint
from discord.ext import commands
from discord.utils import get
import youtube_dl
youtube_dl.utils.bug_reports_message = lambda: ''
import asyncio
ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

bot = discord.Bot()
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='.', intents=intents)      
random_number = randint(0,10)        


    
@bot.event
async def on_ready():
    print(f'logged in as {bot.user}')

@bot.event
async def on_member_join(member):
    await member.send(
        "https://cdn.discordapp.com/attachments/964222431571091516/1002489393640132699/out.webm"
    )
    print('sent message')
    
@bot.slash_command(name = 'hello',description = 'Say Hello')
async def hello(ctx):
    await ctx.respond('Hey!')
    
@bot.slash_command(name = 'ddos',description = 'Execute order 66')
async def test(ctx,name, amount,starting_message):
    try:
        for i in range(int(amount)):
            message = await ctx.send(starting_message)
            await message.create_thread(name = name)
    except Exception as ex:
        await ctx.respond(f'{ex.__class__.__name__} {ex.args}')
       
@bot.slash_command(name = 'guessnumber', description = 'Guess the number!')
async def gtn(ctx,guess_num):
    global random_number
    try:
        if int(guess_num) == random_number:
            await ctx.respond('Correct!')
            random_number = randint(0,10)
            print(random_number)
        else:
            await ctx.respond('Wrong number,try again!') 
    except Exception as e:
        await ctx.respond('Something went wrong')
        await ctx.respond(f'Debug info: {e.__class__.__name__}, {e.args}')     

@bot.slash_command(name = 'jointest')
async def jointest(ctx):
    try:
        await ctx.author.send(
            'https://cdn.discordapp.com/attachments/964222431571091516/1002489393640132699/out.webm'
        )
        await ctx.respond('message sent successfully')
    except Exception as e:
        await ctx.respond(f'{e.__class__.__name__} {e.args}')
        
@bot.slash_command(name = 'silentisgay', description = 'Fuck Silent')
async def sig(ctx, message,amount,user_id):
    user_id = int(user_id)
    user = bot.get_user(user_id)
    await ctx.respond(str(type(user)))
    if user:
        for i in range(int(amount)):
            print('sent successfully')
            await user.send(message)
    else:
        await ctx.respond(f'user {user_id} not found!')
        
@bot.slash_command(name = 'getid',description = 'get own id')
async def getid(ctx):
    await ctx.respond(ctx.author.id)  
    
@bot.slash_command(name = 'idtest', description = 'id test')
async def idtest(ctx):
    user = ctx.author
    await ctx.respond(f'user id: {user.id}, name: {user}') 
    
    user = get(bot.get_all_members(),id = ctx.author.id)
    if user:
        await ctx.respond(str(type(ctx.author.id)))
        await ctx.respond('user found')
    else:
        
        await ctx.respond('something went wrong') 
        
@bot.slash_command(name = 'testchannel', description = 'test')
async def testchannel(ctx,message,channelid):
    for channel in ctx.guild.channels:
        if channel.id == int(channelid):
            await channel.send(message)
        else:
            print(channel.id)
            print('wrong channel')
    
@bot.slash_command(name = 'embedtest', description = 'Embed Test')
async def embedtest(ctx):
    embed = discord.Embed(
        title = 'lorem ipsum',
        description = 'dolor sit amet',
        color = discord.Colour.blue()
    )       
    embed.add_field(name = 'lorem ipsum', value = 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia, molestiae quas vel sint commodi repudiandae consequuntur voluptatum laborum numquam blanditiis harum quisquam eius sed odit fugiat iusto fuga praesentiumoptio, eaque rerum! Provident similique accusantium nemo autem. **Veritatisobcaecati tenetur iure eius earum ut molestias architecto voluptate aliquamnihil, eveniet aliquid culpa officia aut! Impedit sit sunt quaerat, odit,tenetur error, harum nesciunt ipsum debitis quas aliquid.**', inline = False)
    embed.add_field(name = 'Inline field 1', value = 'Inline field 1', inline = True)
    embed.add_field(name = 'Inline field 2', value = 'Inline field 2', inline = True)
    embed.add_field(name = 'Inline field 3', value = 'Inline field 3', inline = True)
    embed.set_author(name = 'Dungeon Masters')
    embed.set_image(url = 'https://pbs.twimg.com/media/E1Qd9FwXoAAg911.jpg:large')
    
    await ctx.respond('Successfull', embed = embed)


@bot.slash_command(name='play_song', help='To play song')
async def play(ctx,url):
    
    try :
        server = ctx.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        await ctx.send('**Now playing:** {}'.format(filename))
    except Exception as e:
        await ctx.send(f"The bot is not connected to a voice channel. {e.__class__.__name__} {e.args}")


@bot.slash_command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.author.voice.channel
    await channel.connect()


@bot.slash_command(name='pause', help='This slash_command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")
    
@bot.slash_command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song slash_command")
    


@bot.slash_command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.slash_command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")




@bot.slash_command(name = 'whats_my_name')
async def whats_my_name(ctx) :
    await ctx.send('Hello {}'.format(ctx.author.name))

@bot.slash_command(name = 'where_am_i')
async def where_am_i(ctx):
    owner=str(ctx.guild.owner)
    region = str(ctx.guild.region)
    guild_id = str(ctx.guild.id)
    memberCount = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)
    desc=ctx.guild.description
    
    embed = discord.Embed(
        title=ctx.guild.name + " Server Information",
        description=desc,
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=guild_id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)

    await ctx.send(embed=embed)

    members=[]
    async for member in ctx.guild.fetch_members(limit=150) :
        await ctx.send('Name : {}\t Status : {}\n Joined at {}'.format(member.display_name,str(member.status),str(member.joined_at)))

