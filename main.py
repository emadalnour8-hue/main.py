import os
from typing import Optional
from fastapi import FastAPI, Request, Form
from telegram import Update
from telegram.ext import Application, CommandHandler

BOT_TOKEN = "8355891654:AAE7Yncq6CmJYTONl0GQC8DQgxxnSc8i_jg"
OWNER_ID = 8081542687

app = FastAPI()
tg_app: Optional[Application] = None

@app.on_event("startup")
async def startup():
    global tg_app
    tg_app = Application.builder().token(BOT_TOKEN).build()
    tg_app.add_handler(CommandHandler("start", lambda u, c: u.message.reply_text("✅ البوت جاهز لاستقبال إيميلاتك الآن!")))
    await tg_app.initialize()
    await tg_app.start()

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, tg_app.bot)
    await tg_app.update_queue.put(update)
    return {"ok": True}

# الوظيفة الجديدة لاستقبال الإيميلات من Mailgun
@app.post("/mailgun")
async def mailgun_webhook(
    sender: str = Form(...),
    subject: str = Form(...),
    body: str = Form(None, alias='body-plain')
):
    message = f"📧 **إيميل جديد وصل!**\n\n👤 **من:** {sender}\n📌 **الموضوع:** {subject}\n\n📝 **النص:**\n{body}"
    await tg_app.bot.send_message(chat_id=OWNER_ID, text=message, parse_mode='Markdown')
    return {"status": "delivered"}
