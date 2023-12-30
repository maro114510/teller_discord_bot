
import os
from io import StringIO
from datetime import datetime, timedelta
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TELLER_TOKEN = os.getenv("TELLER_TOKEN")

intents = discord.Intents.default()
intents.members = True 
intents.message_content = True 


# Botをインスタンス化
bot = commands.Bot(
    command_prefix="$", 
    case_insensitive=True, 
    intents=intents 
)

@bot.event
async def on_ready():
    print("Bot is ready!")


@bot.command()
async def hello(ctx: commands.Context) -> None:
    """helloと返すコマンド"""
    await ctx.send(f"Hello {ctx.author.name}")

@bot.command()
async def add(ctx: commands.Context, a: int, b: int) -> None:
    """足し算をするコマンド"""
    await ctx.send(a+b)


@bot.command(
    name="message",
    aliases=["msg", "m"],
)
async def get_message(ctx: commands.Context, channel: discord.TextChannel) -> None:
    """チャンネルのメッセージを取得し、テキストファイルに保存するコマンド"""

    stream = StringIO()

    async for message in channel.history(
        after=datetime.utcnow() -timedelta(hours=1),
        oldest_first=True, 
    ):
        jst = message.created_at + timedelta(hours=9)
        msg = f"{message.author.name}: {jst.strftime('%Y/%m/%d %H:%M:%S')}\n{message.content}"
        stream.write(msg)
        stream.write("\n\n")

    stream.seek(0)
    await ctx.send(file=discord.File(stream, filename="messages.txt"))
    stream.close()

bot.run(TELLER_TOKEN)
