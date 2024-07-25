from telethon import TelegramClient, events, functions
import re
import os
from colorama import init, Fore, Back, Style
import asyncio

api_identifier = os.getenv("api_id")
api_hash_value = os.getenv("api_hash")
admin_mode = int(os.getenv("admin_mode"))
session_name = os.getenv("session_name")

telegram_client = TelegramClient(session_name, api_identifier, api_hash_value).start()
init(autoreset=True)

ascii_logo = (
    Fore.LIGHTRED_EX + Style.BRIGHT + "  ____   _   _    _   _______   _    _  _ \n" +
    Fore.LIGHTRED_EX + Style.BRIGHT + " / __ \\ | \\ | |  | | |__   __| | |  | || |\n" +
    Fore.LIGHTRED_EX + Style.BRIGHT + "| |  | ||  \\| |  | |    | |    | |  | || |\n" +
    Fore.LIGHTRED_EX + Style.BRIGHT + "| |  | || . ` |  | |    | |    | |  | || |\n" +
    Fore.LIGHTRED_EX + Style.BRIGHT + "| |__| || |\\  |  | |____| |____| |__| ||_|\n" +
    Fore.LIGHTRED_EX + Style.BRIGHT + " \\____/ |_| \\_|  |______|______|\\____/ (_)\n" +
    Fore.LIGHTRED_EX + Style.BRIGHT + "GNAZH V4"
)

channel_invite_link = "t.me/JJ7AA"

print(ascii_logo)
print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "\nClick here to join our Telegram channel: " + Fore.LIGHTGREEN_EX + Style.BRIGHT + channel_invite_link)
print(Fore.CYAN + Style.BRIGHT + "\nThe source is running successfully . . . ")
print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "_____________________________")

user_id_set = set()
keyword_list = ['يكتب', 'يرسل', 'يبعت', 'يقول', 'اول', 'first' ,'FIRST' ,'First' ,'يكتب', 'يرسل', 'يبعت', 'يقول', 'اول', 'ا و ل', ' أ و ل', 'أول', 'اولـ', 'awl', 'اwل', 'اوL', 'aول', 'awل', 'اوl', 'ا.ول', 'اكا']
replacement_dict = {
    'الحركات': '', 'الشات': '', 'التعليقات': '', 'بلشات': '', 'بالتعليقات': '', 'بلتعليقات': '','الخاص': '',
    'اقواس': '', 'بلاقواس': '', 'في ': '', 'بلا ': '', 'كلمة ': '', 'كلمه ': '',
    'يقول ': '', 'يكتب ': '', 'مناقشه ': '', 'كومنت ': '', 'كمنت ': '', 'First': '', 'ک': 'ك', 'او ل': '',
    'ا ول': '', 'ا و ل': '', 'ا و  ل': '', 'يحط': '', 'يرسل': '', 'ف ': '', 'بالتشكيل': '',
    'تشكيل': '', 'Comment': '', 'ࢪ': 'ر', '؏': 'ع', 'آ': 'ا', 'ٱ': 'ا', 'ے': '', 'ـ': '',
    'اول ': '', 'اسم': '', 'ۅ': 'و', 'حركات': '', '()': '', 'وبالايموجي': '', 'بالايموجي': '',
    'يكتب ': '', 'واحد ': '', ' خليت حركات حته محد ينسخ': '', 'بدون ': '', 'شخص': '',
    'فالتعليقات': '', 'أول ': '', 'فلبوت': '', 'ايموجي': '', 'ݪ': 'ل', 'ݛ': 'ر', 'حرڪات': '',
    'مع ': '', 'ڪ': 'ك', 'گ': 'ك', 'بل ': '', 'مفعل لا تشارك': '', 'أ': 'ا', 'شات ': '',
    'FIRST': '', 'كلمه': '', 'ټ': 'ت', 'ډ': 'د', 'ﺂ': 'ا', 'ﺑ': 'ب', 'خاص': '', 'ڝ': 'ص',
    'ﻣ': 'م', 'ט': 'ن', 'ڼ': 'ن', 'נ': 'د', 'ﺣ': 'ح', 'ہ': 'ه', 'first': ''
}
active_channels = set()
default_delay_time = 0 

def clean_text(text):
    decoration_emoji_pattern = re.compile(
        "["  
        u"\U0001F600-\U0001F64F"  
        u"\U0001F300-\U0001F5FF"  
        u"\U0001F680-\U0001F6FF"  
        u"\U0001F1E0-\U0001F1FF"  
        u"\u0300-\u036f"  
        u"\u0489"  
        u"\u1AB0-\u1AFF"  
        u"\u1DC0-\u1DFF"  
        u"\u20D0-\u20FF"  
        u"\uFE20-\uFE2F"  
        "]+",
        flags=re.UNICODE,
    )
    return decoration_emoji_pattern.sub(r'', text)

async def can_send_comment(channel_id):
    try:
        result = await telegram_client(functions.channels.GetParticipantRequest(channel=channel_id, participant='me'))
        return result.participant.can_send_messages
    except:
        return False

def prepare_response(text):
    for word, replacement in replacement_dict.items():
        text = text.replace(word, replacement)
    text = clean_text(text)
    return text.strip()

def extract_text_within_parentheses(text):
    return re.findall(r'\(([^()]*)\)', text)

def process_response_parentheses(message, response):
    if any(message.lower().endswith(x) for x in [
    ' مع اقواس', ' مع اقواص',
    ' بي اقواس', ' بي اقواص',
    ' بي الاقواس', ' بي الاقواص',
    ' مع الاقواس', ' مع الاقواص',
    ' بل اقواس', ' بل اقواص',
    ' بل اقواص', ' بل اقواص',
    ' بالاقواس', ' بالاقواص',
    'مع اقواس', 'مع اقواص',
    'بي اقواس', 'بي اقواص',
    'بي الاقواس', 'بي الاقواص',
    'مع الاقواس', 'مع الاقواص',
    'بل اقواس', 'بل اقواص',
    'بالاقواس', 'بالاقواص'
]):
        response = f"({response})"
    elif any(message.lower().endswith(x) for x in [
    ' بدون اقواس', ' بدون اقواص',
    ' من غير اقواس', ' من غير اقواص',
    ' بلاقواس', ' بلاقواص',
    'بدون اقواس', 'بدون اقواص',
    'من غير اقواس', 'من غير اقواص',
    'بلاقواس', 'بلاقواص',
]):
        pass
    return response

async def fetch_user_info(user_id):
    try:
        user = await telegram_client.get_entity(user_id)
        return f"[{user.first_name}](tg://user?id={user_id})"
    except:
        return f"[غير معروف](tg://user?id={user_id})"

@telegram_client.on(events.NewMessage())
async def message_handler(event):
    global default_delay_time
    sender_id = (await event.get_sender()).id
    message_text = event.raw_text.strip()

    if sender_id == admin_mode:
        if message_text.lower().startswith('/s '):
            user_id = int(message_text.split()[1])
            if len(user_id_set) < 10:
                user_id_set.add(user_id)
                await event.delete()
            else:
                await event.reply("لا يمكنك إضافة أكثر من 10 مستخدمين.")
            return

        if message_text.lower().startswith('/set '):
            channel_id = int(message_text.split()[1])
            active_channels.add(channel_id)
            await event.delete()
            return

        if message_text.lower() == "/ls":
            user_list = [f"{index + 1}. {user_id} - {await fetch_user_info(user_id)}" for index, user_id in enumerate(user_id_set)]
            channel_list = [f"{index + 1}. {channel_id}" for index, channel_id in enumerate(active_channels)]
            response_text = "مستخدمين الاوامر:\n" + "\n".join(user_list) + "\n\nالقنوات المفعلة:\n" + "\n".join(channel_list)
            await event.reply(response_text)
            return

        if message_text.lower().startswith('/r '):
            index = int(message_text.split()[1])
            if 1 <= index <= len(user_id_set):
                user_id = list(user_id_set)[index - 1]
                user_id_set.remove(user_id)
                await event.reply(f"تم حذف {user_id}.")
            else:
                await event.reply("الرقم غير صحيح.")
            return

        if message_text.lower().startswith('/rm '):
            index = int(message_text.split()[1])
            if 1 <= index <= len(active_channels):
                channel_id = list(active_channels)[index - 1]
                active_channels.remove(channel_id)
                await event.reply(f"تم حذف القناة {channel_id}.")
            else:
                await event.reply("الرقم غير صحيح.")
            return

        if message_text.lower().startswith('/time '):
            try:
                default_delay_time = int(message_text.split()[1])
                await event.reply(f"تم ضبط وقت التأخير إلى {default_delay_time} ثانية.")
            except ValueError:
                await event.reply("الرجاء إدخال رقم صالح.")
            return

        if message_text.lower() == "/help":
            help_text = (
                "`/set -100` [channel_id] - تفعيل القناة.\n"
                "`/s` [user_id] - تعيين مستخدم لمراقبته.\n"
                "`/ls` - عرض قائمة المستخدمين المراقبين مع أسمائهم وروابطهم والقنوات المفعلة.\n"
                "`/r` [index] - حذف مستخدم من قائمة المراقبين حسب الرقم.\n"
                "`/rm` [index] - حذف قناة من قائمة القنوات المفعلة حسب الرقم.\n"
                "`/time` [seconds] - تعيين وقت التأخير بالثواني."
            )
            await event.reply(help_text)
            return

    if sender_id in user_id_set:
        if event.chat_id in active_channels:
            parentheses_matches = extract_text_within_parentheses(message_text)
            keyword_match = re.search(r'\b(?:' + '|'.join(keyword_list) + r')\b\s*(.*)', message_text)
            username_match = re.search(r'@(\w+)', message_text)

            if username_match:
                username = username_match.group(0)
                cleaned_message = prepare_response(message_text)
                response = cleaned_message.replace(username, "").strip()
                if parentheses_matches:
                    response_content = parentheses_matches[0]
                    response = process_response_parentheses(message_text, response_content)
                await asyncio.sleep(default_delay_time)
                await telegram_client.send_message(username, response)
                return

            if parentheses_matches:
                response = parentheses_matches[0]
                response = process_response_parentheses(message_text, response)
                if response:  
                    await asyncio.sleep(default_delay_time)
                    await event.reply(response)
            elif keyword_match:
                response = prepare_response(keyword_match.group(1))
                if response:  
                    await asyncio.sleep(default_delay_time)
                    await event.reply(response)
            if message_text.lower() in ["First", "FIRST", "first one", "First one", "FIRST", "first"]:
                await asyncio.sleep(default_delay_time)
                await event.reply("ok")
            else:
                math_matches = re.findall(r'(\d+(?:\.\d+)?[\+\-\*/]\d+(?:\.\d+)?)', message_text)
                if math_matches:
                    for expr in math_matches:
                        try:
                            result = eval(expr)
                            await asyncio.sleep(default_delay_time)
                            await event.reply(f" {result}")
                        except:
                            await event.reply(f"Error in evaluating '{expr}'")

telegram_client.run_until_disconnected()
