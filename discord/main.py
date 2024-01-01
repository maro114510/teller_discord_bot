
import requests
import os
from io import StringIO
from datetime import datetime, timedelta
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
TELLER_TOKEN = os.getenv("TELLER_TOKEN")
HORI_WEBHOOK= os.getenv("HORI_WEBHOOK")
TEST_WEBHOOK_URL = os.getenv("TEST_WEBHOOK")

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
	print("Bot is ready!")

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
			TEST_WEBHOOK_URL,
			json={
				"content": msg,
			}
		)
		if res.status_code != 204:
			print("Error: ", res.status_code)
		elif res.status_code == 204:
			print("Success")
		#--- end of if ---
	#--- end of loop ---
#--- end of def ---

bot.run(TELLER_TOKEN)
