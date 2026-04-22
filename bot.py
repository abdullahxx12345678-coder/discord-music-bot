import discord
from discord.ext import commands
import wavelink
import os
import asyncio

# ================= إعدادات البوت =================
intents = discord.Intents.default()
intents.message_content = True  # ضروري لقراءة الأوامر
intents.voice_states = True     # ضروري لدخول الرومات الصوتية

bot = commands.Bot(command_prefix="!", intents=intents)

# ================= إعدادات لافالينك =================
# تأكد من الرابط: لا تضع / في نهايته
LAVALINK_URL = "https://lavalink-server-tlb3.onrender.com"
LAVALINK_PASSWORD = "12345678"

# ================= الأحداث (Events) =================

@bot.event
async def on_ready():
    print(f"✅ تم تسجيل الدخول باسم: {bot.user}")
    
    # ربط البوت بسيرفر لافالينك
    node = wavelink.Node(uri=LAVALINK_URL, password=LAVALINK_PASSWORD)
    try:
        await wavelink.Pool.connect(nodes=[node], client=bot, cache_capacity=100)
    except Exception as e:
        print(f"❌ فشل الاتصال بسيرفر لافالينك: {e}")

@bot.event
async def on_wavelink_node_ready(payload: wavelink.NodeReadyEventPayload):
    print(f"🚀 سيرفر لافالينك جاهز للعمل: {payload.node.identifier}")

# ================= الأوامر (Commands) =================

@bot.command(name="play")
async def play(ctx: commands.Context, *, search: str):
    """أمر تشغيل الأغاني"""
    
    # 1. التحقق من وجود المستخدم في روم صوتي
    if not ctx.author.voice:
        return await ctx.send("❌ لازم تدخل روم صوتي أولاً!")

    # 2. الانضمام للروم أو الحصول على المشغل الحالي
    if not ctx.voice_client:
        try:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        except Exception as e:
            return await ctx.send(f"❌ ما قدرت أدخل الروم: {e}")
    else:
        vc: wavelink.Player = ctx.voice_client

    # 3. البحث عن المقطع (يوتيوب أو روابط مباشرة)
    try:
        # البحث الافتراضي يكون عبر YouTube
        tracks = await wavelink.Playable.search(search)
        
        if not tracks:
            return await ctx.send("❌ مالقيت شي بهذا الاسم.")

        track = tracks[0]
        
        # 4. تشغيل المقطع
        await vc.play(track)
        await ctx.send(f"🎶 جاري تشغيل: **{track.title}**")

    except Exception as e:
        print(f"Error: {e}")
        await ctx.send("❌ حدث خطأ أثناء محاولة التشغيل.")

@bot.command()
async def stop(ctx: commands.Context):
    """إيقاف التشغيل والخروج"""
    vc: wavelink.Player = ctx.voice_client
    if vc:
        await vc.disconnect()
        await ctx.send("👋 تم فصل البوت.")

@bot.command()
async def skip(ctx: commands.Context):
    """تخطي الأغنية الحالية"""
    vc: wavelink.Player = ctx.voice_client
    if vc and vc.playing:
        await vc.skip()
        await ctx.send("⏭️ تم التخطي.")

# ================= التشغيل =================
TOKEN = os.getenv("TOKEN")
if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ خطأ: لم يتم العثور على TOKEN في متغيرات البيئة (Railway/Render)")
