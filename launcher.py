from discord.ext.commands import bot
from bot import bot
import asyncio
from signal import SIGINT, SIGTERM


VERSION = "2.0.5"

bot.run(VERSION)