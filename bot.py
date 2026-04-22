import discord
from discord.ext import commands

# ====== INTENTS ======
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ====== READY ======
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# ====== JOIN ======
@bot.command()
async def join(ctx):
    if not ctx.author.voice:
        return await ctx.send("❌ ادخل روم صوتي أول")

    channel = ctx.author.voice.channel
    vc = ctx.voice_client

    try:
        if vc is None:
            await channel.connect()
        else:
            await vc.move_to(channel)

        await ctx.send("✔ دخلت الروم")

    except Exception as e:
        await ctx.send("❌ فشل الدخول")
        print(e)

# ====== LEAVE ======
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 طلعت من الروم")

# ====== PING ======
@bot.command()
async def ping(ctx):
    await ctx.send("pong")

# ====== RUN ======
bot.run("MTQ5NjE2MzU4MjEzMDM5MzE5OQ.GjYWD-.YtsTK6sNyKqd1wM616YXZX7vdb0rd31anbHRSU")
