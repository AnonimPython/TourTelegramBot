from aiogram import Dispatcher, types
from aiogram.filters import Command
from app.data import COUNTRIES, CHECKLIST, CURRENCY_RATES

def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command(commands=['start', 'help']))
    dp.message.register(cmd_countries, Command(commands=['countries']))
    dp.message.register(cmd_currency, Command(commands=['currency']))
    dp.message.register(cmd_phrases, Command(commands=['phrases']))
    dp.message.register(cmd_checklist, Command(commands=['checklist']))
    dp.message.register(cmd_sights, Command(commands=['sights']))

async def cmd_start(message: types.Message):
    text = (
        "🌍 Помощник по путешествиям!\n\n"
        "Доступные команды:\n"
        "/countries - Список стран\n"
        "/currency [100 USD RUB] - Конвертер валют\n"
        "/phrases [код страны] - Полезные фразы\n"
        "/checklist - Чек-лист для сборов\n"
        "/sights [код страны] - Достопримечательности"
    )
    await message.answer(text)

async def cmd_countries(message: types.Message):
    countries = "\n".join([f"{code} - {data['name']}" for code, data in COUNTRIES.items()])
    await message.answer(f"🛫 Доступные страны:\n{countries}")

async def cmd_currency(message: types.Message):
    try:
        _, amount, from_curr, to_curr = message.text.split()
        from_curr = from_curr.upper()
        to_curr = to_curr.upper()
        
        rate = CURRENCY_RATES.get(from_curr, {}).get(to_curr)
        if not rate:
            return await message.answer("🚫 Нет данных для конвертации")
            
        result = float(amount) * rate
        await message.answer(f"💱 {amount} {from_curr} → {round(result, 2)} {to_curr}")
        
    except Exception:
        await message.answer("❌ Формат: /currency [сумма] [из] [в]\nПример: /currency 100 USD RUB")

async def cmd_phrases(message: types.Message):
    try:
        country_code = message.text.split()[1].upper()
        country = COUNTRIES[country_code]
        phrases = "\n".join([f"• {k} → {v}" for k, v in country['phrases'].items()])
        await message.answer(f"📚 Основные фразы ({country['name']}):\n{phrases}")
    except:
        await message.answer("❌ Используйте: /phrases [код страны]\nПример: /phrases DE")

async def cmd_checklist(message: types.Message):
    checklist = "\n".join([f"✅ {item}" for item in CHECKLIST])
    await message.answer(f"🧳 Чек-лист для путешествий:\n{checklist}")

async def cmd_sights(message: types.Message):
    try:
        country_code = message.text.split()[1].upper()
        country = COUNTRIES[country_code]
        sights = "\n".join([f"🏛 {sight}" for sight in country['sights']])
        await message.answer(f"🌆 Достопримечательности {country['name']}:\n{sights}")
    except:
        await message.answer("❌ Используйте: /sights [код страны]\nПример: /sights IT")