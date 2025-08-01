# 📚 TOPSTUDYPDFBOT - Telegram Bot for Sharing Study Notes

**TOPSTUDYPDFBOT** is a lightweight Telegram bot built using Python and Aiogram.  
It allows users to download premium PDF notes and lets admins manage premium access for students easily.

---

## ✨ Features

- 🔐 Admin-only commands
- 📤 Upload and broadcast PDF notes
- 👑 Premium access system
- 💾 Simple JSON database (no SQL)
- ⚙️ Easy to host locally or on VPS

---

## 💡 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Start message |
| `/help` | How to use the bot |
| `/addpremium [user_id]` | Add premium access (admin only) |
| `/uploadpdf` | Upload and send PDF to all users (admin only) |

---

## 🛠 Tech Stack

- **Language:** Python 3
- **Framework:** Aiogram (Telegram Bot API)
- **Database:** JSON-based (no external DB needed)

---

## 🚀 Setup Instructions

### 1. Clone this repo
```bash
git clone https://github.com/yourusername/TOPSTUDYPDFBOT.git
cd TOPSTUDYPDFBOT
