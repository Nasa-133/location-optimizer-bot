#!/usr/bin/env python3
# -*- coding: utf-8 -*-
START_MESSAGE = """
🎯 Assalomu alaykum! Marshrut optimallashtirish botiga xush kelibsiz!

📍 Ushbu bot sizga bir nechta manzillarni eng qisqa yo'l bo'yicha tartiblab beradi.

🚀 Boshlash uchun birinchi manzilni yuboring (lokatsiya yoki matn ko'rinishida)
"""

LOCATION_REQUEST = """
📍 Lokatsiyangizni yuboring:
• Telegram'da lokatsiya tugmasini bosing
• Yoki manzilni matn ko'rinishida yozing
"""

CONFIRM_ADDRESS = "📍 Siz yuborgan lokatsiya: {address}\n❓ Ushbu manzilni tasdiqlaysizmi?"

# Keyingi manzil so'rash
ADD_MORE_ADDRESS = "➕ Yana manzil qo'shasizmi?"

# Oxirgi manzil so'rash
FINAL_CHOICE = "Oxirgi manzil hozirgi joyingizmi yoki boshqa manzil qo'shasizmi?"

# Marshrut natijasi
ROUTE_RESULT = """
🔁 Optimal marshrut: {route_order}
⏱ Masofa: {distance} km / Vaqt: {duration} daqiqa

📍 Manzillar:
{addresses}

🔗 Yandex Mapda ko'rish: {map_url}
"""

# Xatolik xabarlari
ERROR_GEOCODING = "❌ Manzilni aniqlashda xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring."
ERROR_ROUTE = "❌ Marshrut hisoblashda xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring."
ERROR_GENERAL = "❌ Kutilmagan xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring."

# Muvaffaqiyat xabarlari
ADDRESS_ADDED = "✅ Manzil qo'shildi!"
ROUTE_CALCULATING = "⏳ Marshrut hisoblanmoqda..."

# Admin xabarlar
ADMIN_WELCOME = "🔑 Admin paneliga xush kelibsiz!"
ADMIN_USERS_LIST = "👥 Foydalanuvchilar ro'yxati:\n\n{users}"
ADMIN_BROADCAST_REQUEST = "📨 Barcha foydalanuvchilarga yubormoqchi bo'lgan xabaringizni yozing:"
ADMIN_BROADCAST_SUCCESS = "✅ Xabar {count} ta foydalanuvchiga yuborildi!"
ADMIN_ACCESS_DENIED = "❌ Sizda admin paneliga kirish huquqi yo'q!"
ADMIN_LOGIN_REQUEST = "🔐 Admin login kiriting:"
ADMIN_PASSWORD_REQUEST = "🔑 Admin parol kiriting:"
ADMIN_LOGIN_SUCCESS = "✅ Muvaffaqiyatli kirdingiz!"
ADMIN_LOGIN_FAILED = "❌ Login yoki parol noto'g'ri!"

# Tugma matnlari
BTN_YES = "✅ Ha"
BTN_NO = "❌ Yo'q"
BTN_ADD_MORE = "➕ Ha"
BTN_RETURN_HERE = "🏠 Shu yerga qaytaman"
BTN_ADD_ANOTHER = "➕ Boshqa manzil qo'shaman"

# Admin tugmalar
BTN_ADMIN_USERS = "👥 Foydalanuvchilar"
BTN_ADMIN_BROADCAST = "📨 Xabar yuborish"
BTN_ADMIN_KEYWORDS = "🔑 Keywords"
BTN_ADMIN_BACK = "⬅️ Orqaga"