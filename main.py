import os
import discord

from dotenv import load_dotenv
from discord.ext import commands

from keep_alive import keep_alive

load_dotenv()

TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    raise RuntimeError("TOKEN environment variable not found!")


intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True
intents.voice_states = True


class MyBot(commands.Bot):

    async def setup_hook(self):
        await self.load_extension("automod")
        await self.load_extension("moderation")


bot = MyBot(
    command_prefix="!",
    intents=intents,
    help_command=None
)


@bot.event
async def on_ready():
    print("=" * 50)
    print(f"✅ Logged in as {bot.user}")
    print(f"🖥️ Connected to {len(bot.guilds)} guild(s)")
    print("=" * 50)


# Keep Alive (Render)
keep_alive()


# Run Bot
try:
    bot.run(TOKEN)

except discord.LoginFailure:
    print("❌ Token không hợp lệ.")

except Exception as e:
    print(f"❌ Lỗi khi khởi động bot: {e}")
import traceback

@bot.event
async def on_error(event, *args, **kwargs):
    print("===== BOT ERROR =====")
    traceback.print_exc()


try:
    bot.run(TOKEN)
except Exception:
    print("===== CRASH =====")
    traceback.print_exc()