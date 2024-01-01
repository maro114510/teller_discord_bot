
import requests
import os
from datetime import datetime, timedelta, time
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

from src.libs.log_init import LogSetting

log_filename = "logs/log_" + datetime.now().strftime("%Y%m%d") + ".log"

if not os.path.exists("logs"):
	os.makedirs("logs")
#--- end of if ---

logger = LogSetting(log_filename).log_init()

load_dotenv()
TELLER_TOKEN = os.getenv("TELLER_TOKEN")
HORI_WEBHOOK= os.getenv("HORI_WEBHOOK")
TEST_WEBHOOK = os.getenv("TEST_WEBHOOK")
CHANNEL_IDS = os.getenv("CHANNEL_IDS").split(",")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(
	intents=intents
)

@client.event
async def on_ready():
	auto_backup.start()
	logger.info("Client is ready!")

times = [
	time(hour=0),
	time(hour=12),
]

#@tasks.loop(seconds=10)
@tasks.loop(time=times)
async def auto_backup() -> None:
	messages = []

	channels = []
	for id in CHANNEL_IDS:
		c = client.get_channel(id)
		channels.append(c)
	#--- end of loop ---

	if channels[0] is None:
		logger.error("No channels")
		return
	#--- end of if ---

	logger.info(channels)

	for channel in channels:
		async for message in channel.history(
			after=datetime.utcnow() - timedelta(hours=12),
			oldest_first=True,
		):
			jst = message.created_at + timedelta(hours=9)
			org_channel = channel.name
			msg = f"""{message.author.name}: {jst.strftime('%Y/%m/%d %H:%M:%S')}\n{message.content}\norigin: {org_channel}"""
			messages.append(msg)
		#--- end of loop ---
	#--- end of loop ---

	if len(messages) == 0:
		logger.info("No messages")
		return
	#--- end of if ---

	for msg in messages:
		res = requests.post(
			TEST_WEBHOOK,
			json={
				"content": msg,
			}
		)
		if res.status_code != 204:
			logger.error("Failed",res.status_code,res.text)
		elif res.status_code == 204:
			logger.info("Backup success")
		#--- end of if ---
	#--- end of loop ---
#--- end of def --

if __name__ == "__main__":
	client.run(TELLER_TOKEN)
#--- end of if ---