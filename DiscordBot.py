import discord
import os
from random import randint
from discord.ext import commands
from discord.utils import get


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
    
@bot.slash_command(name = 'createthread',description = 'Create a thread')
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
bot.run('MTAwNDMyNzg5NjA5OTMyODA0MA.GtpEqb.udTsYPXYORPpCaBLPx1c-7UwtY56-aV2qzzJhc')


    