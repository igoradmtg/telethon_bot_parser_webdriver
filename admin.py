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

import os
import json
import requests
from shutil import copyfile
from settings import CHANNEL_NAME

dir_admin = os.path.join("input","admin") # Dir input doc
spam_image = os.path.join(dir_admin,"_spam.jpg") # Image filename
spam_text = os.path.join(dir_admin,"_spam.txt") # Text filename
file_channel_name = os.path.join(dir_admin,"_channel.txt") # File name channel ID
channel_url = os.path.join(dir_admin,"_channel_url.txt") # File name channel URL

if not os.path.isdir(dir_admin):
    os.makedirs(dir_admin)

def get_file_admin(user_id):
    global dir_admin
    return os.path.join(dir_admin,"adm"+str(user_id)+".json")

def is_admin(user_id):
    file_admin = get_file_admin(user_id)
    if os.path.isfile(file_admin):
        return True
    else:
        return False

def set_admin(user_id):
    file_admin = get_file_admin(user_id)
    print(file_admin)
    admin_info = {"user_id":user_id}
    with open(file_admin,'w') as json_file:
        json.dump(admin_info,json_file)
    
def copy_image_spam(path):
    global spam_image 
    copyfile(path, spam_image)  
    return spam_image
        
def save_text_spam(text):
    global spam_text 
    with open(spam_text,'w',encoding="utf-8") as text_file:
        text_file.write(text)

def save_text_chanel(text):
    global file_channel_name 
    with open(file_channel_name,'w',encoding="utf-8") as text_file:
        text_file.write(text.replace('*','').replace("'",''))

def save_url_chanel(text):
    global channel_url 
    with open(channel_url,'w',encoding="utf-8") as text_file:
        text_file.write(text.replace('*','').replace("'",''))
        
def start_cmd(user_id,cmd):        
    file_admin = get_file_admin(user_id)
    print("start_cmd",file_admin)
    admin_info = {"user_id":user_id,"cmd":cmd}
    with open(file_admin,'w') as json_file:
        json.dump(admin_info,json_file)

def get_cmd(user_id):    
    file_admin = get_file_admin(user_id)
    print("get_cmd",file_admin)
    try:
        with open(file_admin) as json_file:
            admin_info = json.load(json_file)
    except Exception:
        admin_info = {"user_id":user_id}
    return admin_info.get("cmd",False)

def get_spam_info():
    global spam_image,spam_text
    values_ret = {"image":False,"text":"Empty"}
    if os.path.isfile(spam_image):
        values_ret["image"] = spam_image
    try:
        with open(spam_text,'r',encoding="utf-8") as text_file:
            text = text_file.read()
    except Exception:
        text = "Empty"
    values_ret["text"] = text
    return values_ret        
    
def get_all_users(user_dir):    
    user_list=[]
    onlyfiles = [f for f in os.listdir(user_dir) if os.path.isfile(os.path.join(user_dir, f))]
    for file_name in onlyfiles:
        bname = os.path.basename(file_name)
        user_list.append(bname.replace("us","").replace(".json",""))
    print(user_list)
    return user_list    
        
def get_all_users_file(user_dir):    
    onlyfiles = [f for f in os.listdir(user_dir) if os.path.isfile(os.path.join(user_dir, f))]
    print(onlyfiles)
    return onlyfiles    
    
def read_json(filejson):
    """Read file JSON"""
    print("read json :", filejson)
    try:
        with open(filejson) as json_file:
            user_info = json.load(json_file)
    except Exception:
        user_info = []
    return user_info
    
def get_chat_member(bot_token,user_id):    
    """Get chat member"""
    try:
        with open(file_channel_name,'r',encoding="utf-8") as text_file:
            chat_id = text_file.read()
        url="https://api.telegram.org/bot"+bot_token+"/getChatMember?chat_id="+chat_id+"&user_id="+str(user_id)
        response = requests.get(url)
        member_info = response.json()    
        print(member_info)
        if member_info['ok']==True:
            if member_info['result']['status']=='creator':
                return True
            elif member_info['result']['status']=='administrator':
                return True
            elif member_info['result']['status']=='member':
                return True
            elif member_info['result']['status']=='restricted':
                return True
            
        return False            
    except Exception as err:
        print(err)
        return False

def get_chanel_url():
    global channel_url
    default_url = "https://t.me/joinchat/VTAARYqFTBWXjTBh"
    if not os.path.isfile(channel_url):
        return default_url
    try:
        with open(channel_url,'r',encoding="utf-8") as text_file:
            text = text_file.read()
    except Exception:
        text = default_url
    return text
        
