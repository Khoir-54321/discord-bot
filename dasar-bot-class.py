# test-bot(bot class)
# This example requires the 'members' and 'message_content' privileged intents to function.

import requests
import discord
import random
import os
from discord.ext import commands
from bot_logic import gen_pass
from logic_poke import Pokemon

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# command prefix 
bot = commands.Bot(command_prefix='$', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')  # type: ignore
    print('------')

# Addition command
@bot.command()
async def tambah(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

# Subtraction command
@bot.command()
async def kurang(ctx, left: int, right: int):
    """Subtracts the second number from the first."""
    await ctx.send(left - right)

# Multiplication command
@bot.command()
async def kali(ctx, left: int, right: int):
    """Multiplies two numbers."""
    await ctx.send(left * right)

# Division command
@bot.command()
async def bagi(ctx, left: int, right: int):
    """Divides the first number by the second."""
    if right != 0:
        await ctx.send(left / right)
    else:
        await ctx.send("Cannot divide by zero!")

# spamming word
@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)

# password generator        
@bot.command()
async def pw(ctx):
    await ctx.send(f'Kata sandi yang dihasilkan: {gen_pass(10)}')

# coinflip
@bot.command()
async def coinflip(ctx):
    num = random.randint(1, 2)
    if num == 1:
        await ctx.send('It is Head!')
    if num == 2:
        await ctx.send('It is Tail!')

# rolling dice
@bot.command()
async def dice(ctx):
    nums = random.randint(1, 6)
    await ctx.send(f'It is {nums}!')

# welcome message
@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')  # type: ignore

# Custom help command
# @bot.command()
# async def help(ctx):
#     help_message = """
#     **Available Commands:**

#     `$tambah <num1> <num2>` - Adds two numbers.
#     `$kurang <num1> <num2>` - Subtracts the second number from the first.
#     `$kali <num1> <num2>` - Multiplies two numbers.
#     `$bagi <num1> <num2>` - Divides the first number by the second.
    
#     Other commands:
#     `$repeat <times> <message>` - Repeats a message multiple times.
#     `$pw` - Generates a random password.
#     `$coinflip` - Flips a coin (Head/Tail).
#     `$dice` - Rolls a dice (1-6).
#     `$joined <member>` - Shows when a member joined.
#     """
#     await ctx.send(help_message)

# overwriting kalimat.txt
@bot.command()
async def tulis(ctx, *, my_string: str):
    with open('kalimat.txt', 'w', encoding='utf-8') as t:
        text = ""
        text += my_string
        t.write(text)
# append kalimat.txt
@bot.command()
async def tambahkan(ctx, *, my_string: str):
    with open('kalimat.txt', 'a', encoding='utf-8') as t:
        text = "\n"
        text += my_string
        t.write(text)
# reading kalimat.txt
@bot.command()
async def baca(ctx):
    with open('kalimat.txt', 'r', encoding='utf-8') as t:
        document = t.read()
        await ctx.send(document)

# random local meme image
@bot.command()
async def meme(ctx):
    img_name = random.choice(os.listdir('meme'))
    with open(f'meme/{img_name}', 'rb') as f:
    # with open(f'meme/enemies-meme.jpg', 'rb') as f:
        # Mari simpan file perpustakaan/library Discord yang dikonversi dalam variabel ini!
        picture = discord.File(f)
    await ctx.send(file=picture)
    
@bot.command()
async def animals(ctx):
    img_name = random.choice(os.listdir('animalmeme'))
    with open(f'animalmeme/{img_name}', 'rb') as f:
    # with open(f'meme/enemies-meme.jpg', 'rb') as f:
        # Mari simpan file perpustakaan/library Discord yang dikonversi dalam variabel ini!
        picture = discord.File(f)
    await ctx.send(file=picture)

# The '$go' command
@bot.command()
async def go(ctx):
    author = ctx.author.name  # Getting the name of the message's author
    # Check whether the user already has a Pokémon. If not, then...
    # if author not in Pokemon.pokemons.keys():
    pokemon = Pokemon(author)  # Creating a new Pokémon
    await ctx.send(await pokemon.info())  # Sending information about the Pokémon
    image_url = await pokemon.show_img()  # Getting the URL of the Pokémon image
    if image_url:
        embed = discord.Embed()  # Creating an embed message
        embed.set_image(url=image_url)  # Setting up the Pokémon's image
        await ctx.send(embed=embed)  # Sending an embedded message with an image
    else:
        await ctx.send("Failed to upload an image of the pokémon.")

#show local drive    
@bot.command()
async def local_drive(ctx):
    try:
      folder_path = "./files"  # Replace with the actual folder path
      files = os.listdir(folder_path)
      file_list = "\n".join(files)
      await ctx.send(f"Files in the files folder:\n{file_list}")
    except FileNotFoundError:
      await ctx.send("Folder not found.")

#show local file
@bot.command()
async def showfile(ctx, filename):
  """Sends a file as an attachment."""
  folder_path = "./files/"
  file_path = os.path.join(folder_path, filename)
  try:
    await ctx.send(file=discord.File(file_path))
  except FileNotFoundError:
    await ctx.send(f"File '{filename}' not found.")

# upload file to local computer
@bot.command()
async def simpan(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            # file_url = attachment.url  IF URL
            await attachment.save(f"./files/{file_name}")
            await ctx.send(f"Menyimpan {file_name}")
    else:
        await ctx.send("Anda lupa mengunggah :(")

# Run the bot
bot.run('MTMwNTEyMDczNjc1ODg1NzczOA.Gu-Lqx.-7VTfng_4Q-3Cyrp08IvbFZetZJcE4JHEGapMo')

