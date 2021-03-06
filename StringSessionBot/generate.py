from asyncio.exceptions import TimeoutError
from Data import Data
from pyrogram import Client, filters
from telethon import TelegramClient
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)


@Client.on_message(filters.private & ~filters.forwarded & filters.command('generate'))
async def main(_, msg):
    await msg.reply(
        "๐ุงุฐุง ูููุช ุชูุฑูุฏ ุชููุตููุจ ุณููุฑุณ ููููุฒู ููุฃุฎุชูุงุฑ ููููุฏ ุจูุงููุฑูุฌูุฑุงู, ูุงุฐุง ุชูุฑููุฏ ุชููุตููุจ ุงูุชููุซูู ููุฃุฎูุชุงุฑ ููููุฏ ุชูุฑูููุณ",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("๐งยฆููููุฏ ุจูุงููุฑูุฌูุฑุงู", callback_data="pyrogram"),
            InlineKeyboardButton("๐ยฆููููุฏ ุชูุฑูููุณ", callback_data="telethon")
        ]])
    )


async def generate_session(bot, msg, telethon=False):
    await msg.reply("๐ุจุฏุง ุนูู ุฌูุณู {} ูุงุณุชุฎุฑุงุฌ ุงูููุฏ...".format("ุชูููุซูู" if telethon else "ูููููุฒู"))
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, '๐ฎุฃููุง ูู ุจุฃุฑุณุงู ุงูู `API_ID`', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        await api_id_msg.reply('โููุฌุฏ ุฎุทุฃ ูู ุงูู API_ID . โ๏ธูู ูุถูู ุงุจุฏุฃ ุนูู ุฌูุณู ูุฑู ุงุฎุฑู.', quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    api_hash_msg = await bot.ask(user_id, '๐ฎุญุณููุง ูู ุจุฃุฑุณุงู ุงูู `API_HASH`', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    api_hash = api_hash_msg.text
    phone_number_msg = await bot.ask(user_id, 'โ๏ธุงูุงู ุงุฑุณู `ุฑููู` ูุน ุฑูุฒ ุฏููุชู , ูุซุงู :`+201098719733`', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    phone_number = phone_number_msg.text
    await msg.reply("โฌ๏ธุงูุชูุธุฑ ููุญุธูู ุณููู ููุฑุณูู ูููุฏ ูุญุณุงุจูู ุจุงูุชููุฌูุฑุงู...")
    if telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    else:
        client = Client(":memory:", api_id, api_hash)
    await client.connect()
    try:
        if telethon:
            code = await client.send_code_request(phone_number)
        else:
            code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply('`API_ID` ู `API_HASH` โูุฐู ุงูุงูุจููุงุช ุฎุทุฃ. โ๏ธูู ูุถูู ุงุจุฏุฃ ุนูู ุฌูุณู ูุฑู ุงุฎุฑู', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply('`ุฑููู` โุฎุทุฃ. ุฑุฌุงุกุง ูู ุจุฃุนุงุฏุฉ ุงูุงุณุชุฎุฑุงุฌ ูู ุฌุฏูุฏ.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    try:
        phone_code_msg = await bot.ask(user_id, " ๐ูู ูุถูู ุงูุญุต ุญุณุงุจู ุจุงูุชููุฌุฑุงู ูุชููุฏ ุงูููุฏ ูู ุญุณุงุจ ุงุดุนุงุฑุงุช ุงูุชููุฌุฑุงู. ุฅุฐุง ูุงู ููุงู ุชุญูู ุจุฎุทูุชูู( ุงููุฑูุฑ ) ุ ุฃุฑุณู ูููุฉ ุงููุฑูุฑ ููุง ุจุนุฏ ุงุฑุณุงู ููุฏ ุงูุฏุฎูู ุจุงูุชูุณูู ุฃุฏูุงู.- ุงุฐุง ูุงูุช ูููุฉ ุงููุฑูุฑ ุงู ุงูููุฏ  ูู 12345 ูุฑุฌู ุงุฑุณุงููุง ุจุงูุดูู ุงูุชุงูู 1 2 3 4 5 ูุน ูุฌูุฏ ูุณูุงููุงุช ุจูู ุงูุงุฑูุงู ุงุฐุง ุงุญุชุฌุช ูุณุงุนุฏุฉ @TTTLL0", filters=filters.text, timeout=600)
        if await cancelled(api_id_msg):
            return
    except TimeoutError:
        await msg.reply('โุนุฐุฑุง ููุฏ ุชุฎุทูุช 10 ุฏูุงุฆู ูู ุงูุฒูู ุงููุญุฏุฏ. โ๏ธูู ูุถูู ุงุจุฏุฃ ุนูู ุฌูุณู ูุฑู ุงุฎุฑู.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    phone_code = phone_code_msg.text.replace(" ", "")
    try:
        if telethon:
            await client.sign_in(phone_number, phone_code, password=None)
        else:
            await client.sign_in(phone_number, code.phone_code_hash, phone_code)
    except (PhoneCodeInvalid, PhoneCodeInvalidError):
        await msg.reply('โุงูููุฏ ุบูุฑ ุตุญูุญ. โ๏ธูู ูุถูู ุงุจุฏุฃ ุนูู ุฌูุณู ูุฑู ุงุฎุฑู.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (PhoneCodeExpired, PhoneCodeExpiredError):
        await msg.reply('โุงูููุฏ ูุฐุง ุงูุชูุช ุตูุงุญูุชู. โ๏ธูู ูุถูู ุงุจุฏุฃ ุนูู ุฌูุณู ูุฑู ุงุฎุฑู.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (SessionPasswordNeeded, SessionPasswordNeededError):
        try:
            two_step_msg = await bot.ask(user_id, 'ูุฐุง ุงูุญุณุงุจ ูุญูู ูู ุฎูุงู ุงูุชุญูู ุจุฎุทูุชูู. ูู ูุถูู ุงุฑุณู ๐ ูููู ุงุงููุฑูุฑ .', filters=filters.text, timeout=300)
        except TimeoutError:
            await msg.reply('โุนุฐุฑุง ููุฏ ุชุฎุทูุช 5 ุฏูุงุฆู ูู ุงูุฒูู ุงููุญุฏุฏ. โ๏ธูู ูุถูู ุงุจุฏุฃ ุนูู ุฌูุณู ูุฑู ุงุฎุฑู.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return
        try:
            password = two_step_msg.text
            if telethon:
                await client.sign_in(password=password)
            else:
                await client.check_password(password=password)
            if await cancelled(api_id_msg):
                return
        except (PasswordHashInvalid, PasswordHashInvalidError):
            await two_step_msg.reply('โูููู ุงููุฑูุฑ ุฎุทุฃ. โ๏ธูู ูุถูู ุงุจุฏุฃ ุนูู ุฌูุณู ูุฑู ุงุฎุฑู.', quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = "**{} ุฌููุณูู ุฌูุฏููุฏู** \n\n`{}` \n\nุงุณุชุฎุฑุฌุช ูู @EITHON1".format("โฌ๏ธุชูููููุซููููู" if telethon else "โฌ๏ธูููููููููุฒู", string_session)
    try:
        await client.send_message("me", text)
    except KeyError:
        pass
    await client.disconnect()
    await phone_code_msg.reply("โุชู ุงุณุชุฎุฑุงุฌ ุงูุฌูุณู ุจูุฌุงุญ {}. \n\n๐ูู ูุถูู ุชูุญุต ุงูุฑุณุงุฆู ุงููุญููุธู ุจุญุณุงุจู! \n\nBy @EITHON1".format("telethon" if telethon else "pyrogram"))


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("โ๏ธุชู ุงูุบุงุก ุงูุงุณุชุฎุฑุงุฌ!", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return True
    elif "/restart" in msg.text:
        await msg.reply("๐ุชูุช ุงุนุงุฏู ุชุดุบูู ุงูุจูุช !", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return True
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("โจ๏ธุชู ุฃูุบุงุก ุงูุงุณุชุฎุฑุงุฌ!", quote=True)
        return True
    else:
        return False
