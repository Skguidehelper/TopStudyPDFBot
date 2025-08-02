import logging
import json
import os
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN
from utils import is_admin, add_premium_user, is_premium_user

# 🔧 Logging setup
logging.basicConfig(level=logging.INFO)

# 🤖 Initialize Bot and Dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# ✅ /start Command
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id

    # 🔐 Save user ID in users.json
    if not os.path.exists("users.json"):
        with open("users.json", "w") as f:
            json.dump([], f)

    with open("users.json", "r+") as f:
        users = json.load(f)
        if user_id not in users:
            users.append(user_id)
            f.seek(0)
            json.dump(users, f)

    await message.answer(
        f"👋 नमस्ते {message.from_user.first_name}!\n\n"
        "🙏 आपका स्वागत है *Top Study Notes Bot* में!\n"
        "📚 यहां आप Free और Premium Notes पा सकते हैं।\n\n"
        "🧭 शुरू करने के लिए /help दबाएं।",
        parse_mode="Markdown"
    )

# ✅ /help Command
@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    await message.answer(
        "📚 *Download notes:* [Click here](https://t.me/TopStudyPDFBot/files)\n\n"
        "📌 *Available Commands:*\n"
        "/start - वेलकम मैसेज\n"
        "/help - हेल्प कमांड\n"
        "/notes - फ्री नोट्स पाएं\n"
        "/premium - प्रीमियम एक्सेस जानें\n"
        "/premiumnotes - प्रीमियम नोट्स पाएं\n"
        "/contact - संपर्क करें\n"
        "/addpremium user_id - प्रीमियम यूजर जोड़ें (केवल एडमिन के लिए)",
        parse_mode="Markdown"
    )

# ✅ /notes Command
@dp.message_handler(commands=['notes'])
async def send_notes(message: types.Message):
    await message.answer(
        "📥 *यहां से PDF Notes डाउनलोड करें:*\n"
        "🔗 https://example.com/your-notes-link\n\n"
        "_Note: यह Free Notes हैं_",
        parse_mode="Markdown"
    )

# ✅ /premium Command
@dp.message_handler(commands=['premium'])
async def premium_info(message: types.Message):
    await message.answer(
        "💎 *Premium Access Details:*\n"
        "✅ सभी Subjects के Notes\n"
        "✅ बिना Ads के उपयोग\n"
        "✅ Early Access to New Notes\n\n"
        "💰 *Price:* ₹49/- per month\n"
        "📲 Pay via UPI: yourupi@upi\n"
        "🧾 Contact: @skguidehelper",
        parse_mode="Markdown"
    )

# ✅ /contact Command
@dp.message_handler(commands=['contact'])
async def contact_admin(message: types.Message):
    await message.answer("📲 किसी भी सहायता के लिए संपर्क करें: @skguidehelper")

# ✅ /addpremium Command
@dp.message_handler(commands=['addpremium'])
async def add_premium(message: types.Message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.reply("❌ आपको यह command चलाने की अनुमति नहीं है।")
        return

    try:
        parts = message.text.strip().split()
        if len(parts) != 2:
            await message.reply("⚠️ सही उपयोग:\n`/addpremium user_id`", parse_mode="Markdown")
            return

        target_id = int(parts[1])
        if add_premium_user(target_id):
            await message.reply(f"✅ यूज़र {target_id} को Premium Access दे दिया गया।")
        else:
            await message.reply("ℹ️ यह यूज़र पहले से ही Premium User है।")

    except Exception as e:
        await message.reply(f"⚠️ Error: {str(e)}")

# ✅ /premiumnotes Command
@dp.message_handler(commands=['premiumnotes'])
async def send_premium_notes(message: types.Message):
    user_id = message.from_user.id
    if not is_premium_user(user_id):
        await message.reply(
            "🔒 यह फ़ीचर केवल *Premium Users* के लिए है।\n\n"
            "💰 Premium Access के लिए ₹49/- प्रति माह का भुगतान करें।\n"
            "📲 Pay via UPI: yourupi@upi\n"
            "🧾 संपर्क करें: @skguidehelper",
            parse_mode="Markdown"
        )
        return

    try:
        file_path = "notes/sample_notes.pdf"
        with open(file_path, "rb") as doc:
            await message.answer_document(
                doc,
                caption="💎 *Premium PDF Notes*",
                parse_mode="Markdown"
            )
    except Exception as e:
        await message.reply(f"⚠️ Error sending PDF: {str(e)}")

# ✅ Document Upload by Admin (Save)
@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def handle_upload_pdf(message: types.Message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.reply("❌ आपको PDF अपलोड करने की अनुमति नहीं है।")
        return

    try:
        document = message.document
        file_name = document.file_name
        caption = message.caption or "📄 नया नोट्स उपलब्ध है।"

        os.makedirs("notes", exist_ok=True)
        file = await bot.get_file(document.file_id)
        await document.download(destination_file=f"notes/{file_name}")

        await message.reply(f"✅ PDF '{file_name}' सफलतापूर्वक सेव हो गया!\n\nℹ️ Caption: {caption}")

        # Broadcast to users (Optional future step)

    except Exception as e:
        await message.reply(f"⚠️ Error: {str(e)}")

# ✅ Broadcast PDF to all users by Admin
@dp.message_handler(commands=['broadcast'])
async def wait_for_pdf(message: types.Message):
    if is_admin(message.from_user.id):
        await message.reply("📤 कृपया वह PDF भेजें जिसे आप सभी users को भेजना चाहते हैं।")
    else:
        await message.reply("❌ आपको यह कमांड चलाने की अनुमति नहीं है।")

@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def broadcast_pdf(message: types.Message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return  # Ignore document from non-admin

    if not os.path.exists("users.json"):
        await message.reply("⚠️ कोई भी यूज़र फ़ाइल में मौजूद नहीं है।")
        return

    try:
        with open("users.json", "r") as f:
            users = json.load(f)

        doc = message.document
        for uid in users:
            try:
                await bot.send_document(uid, doc.file_id, caption="📘 *नए Notes उपलब्ध हैं!*", parse_mode="Markdown")
            except Exception as e:
                logging.error(f"❌ Cannot send to {uid}: {str(e)}")

        await message.reply("✅ सभी यूज़र्स को PDF भेज दी गई।")

    except Exception as e:
        await message.reply(f"⚠️ Error: {str(e)}")

# ✅ Run the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

