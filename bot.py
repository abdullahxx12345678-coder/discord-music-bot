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
LAVALINK_PASSWORD = "youshallnotpass"

async def connect_nodes():
    node = wavelink.Node(
        uri=LAVALINK_URL,
        password=LAVALINK_PASSWORD,
        identifier="MAIN"
    )

    await wavelink.Pool.connect(client=bot, nodes=[node])

# ================= CONNECT LAVALINK =================
@bot.event
async def on_ready():
    print("BOT ONLINE")
    try:
        await connect_nodes()
        print("LAVALINK CONNECT ATTEMPT DONE")
    except Exception as e:
        print("ERROR CONNECTING NODE:", e)

# ================= JOIN VOICE =================
async def join_voice(ctx):
    if not ctx.author.voice:
        return await ctx.send("❌ ادخل روم صوتي أول")

    channel = ctx.author.voice.channel

    if not ctx.voice_client:
        await channel.connect(cls=wavelink.Player)
    else:
        await ctx.voice_client.move_to(channel)

# ================= PLAY (URL ONLY) =================
@bot.command()
async def play(ctx, url: str):
    await join_voice(ctx)

    vc: wavelink.Player = ctx.voice_client

    try:
        tracks = await wavelink.Playable.search(url)

        if not tracks:
            return await ctx.send("❌ ما قدرت أجيب الصوت من الرابط")

        track = tracks[0] if isinstance(tracks, list) else tracks

        await vc.play(track)

        await ctx.send(f"🎶 جاري التشغيل: **{track.title}**")

    except Exception as e:
        await ctx.send("❌ صار خطأ أثناء التشغيل")
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
