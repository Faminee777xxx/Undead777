import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import feedparser

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# กำหนด channel_id ของ YouTube ที่ต้องการติดตาม
YOUTUBE_CHANNEL_ID = "UCDBi2-s04PIchOAZPbGsqnA"  # เปลี่ยนเป็นของจริง
YOUTUBE_FEED_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={YOUTUBE_CHANNEL_ID}"

# กำหนด channel ID ใน Discord ที่จะแจ้งเตือน
DISCORD_CHANNEL_ID = 1296023140010426368  # เปลี่ยนเป็นของจริง

last_video_id = None

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    check_new_video.start()

@tasks.loop(minutes=5)
async def check_new_video():
    global last_video_id
    feed = feedparser.parse(YOUTUBE_FEED_URL)
    if not feed.entries:
        return

    latest_video = feed.entries[0]
    video_id = latest_video.yt_videoid
    video_url = latest_video.link
    title = latest_video.title

    if video_id != last_video_id:
        last_video_id = video_id
        channel = bot.get_channel(DISCORD_CHANNEL_ID)
        if channel:
            embed = discord.Embed(title="**คริปรีเฟกมาแล้ว!**\n", description=f"[{title}]({video_url})", color=0x000000)
            embed.set_thumbnail(url="https://www.youtube.com/s/desktop/9cfa893a/img/favicon_144x144.png")
            embed.set_image(url=latest_video.media_thumbnail[0]['url'])
            await channel.send(embed=embed)

bot.run(TOKEN)
