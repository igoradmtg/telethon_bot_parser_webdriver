# -*- coding: utf-8 -*-
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# https://github.com/igoradmtg/
import time
import os
import re
import json
from telethon import TelegramClient, events, utils, Button
from settings import API_ID, API_HASH, BOT_TOKEN, ADMIN_PASSWORD
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from time import sleep
#import web_driver
import admin
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

#close_browser = True # Close browser window after parser
#show_browser = False # Show browser window
close_browser = False # Close browser window after parser
show_browser = True # Show browser window
max_pages = 100 # Maximum test pages
#firefox = FirefoxBinary("C:\Program Files\\Mozilla Firefox\\firefox.exe")
timesleep = [1,0.5]

def get_tovar_number_from_link(tovar_link):
    match = re.search(r'\/([0-9]+)\/',tovar_link)
    #print(match)
    if match:
        return match.group(1)
    else:    
        return ""


async def get_tovar_param(chat_id,tovar_number_user,tovar_name_user, event):
    #browser = webdriver.Firefox(firefox_binary=firefox) # Показывать экран браузера
    #if show_browser:
    #    browser = webdriver.Firefox()
    #else:
    #    options = Options() # Не показывать экран браузера
    #    options.add_argument('--headless') # Не показывать экран браузера
    #    browser = webdriver.Firefox(options=options) # НЕ показывать экран браузера
    #browser = webdriver.Chrome()
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.implicitly_wait(4) # seconds
    browser.get('https://www.wildxxxxxx.ru/')
    assert 'Wildxxxxxx' in browser.title
    elem = browser.find_element_by_class_name('search-catalog__input')  # Find the search box
    elem.send_keys(tovar_name_user.strip() + Keys.RETURN)
    num_page = 1 # Текущий номер страницы
    await event.edit("🔎 <b>Поиск запущен..</b> Ранжирование артикула проверяется в полной версии сайта для компьютеров.\r\nТекущая страница: "+str(num_page),parse_mode='html')
    time.sleep(timesleep[0])
    #with open("test.html", "w", encoding='utf-8') as f:
    #    f.write(browser.page_source)
    # Поиск строки: По Вашему запросу ничего не найдено. searching-results__text
    #with open("test.html", "w", encoding='utf-8') as f:
    #    f.write(browser.page_source)
    list_pages = [] # Массив ссылок
    
    try:
        elem = browser.find_element_by_css_selector('p.searching-results__text')
    except Exception as err:
        print(err)
        elem = False
        
    if not elem == False :
        str_p = str(elem.text).strip()
        #print(str_p)
        if str_p == "По Вашему запросу ничего не найдено.":
            print(str_p)
            if close_browser:
                browser.quit()
            return {"result":False,"text":str_p}
    #        
    # Поиск первой ссылки на товар
    
    find_row_link = 0 # Найденный номер
    find_num_page = 0 # Найденная позиция
    while True:
        count_link = 0
        list_a = browser.find_elements_by_class_name('product-card__main')
        if len(list_a)>0 :
            tovar_link = ""
            tovar_count = 0
            for elm_a in list_a:
                tovar_count += 1
                count_link += 1
                try:
                    tovar_link = str(elm_a.get_attribute('href'))
                except Exception as err:
                    print(err)
                    continue
                tovar_number = get_tovar_number_from_link(tovar_link)
                if tovar_number_user == tovar_number:
                    find_row_link = count_link
                    find_num_page = num_page
                # print(tovar_count,tovar_link,tovar_number)
        if count_link == 0:
            print("Нет ссылок на товары")
            if close_browser:
                browser.quit()
            return {"result":False,"text":"Нет ссылок на товары"}
        if find_row_link > 0:
            break
        #print("Не найден артикул товара")
            
        # <a href="https://www.wildxxxxxx.ru/catalog/0/search.aspx?search=%D1%88%D0%B0%D0%BC%D0%BF%D1%83%D0%BD%D1%8C&amp;xsearch=true&amp;page=4" class="pagination-item" data-link="{on ~updatePage (+value)}" data-jsv="#905^/905^">4</a>
        try:
            elm_a_page_next = browser.find_element_by_css_selector('a.pagination-next')
        except Exception as err:
            print(err)
            elm_a_page_next = False
        if elm_a_page_next != False:
            num_page += 1
            try:
                page_link = str(elm_a_page_next.get_attribute('href'))
            except Exception as err:
                print(err)
                break
            #page_text = str(elm_a_page_next.text)
            #print("Page text",page_text)
            #print("Num page",num_page,"Page url",page_link)
            #text_respond = "Num page " + str(num_page)
            await event.edit("🔎 <b>Поиск запущен..</b> Ранжирование артикула проверяется в полной версии сайта для компьютеров.\r\nТекущая страница: "+str(num_page),parse_mode='html')
            if num_page>max_pages:
                break
            elm_a_page_next.click()    
            time.sleep(timesleep[1])
        else:
            break
                
    if find_row_link == 0:
        print("Не найден артикул товара")
        if close_browser:
            browser.quit()
        return {"result":False,"text":"Не найден артикул товара"}
            
    str_return = '\U0001F609' + "<b>Артикул "+tovar_number_user+" по запросу " + tovar_name_user + " найден:</b>\r\n" + \
        "Страница: " + str(find_num_page) + "\r\n" + \
        "Позиция: " + str(find_row_link) + "\r\n"
    #print(str_return)    
    if close_browser:
        browser.quit()
    return {"result":True,"text":str_return,"find_num_page":find_num_page,"find_row_link":find_row_link}

def close_browser():
    browser.quit()


bot = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)
dir_images = os.path.join("input","img") # Dir input img
dir_document = os.path.join("input","doc") # Dir input doc
dir_users = os.path.join("input","users") # Dir input doc
dir_task = os.path.join("input","task") # Dir input task
if not os.path.isdir(dir_images):
    os.makedirs(dir_images)
if not os.path.isdir(dir_document):
    os.makedirs(dir_document)
if not os.path.isdir(dir_task):
    os.makedirs(dir_task)
if not os.path.isdir(dir_users):
    os.makedirs(dir_users)

user_info = []
user_admin = []
file_user_info = ""
file_admin_info = ""

def get_admin_btn():
    markup = bot.build_reply_markup(
        [
            [Button.inline('\U00002709' + ' Разослать спам', 'sendspam')],
            [Button.inline('\U0001F680' + ' Загрузить фото для спама', 'spamphoto')],
            [Button.inline('\U0001F681' + ' Новый текст для спама', 'spamtext')],
            [Button.inline('\U0001F682' + ' Просмотр спам рассылки', 'spamtest')],
            [Button.inline('\U0001F683' + ' Установить ID канала для подписки', 'channelmembers')],
            [Button.inline('\U0001F684' + ' Установить URL канала для подписки', 'channelurl')]
    ])
    return markup
    
def get_return_btn():
    markup = bot.build_reply_markup(
        [
            [Button.inline('\U0001F514' + ' Назад', 'admin')]
    ])
    return markup

def get_file_admin_info(chat_id):
    """Set file_user_info"""
    global file_user_info
    file_user_info = os.path.join(dir_users,"us"+str(chat_id)+".json")
    print("get_file_admin_info",file_user_info)

def get_file_user_info(chat_id):
    """Set file_user_info"""
    global file_user_info
    file_user_info = os.path.join(dir_task,"us"+str(chat_id)+".json")
    print("file_user_info",file_user_info)

def read_json():
    """Read file JSON"""
    global user_info,file_user_info
    print("read json :", file_user_info)
    try:
        with open(file_user_info) as json_file:
            user_info = json.load(json_file)
    except Exception:
        user_info = []
    return True

def save_json():
    """Save file JSON"""
    global user_info,file_user_info
    print("save json :", file_user_info)
    with open(file_user_info,'w') as json_file:
        json.dump(user_info,json_file)
    return True

def subscribe_text_to_json(num):
    """Podpiska na tovar"""
    global user_info
    read_json()
    tovar_number = ""
    tovar_name = ""
    try:
        user_info[num]={"tovar_number":user_info[num]["tovar_number"],"tovar_name":user_info[num]["tovar_name"],"update":1}
        tovar_number = user_info[num]["tovar_number"]
        tovar_name = user_info[num]["tovar_name"]
    except Exception as err:
        print(err)
    save_json()    
    return {"tovar_number":tovar_number,"tovar_name":tovar_name}

def unsubscribe_text_to_json(num):
    """Podpiska na tovar"""
    global user_info
    read_json()
    tovar_number = ""
    tovar_name = ""
    try:
        user_info[num]={"tovar_number":user_info[num]["tovar_number"],"tovar_name":user_info[num]["tovar_name"],"update":0}
        tovar_number = user_info[num]["tovar_number"]
        tovar_name = user_info[num]["tovar_name"]
    except Exception as err:
        print(err)
    save_json()    
    return {"tovar_number":tovar_number,"tovar_name":tovar_name}
    

def add_text_to_json(chat_id,tovar_number,tovar_name): 
    """Add text to user file json"""
    global user_info
    get_file_user_info(chat_id)
    read_json()
    find_row = 0
    is_find_text = False
    if len(user_info)>0:
        cnt = 0
        for row_info in user_info:
            if ((row_info["tovar_number"] == tovar_number) and (row_info["tovar_name"] == tovar_name)):
                is_find_text = True
                find_row = cnt
            cnt += 1    
    if is_find_text == False:
        find_row = len(user_info)
        user_info.append({"tovar_number":tovar_number,"tovar_name":tovar_name,"update":0})
    save_json()    
    return find_row
    
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    """Send a message when the command /start is issued."""
    sender = await event.get_sender()
    name = utils.get_display_name(sender)
    print("start. Sender",name,"say",event.text)
    #await event.respond('Hi!')
    await event.respond("<b>Узнайте, на каких позициях находится ваш товар в поиске WildXXXXX</b>\r\n"+"Введите артикул и запрос который вас интересует, например: <code>22695156 чехол для iPhone 12</code>.",parse_mode='html')
    raise events.StopPropagation

@bot.on(events.NewMessage(pattern='([0-9]* \S*)'))
async def numbers(event):
    sender = await event.get_sender()
    name = utils.get_display_name(sender)
    chat_id = event.sender_id
    print("Chat_id",chat_id)
    info_members = admin.get_chat_member(BOT_TOKEN,chat_id)
    if info_members == False:
        print("info_members False")
        channel_url = admin.get_chanel_url()
        markup = bot.build_reply_markup(
            [
                [Button.url('\U0001F514' + ' Подписаться', channel_url)],
        ])
        
        await event.respond("Сервис доступен только для подписанных на канал",parse_mode='html',buttons=markup)

        raise events.StopPropagation
        return
    text = str(event.text).replace("`","")
    text_list = re.split(r' ',text)
    tovar_number = '' # Tovar number
    tovar_name = '' # Tovar name
    for text_word in text_list:
        if not tovar_number:
            tovar_number += text_word
        else:
            tovar_name += text_word + " " 
    tovar_number = tovar_number.strip()        
    tovar_name = tovar_name.strip()
    print("tovar_number:",tovar_number,"tovar_name:",tovar_name)
    #await event.reply('Tovar number: ' + tovar_number)
    #await event.reply('Tovar name: ' + tovar_name) '\U0001F609'
    msg = await event.respond("🔎 <b>Поиск запущен..</b> Ранжирование артикула проверяется в полной версии сайта для компьютеров.",parse_mode='html')
    info_webdriver = await get_tovar_param(chat_id,tovar_number,tovar_name,msg) # Execute parser 
    text_respond = info_webdriver["text"] # Text for user
    result_parser = info_webdriver["result"] # Resultat for save user info
    await msg.delete()
    #print(text_respond)
    if result_parser:    
        row_list = add_text_to_json(chat_id,tovar_number,tovar_name) # Сохраняем
    if result_parser and (len(text_respond)>0):
        markup = bot.build_reply_markup(
            [
                [Button.inline('\U0001F514' + ' Подписаться', 'podpis_'+str(row_list))],
                [Button.inline('\U0001F504' + ' Обновить', 'update_'+str(row_list))]
        ])
        await event.respond(text_respond, parse_mode='html', buttons=markup)
    elif len(text_respond)>0:
        await event.respond(text_respond,parse_mode='html')
    raise events.StopPropagation

async def get_users_from_chat():
    """Error user only NOT BOT"""
    offset=0
    limit=100
    my_channel = 'https://t.me/joinchat/kDBYY9Ds85ZiN2Vi'
    channel = await bot.get_entity(my_channel)
    while True:
        participants = await bot(GetParticipantsRequest(
            channel, ChannelParticipantsSearch(''), offset, limit,
            hash=0
        ))
        print(participants)
        break
        if not participants.users:
            break
        #all_participants.extend(participants.users)
        offset += len(participants.users)
        print(participants.users)

@bot.on(events.CallbackQuery())
async def handlerCallbackQuery(event):
    global user_info,dir_task
    chat_id = event.sender_id
    await event.answer()
    text_respond = event.data.decode('utf-8')
    print(text_respond)    
    get_file_user_info(chat_id)
    if text_respond == "sendspam":
        #await event.respond("sendspam", parse_mode='html')
        await event.delete()
        user_list = admin.get_all_users(dir_task)
        spam_info = admin.get_spam_info()
        for user_id in user_list:
            user_id = int(user_id)
            if spam_info["image"] != False:
                await bot.send_file(user_id, file = spam_info["image"],caption = spam_info["text"],parse_mode='html')
            else:
                await bot.send_message(user_id, spam_info["text"], parse_mode='html')
            
        await event.respond('Рассылка завершена', parse_mode='html', buttons=get_return_btn())    
    elif text_respond == "spamphoto":
        await event.respond("Загрузите фото для <b>СПАМ рассылки</b>", parse_mode='html')
    elif text_respond == "channelmembers":
        admin.start_cmd(chat_id,"channelmembers")
        await event.respond("Введите <b>ID или имя канала</b> для подписки", parse_mode='html')
    elif text_respond == "channelurl":
        admin.start_cmd(chat_id,"channelurl")
        await event.respond("Введите <b>URL канала</b> для подписки", parse_mode='html')
    elif text_respond == "spamtext":
        admin.start_cmd(chat_id,"spamtext")
        await event.respond("Введите текст для <b>СПАМ рассылки</b>", parse_mode='html')
    elif text_respond == "spamtest":
        await event.delete()
        spam_info = admin.get_spam_info()
        if spam_info["image"] != False:
            await bot.send_file(chat_id, file = spam_info["image"],caption = spam_info["text"],parse_mode='html')
        else:
            await bot.send_message(chat_id, spam_info["text"], parse_mode='html')
        await event.respond('Панель администратора. Выберите действие', parse_mode='html', buttons=get_admin_btn())    
    elif text_respond == "admin":        
        await event.delete()
        await event.respond('Панель администратора. Выберите действие', parse_mode='html', buttons=get_admin_btn())
    elif str(text_respond).find('podpis_')>-1:
        num_row_json = int(text_respond.replace('podpis_',''))
        print("Podpis",num_row_json)
        tovar_info = subscribe_text_to_json(num_row_json)
        message = await event.get_message()
        print(message)
        msg_id=utils.get_message_id(message)
        print(msg_id)
        await message.delete()
        markup = bot.build_reply_markup(
            [
                [Button.inline('\U0001F514' + ' Отписаться', 'otpis_'+str(num_row_json))],
                [Button.inline('\U0001F504' + ' Обновить', 'update_'+str(num_row_json))]
        ])
        await event.respond('Включена подписка на товар '+tovar_info["tovar_name"]+" Артикул "+tovar_info["tovar_number"],parse_mode='html', buttons=markup)
    elif str(text_respond).find('otpis_')>-1:
        num_row_json = int(text_respond.replace('otpis_',''))
        print("Podpis",num_row_json)
        tovar_info = unsubscribe_text_to_json(num_row_json)
        message = await event.get_message()
        print(message)
        msg_id=utils.get_message_id(message)
        print(msg_id)
        await message.delete()
        markup = bot.build_reply_markup(
            [
                [Button.inline('\U0001F514' + ' Подписаться', 'podpis_'+str(num_row_json))],
                [Button.inline('\U0001F504' + ' Обновить', 'update_'+str(num_row_json))]
        ])
        await event.respond('Отключена подписка на товар '+tovar_info["tovar_name"]+" Артикул "+tovar_info["tovar_number"],parse_mode='html', buttons=markup)
        #await event.edit(message)
    elif str(text_respond).find('update_')>-1:
        print("Update")
        msg = await event.edit("🔎 <b>Поиск запущен..</b> Ранжирование артикула проверяется в полной версии сайта для компьютеров.",parse_mode='html')
        num_row_json = int(text_respond.replace('update_',''))
        print("Update",num_row_json)
        read_json()
        try:
            tovar_number = user_info[num_row_json]["tovar_number"]
            tovar_name = user_info[num_row_json]["tovar_name"]
        except Exception as err:
            print(err)
        info_webdriver = await get_tovar_param(chat_id,tovar_number,tovar_name, event) # Execute parser 
        text_respond = info_webdriver["text"] # Text for user
        result_parser = info_webdriver["result"] # Resultat for save user info
        await event.delete()
        #print(text_respond)
        if result_parser:    
            row_list = add_text_to_json(chat_id,tovar_number,tovar_name) # Сохраняем
        if result_parser and (len(text_respond)>0):
            markup = bot.build_reply_markup(
                [
                    [Button.inline('\U0001F514' + ' Подписаться', 'podpis_'+str(row_list))],
                    [Button.inline('\U0001F504' + ' Обновить', 'update_'+str(row_list))]
            ])
            await event.respond(text_respond, parse_mode='html', buttons=markup)
        elif len(text_respond)>0:
            await event.respond(text_respond,parse_mode='html')
    raise events.StopPropagation

@bot.on(events.CallbackQuery(data = b'yes'))
async def handler(event):
    if event.data == b'yes':
        await event.answer('Correct answer!')
    raise events.StopPropagation    

@bot.on(events.CallbackQuery(data=b'no'))
async def handler(event):
    # Pop-up message with alert
    await event.answer('Wrong answer!', alert=True)
    raise events.StopPropagation

@bot.on(events.CallbackQuery(data=b'super'))
async def handler(event):
    # Pop-up message with alert
    chat_id = event.sender_id
    await event.answer()
    await bot.send_message(chat_id, 'click me')
    raise events.StopPropagation

@bot.on(events.CallbackQuery(data=b'super'))
async def handler(event):
    # Pop-up message with alert
    chat_id = event.sender_id
    await event.answer()
    await bot.send_message(chat_id, 'click me')
    raise events.StopPropagation
                    
@bot.on(events.NewMessage(pattern='/btn2'))
async def buttonstst(event):
    chat_id = event.sender_id
    markup = bot.build_reply_markup([[Button.inline('hi', b'yes')],[Button.inline('hi', b'yes')],[Button.inline('hi', b'yes')]])
    await bot.send_message(chat_id, 'click me', buttons=markup)
    raise events.StopPropagation
                    
@bot.on(events.NewMessage(pattern='/btn1'))
async def buttonstst(event):
    chat_id = event.sender_id
    markup = bot.build_reply_markup([[Button.inline('hi', b'yes')],[Button.inline('hi', b'yes')],[Button.inline('hi', b'yes')]])
    await bot.send_message(chat_id, 'click me', buttons=markup)
    raise events.StopPropagation
    #await bot.send_message(chat_id, 'Yes or no?', buttons=[
    #    Button.inline('Yes!', b'yes'),
    #    Button.inline('No', b'yes'),
    #    Button.inline('Super', b'yes')
    #])
    
@bot.on(events.NewMessage(pattern='/getuser'))
async def buttonstst(event):
    chat_id = event.sender_id
    await bot.send_message(chat_id, 'get user')
    #await get_users_from_chat()
    raise events.StopPropagation

@bot.on(events.NewMessage(pattern='/getmembers'))
async def buttonstst(event):
    chat_id = event.sender_id
    await bot.send_message(chat_id, 'getmembers')
    info_members = admin.get_chat_member(BOT_TOKEN,chat_id)
    if (info_members == False):
        print("False")
    print(info_members)
    #await get_users_from_chat()
    raise events.StopPropagation


@bot.on(events.NewMessage(pattern=r'/admin \S+'))
async def buttonstst(event):
    chat_id = event.sender_id
    text = str(event.text)
    text_pass = text.replace('/admin ','').strip()
    print("text_pass",text_pass)
    if text_pass != ADMIN_PASSWORD:
        await bot.send_message(chat_id, 'Пароль не правильный')
    else:    
        await event.respond('Панель администратора. Выберите действие', parse_mode='html', buttons=get_admin_btn())
        admin.set_admin(chat_id)
    #await get_users_from_chat()
    raise events.StopPropagation
                    
@bot.on(events.NewMessage)
async def echo(event):
    """Echo the user message."""
    sender = await event.get_sender()
    name = utils.get_display_name(sender)
    chat_id = event.sender_id
    text = str(event.text)
    #print("NewMessage. Sender",name,"say",text)
    #print(event)
    if admin.is_admin(chat_id):
        admin_cmd = admin.get_cmd(chat_id)
        if admin_cmd == "spamtext":
            admin.save_text_spam(text)
            await event.respond('Спам сохранили',buttons = get_return_btn())
            admin.set_admin(chat_id)
            return
        elif admin_cmd == "channelmembers":
            admin.save_text_chanel(text)
            await event.respond('Канал для подписки сохранили',buttons = get_return_btn())
            admin.set_admin(chat_id)
            return
        elif admin_cmd == "channelurl":
            admin.save_url_chanel(text)
            await event.respond('Канал для подписки сохранили',buttons = get_return_btn())
            admin.set_admin(chat_id)
            return
    text_error = "<b>Неверный формат</b>\r\n" + "В запросе должен быть сначала <i>артикул</i>, после чего <i>ключевое слово</i>. Пример: <code>22695156 чехол для iPhone 12.</code> \r\n"
    if event.photo:
        if admin.is_admin(chat_id):
            await event.reply('Start download file')
        path = await event.download_media(file=dir_images)
        print('File saved to', path)  # printed after download is done        
        if admin.is_admin(chat_id):
            image_spam = admin.copy_image_spam(path)
            await event.respond('File saved to ' + image_spam,buttons = get_return_btn())
    elif event.document:
        #await event.reply('Start download file')
        path = await event.download_media(file=dir_document)
        print('File saved to', path)  # printed after download is done        
        #await event.respond('File saved to ' + path)
    elif len(text)>0:
        await event.respond(text_error + event.text,parse_mode='html')
    else:
        await event.respond(text_error + event.text,parse_mode='html')

def main():
    """Start the bot."""
    try:
        print('(Press Ctrl+C to stop this)')
        bot.run_until_disconnected()
    finally:
        bot.disconnect()
        

if __name__ == '__main__':
    main()
