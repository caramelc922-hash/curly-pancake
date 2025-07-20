from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
import telegram

CHANNEL_ID = "@mediabecek"  
BOT_TOKEN = "7713895035:AAHlxC4QOoko0bU-V-fTe6ZvCJxiNAi7WoM"  

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name

    with open("users.txt", "a+") as f:
        f.seek(0)
        if str(user_id) not in f.read():
            f.write(str(user_id) + "\n")

    photo_url = "https://deras88.b-cdn.net/ADS%20DERAS88%20(29)%20(1).png"  
    caption = (
        f"👋 Hai {first_name}!\n\n"
        "Selamat datang di *Channel Eksklusif!* 🔥\n\n"
        "Untuk melihat konten premium, kamu wajib join channel terlebih dahulu ya."
    )

    keyboard = [
        [InlineKeyboardButton("🔗 Join Channel", url=f"https://t.me/{CHANNEL_ID[1:]}")],
        [InlineKeyboardButton("✅ Sudah Join", callback_data='check_join')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=photo_url,
        caption=caption,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

def check_join(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id

    try:
        member = context.bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            query.edit_message_text("✅ Kamu sudah join! Ini kontennya:\nhttps://t.me/s/namachannelkamu/1")
        else:
            query.answer("❌ Kamu belum join channel!", show_alert=True)
    except telegram.error.TelegramError:
        query.answer("⚠️ Gagal memeriksa. Coba lagi nanti.", show_alert=True)

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(check_join, pattern='check_join'))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
