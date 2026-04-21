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
LAVALINK_URL = "https://lavalink-server-tlb3.onrender.com"
LAVALINK_PASSWORD = "12345678"

# ================= LAVALINK CONNECT =================
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await connect_nodes()

async def connect_nodes():
    try:
        node = wavelink.Node(
            uri=LAVALINK_URL,
            password=LAVALINK_PASSWORD,
            identifier="MAIN"
        )

        await wavelink.Pool.connect(client=bot, nodes=[node])
        print("Lavalink Connected ✔")

    except Exception as e:
        print("Lavalink Error:", e)

# ================= JOIN VOICE =================
async def join_voice(ctx):
    if not ctx.author.voice:
        await ctx.send("❌ ادخل روم صوتي أول")
        return None

    channel = ctx.author.voice.channel

    vc = ctx.voice_client

    if vc is None:
        try:
            vc = await channel.connect()
        except:
            await ctx.send("❌ ما قدرت أدخل الروم الصوتي")
            return None
    else:
        await vc.move_to(channel)

    return vc

# ================= PLAY =================
@bot.command()
async def play(ctx, url: str):
    await ctx.send("🎵 اختبار دخول الصوت...")

    vc = await join_voice(ctx)

    if vc:
        await ctx.send("✔ دخلت الروم الصوتي بنجاح")
    else:
        await ctx.send("❌ فشل الدخول")

# ================= CONTROLS =================
@bot.command()
async def skip(ctx):
    vc: wavelink.Player = ctx.voice_client
    if vc and vc.playing:
        await vc.stop()
        await ctx.send("⏭ تم التخطي")

@bot.command()
async def pause(ctx):
    vc: wavelink.Player = ctx.voice_client
    if vc:
        await vc.pause(True)
        await ctx.send("⏸ توقف")

@bot.command()
async def resume(ctx):
    vc: wavelink.Player = ctx.voice_client
    if vc:
        await vc.pause(False)
        await ctx.send("▶ استكمال")

@bot.command()
async def stop(ctx):
    vc: wavelink.Player = ctx.voice_client
    if vc:
        await vc.disconnect()
        await ctx.send("⛔ تم الإيقاف")

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

# ================= RUN =================
bot.run(os.getenv("TOKEN"))
