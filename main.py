import os

# الكود يسحب البيانات من إعدادات Railway تلقائياً
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = int(os.environ.get("OWNER_ID", 0))
DOMAIN = os.environ.get("DOMAIN", "ryen.tax")
