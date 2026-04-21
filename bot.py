import discord
from discord.ext import commands
import wavelink
import os

# ================= INTENTS =================
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ================= LAVALINK =================
LAVALINK_HOST = "localhost"
LAVALINK_PORT = 2333
LAVALINK_PASSWORD = "youshallnotpass"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    # اتصال Lavalink
    await connect_nodes()

async def connect_nodes():
    node = wavelink.Node(
        uri=f"http://{LAVALINK_HOST}:{LAVALINK_PORT}",
        password=LAVALINK_PASSWORD
    )

    await wavelink.Pool.connect(client=bot, nodes=[node])

# ================= JOIN VOICE =================
async def join_voice(ctx):
    if not ctx.author.voice:
        return await ctx.send("❌ ادخل روم صوتي أول")

    channel = ctx.author.voice.channel

    if not ctx.voice_client:
        await channel.connect(cls=wavelink.Player)
    else:
        await ctx.voice_client.move_to(channel)

# ================= PLAY =================
@bot.command()
async def play(ctx, *, search: str):
    await join_voice(ctx)

    vc: wavelink.Player = ctx.voice_client

    tracks = await wavelink.Playable.search(search)

    if not tracks:
        return await ctx.send("❌ ما لقيت شيء")

    track = tracks[0]

    await vc.play(track)

    await ctx.send(f"🎶 تشغيل: **{track.title}**")

# ================= SKIP =================
@bot.command()
async def skip(ctx):
    vc: wavelink.Player = ctx.voice_client

    if vc:
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

# ================= RUN BOT =================
bot.run(os.getenv("TOKEN"))
