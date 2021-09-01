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
import os
import re
import json
from telethon import TelegramClient, events, utils, Button
from settings import API_ID, API_HASH, BOT_TOKEN, ADMIN_PASSWORD
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from time import sleep
import web_driver
import admin

bot = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)
dir_images = os.path.join("input","img") # Dir input img
dir_document = os.path.join("input","doc") # Dir input doc
dir_users = os.path.join("input","users") # Dir input doc
dir_task = os.path.join("input","task") # Dir input task

async def main_bot():
    # Getting information about yourself
    me = await bot.get_me()
    # "me" is a user object. You can pretty-print
    # any Telegram object with the "stringify" method:
    #print(me.stringify())
    user_files = admin.get_all_users_file(dir_task)
    username = me.username
    #print(username)
    #print(me.phone)
    for user_file in user_files:
        bname = os.path.basename(user_file)
        chat_id = int(bname.replace("us","").replace(".json",""))
        fullname = os.path.join(dir_task,user_file)
        user_info = admin.read_json(fullname)
        print(fullname)
        row_list = 0
        for info_row in user_info:
            print(info_row)
            if info_row["update"]==1:
                #await bot.send_message(chat_id, 'Hello, myself!')
                tovar_number = info_row["tovar_number"]
                tovar_name = info_row["tovar_name"]
                info_webdriver = web_driver.get_tovar_param(chat_id,tovar_number,tovar_name) # Execute parser 
                text_respond = info_webdriver["text"] # Text for user
                result_parser = info_webdriver["result"] # Resultat for save user info
                #print(text_respond)
                if result_parser and (len(text_respond)>0):
                    markup = bot.build_reply_markup(
                        [
                            [Button.inline('\U0001F514' + ' Отписаться', 'otpis_'+str(row_list))],
                            [Button.inline('\U0001F504' + ' Обновить', 'update_'+str(row_list))]
                    ])
                    await bot.send_message(chat_id,text_respond, parse_mode='html', buttons=markup)
                elif len(text_respond)>0:
                    await bot.send_message(chat_id,text_respond,parse_mode='html')
            row_list += 1
    web_driver.close_browser()

def main():
    """Start the bot."""
    with bot:
        bot.loop.run_until_complete(main_bot())
    

if __name__ == '__main__':
    main()