import os
from typing import Optional
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler

# التوكن الصحيح الذي أرسلته
BOT_TOKEN = "8355891654:AAE7Yncq6CmJYTONl0GQC8DQgxxnSc8i_jg"
OWNER_ID = 8081542687

app = FastAPI()
tg_app: Optional[Application] = None

@app.on_event("startup")
async def startup():
    global tg_app
    # إعداد البوت باستخدام التوكن المحدث
    tg_app = Application.builder().token(BOT_TOKEN).build()
    
    # إضافة أمر ترحيبي للتأكد من استجابة البوت
    tg_app.add_handler(CommandHandler("start", lambda u, c: u.message.reply_text("✅ أهلاً بك! البوت يعمل الآن بشكل صحيح بنسبة 100%.")))
    
    await tg_app.initialize()
    await tg_app.start()

@app.get("/")
async def root():
    return {"status": "online", "bot": "running"}

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, tg_app.bot)
    await tg_app.update_queue.put(update)
    return {"ok": True}
