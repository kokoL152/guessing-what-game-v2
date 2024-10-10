import discord
from discord.ext import commands
import random
import asyncio
import requests
from dotenv import load_dotenv
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

words = ['cat', 'dog', 'house', 'car', 'tree', 'sun', 'moon', 'book', 'chair', 'table']
game_in_progress = False

@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}')

@bot.command()
async def startgame(ctx):
    global game_in_progress
    if game_in_progress:
        await ctx.send("A game is already in progress!")
        return

    game_in_progress = True
    word_to_draw = random.choice(words)
    await ctx.send(f"New game started! The word to draw is: {word_to_draw}")
    await ctx.send("Use this link to draw: http://127.0.0.1:5000/")

    # Set a timer for 60 seconds
    await asyncio.sleep(60)

    await ctx.send("Time's up! The round is over.")
    game_in_progress = False

@bot.command()
async def guess(ctx, word: str):
    global game_in_progress
    if not game_in_progress:
        await ctx.send("No game is currently in progress. Start a new game with !startgame")
        return

    if word.lower() == word_to_draw.lower():
        await ctx.send(f"Congratulations {ctx.author.mention}! You guessed the word correctly!")
        game_in_progress = False
    else:
        await ctx.send("Sorry, that's not the correct word. Keep guessing!")


# Run the bot with your token
load_dotenv()
token = os.getenv("MY_VARIABLE")
bot.run(token)

