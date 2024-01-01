
import requests
import os
import sys
import logging
from io import StringIO
from datetime import datetime, timedelta
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

log_filename = "logs/log_" + datetime.now().strftime("%Y%m%d") + ".logs"

if not os.path.exists("logs"):
    os.makedirs("logs")
#--- end of if ---

# logging setting
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s - %(filename)s(func:%(funcName)s, line:%(lineno)d)] %(message)s",
    encoding="utf-8",
    stream=sys.stdout
)

logger = logging.getLogger(__name__)

load_dotenv()
TELLER_TOKEN = os.getenv("TELLER_TOKEN")
HORI_WEBHOOK= os.getenv("HORI_WEBHOOK")
TEST_WEBHOOK = os.getenv("TEST_WEBHOOK")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Instantiate bot
bot = commands.Bot(
	command_prefix="$",
	case_insensitive=True,
	intents=intents
)

@bot.event
async def on_ready():
	logger.info("Bot is ready!")

@bot.command(
	name="message",
	aliases=["msg", "m"],
	description="Get messages from a channel and send them to a webhook."
)
async def get_message(ctx: commands.Context, channel: discord.TextChannel) -> None:
	"""Get messages from a channel and send them to a webhook."""

	stream = StringIO()
	messages = []

	async for message in channel.history(
		after=datetime.utcnow() - timedelta(hours=24),
		oldest_first=True,
	):
		jst = message.created_at + timedelta(hours=9)
		org_channel = channel.name
		msg = f"""{message.author.name}: {jst.strftime('%Y/%m/%d %H:%M:%S')}\n{message.content}\norigin: {org_channel}"""
		stream.write(msg)
		stream.write("\n\n")
		messages.append(msg)
	#--- end of loop ---

	stream.seek(0)
	await ctx.send(file=discord.File(stream, filename="messages.txt"))
	stream.close()

	for msg in messages:
		res = requests.post(
			TEST_WEBHOOK,
			json={
				"content": msg,
			}
		)
		if res.status_code != 204:
			logger.error("Error: ", res.status_code)
		elif res.status_code == 204:
			logger.info("Success")
		#--- end of if ---
	#--- end of loop ---
#--- end of def ---

bot.run(TELLER_TOKEN)
