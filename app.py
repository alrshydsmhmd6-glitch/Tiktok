import os
import telebot
import yt_dlp

# التوكن الخاص بك
TOKEN = "8999978307:AAEyItZiMBG4aLR5YSLftLJZfzgWCXVU73o"

bot = telebot.TeleBot(TOKEN)

# التفاعل مع أمر /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        f"أهلاً بك يا {message.from_user.first_name} في بوت التحميل الذكي! 📥✨\n\n"
        "أرسل لي رابط فيديو من (تيك توك، يوتيوب، إنستغرام، أو تويتر) وسأقوم بتحميله وإرساله لك فوراً!"
    )
    bot.reply_to(message, welcome_text)

# التفاعل مع الروابط المُرسلة
@bot.message_handler(func=lambda message: True)
def download_and_send_video(message):
    url = message.text.strip()
    
    # التأكد أن النص المكتوب هو رابط
    if not (url.startswith("http://") or url.startswith("https://")):
        bot.reply_to(message, "يرجى إرسال رابط فيديو صحيح يبدأ بـ http أو https 🔗")
        return

    status_msg = bot.reply_to(message, "⏳ جاري تحميل الفيديو، يرجى الانتظار...")
    
    # إعدادات yt_dlp لتنزيل الفيديو بجودة مناسبة
    ydl_opts = {
        'format': 'best[filesize<50M]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'downloaded_video.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }
    
    filename = None
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
        # إرسال الفيديو للمستخدم
        with open(filename, 'rb') as video_file:
            bot.send_video(
                message.chat.id, 
                video_file, 
                caption="تم التحميل بنجاح بواسطة بوت محمد 🚀",
                reply_to_message_id=message.message_id
            )
            
        # حذف رسالة الانتظار
        bot.delete_message(message.chat.id, status_msg.message_id)
        
    except Exception as e:
        bot.edit_message_text(
            f"❌ حدث خطأ أثناء تحميل المقطع، أرجو التأكد من صحة الرابط أو حاول مجدداً.\nالخطأ: {str(e)[:100]}",
            chat_id=message.chat.id,
            message_id=status_msg.message_id
        )
        
    finally:
        # مسح الفيديو بعد إرساله لتوفير المساحة
        if filename and os.path.exists(filename):
            os.remove(filename)

# تشغيل البوت
print("تم تشغيل بوت التحميل بنجاح...")
bot.infinity_polling()
