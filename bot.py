import discord
from discord.ext import commands
import wavelink
import os

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# تأكد أن الرابط لا ينتهي بـ /
LAVALINK_URL = "https://lavalink-server-tlb3.onrender.com:443"
LAVALINK_PASSWORD = "12345678"

@bot.event
async def on_ready():
    print(f"✅ Bot is ready: {bot.user}")
    
    # تعريف النود
    node = wavelink.Node(
        uri=LAVALINK_URL, 
        password=LAVALINK_PASSWORD,
        inactive_timeout=60
    )
    
    try:
        # الربط مع السيرفر
        await wavelink.Pool.connect(nodes=[node], client=bot)
    except Exception as e:
        print(f"❌ Connection error: {e}")

@bot.event
async def on_wavelink_node_ready(payload: wavelink.NodeReadyEventPayload):
    print(f"🚀 Node {payload.node.identifier} is connected and ready!")

@bot.command()
async def play(ctx: commands.Context, *, search: str):
    # تحقق هل السيرفر متصل فعلياً؟
    if not wavelink.Pool.nodes:
        return await ctx.send("❌ عذراً، سيرفر الصوت (Lavalink) غير متصل حالياً. انتظر ثواني وجرب مرة ثانية.")

    if not ctx.author.voice:
        return await ctx.send("❌ ادخل روم صوتي أولاً!")

    if not ctx.voice_client:
        vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    else:
        vc: wavelink.Player = ctx.voice_client

    try:
        tracks = await wavelink.Playable.search(search)
        if not tracks:
            return await ctx.send("❌ ما لقيت نتائج.")

        track = tracks[0]
        await vc.play(track)
        await ctx.send(f"🎶 جاري تشغيل: **{track.title}**")
        
    except Exception as e:
        print(f"Play Error: {e}")
        await ctx.send("❌ فشل تشغيل الصوت.")

bot.run(os.getenv("TOKEN"))
