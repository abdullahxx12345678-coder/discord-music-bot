import discord
from discord.ext import commands
import wavelink
import os

# ================= INTENTS =================
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ================= LAVALINK SETTINGS =================
LAVALINK_URL = "https://lavalink-server-tlb3.onrender.com/"  # 🔴 حط رابط Render هنا
LAVALINK_PASSWORD = "12345678"

async def connect_nodes():
    node = wavelink.Node(
        uri=LAVALINK_URL,
        password=LAVALINK_PASSWORD,
        identifier="MAIN"
    )

    await wavelink.Pool.connect(client=bot, nodes=[node])

async def join_voice(ctx):
    if not ctx.author.voice:
        await ctx.send("❌ ادخل روم صوتي أول")
        return

    channel = ctx.author.voice.channel

    if ctx.voice_client is None:
        await channel.connect()
    else:
        await ctx.voice_client.move_to(channel)

# ================= CONNECT LAVALINK =================
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await connect_nodes()


async def connect_nodes():
    node = wavelink.Node(
        uri=LAVALINK_URL,
        password=LAVALINK_PASSWORD,
        identifier="MAIN"
    )

    await wavelink.Pool.connect(client=bot, nodes=[node])

# ================= PLAY (URL ONLY) =================
@bot.command()
async def play(ctx, url: str):
    await join_voice(ctx)

    vc: wavelink.Player = ctx.voice_client

    try:
        track = await wavelink.Playable.search(url)

        if not track:
            return await ctx.send("❌ ما قدرت أجيب الأغنية")

        track = track[0] if isinstance(track, list) else track

        await vc.play(track)

        await ctx.send(f"🎶 تشغيل: **{track.title}**")

    except Exception as e:
        await ctx.send("❌ صار خطأ في التشغيل")
        print(e)

# ================= SKIP =================
@bot.command()
async def skip(ctx):
    vc: wavelink.Player = ctx.voice_client

    if vc and vc.playing:
        await vc.stop()
        await ctx.send("⏭ تم التخطي")

# ================= PAUSE =================
@bot.command()
async def pause(ctx):
    vc: wavelink.Player = ctx.voice_client

    if vc:
        await vc.pause(True)
        await ctx.send("⏸ توقف مؤقت")

# ================= RESUME =================
@bot.command()
async def resume(ctx):
    vc: wavelink.Player = ctx.voice_client

    if vc:
        await vc.pause(False)
        await ctx.send("▶ استكمال")

# ================= STOP =================
@bot.command()
async def stop(ctx):
    vc: wavelink.Player = ctx.voice_client

    if vc:
        await vc.disconnect()
        await ctx.send("⛔ تم الإيقاف")

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

# ================= RUN BOT =================
bot.run(os.getenv("TOKEN"))
