from flask import Flask, request, current_app
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

app = None
iconset = None

def setapp(app_main):
    global app
    global iconset
    app = app_main
    iconset = UploadSet('iconset', IMAGES)
    configure_uploads(app, iconset)
    print(app, iconset)
    
class User:
    def __init__(self, name, passwd):
        self.name = name
        self.passwd = passwd
        self.icon = None

userName = {}

def valid_login(name, passwd):
    name = name.strip()
    passwd = passwd.strip()
    return has_name(name) and userName[name].passwd == passwd

def do_register(name, passwd):
    name = name.strip()
    passwd = passwd.strip()
    user = User(name, passwd)
    userName[name] = user

def has_name(name):
    name = name.strip()
    return name in userName

def save_icon(name, icon):
    name = name.strip()
    filename = iconset.save(icon, name=name+'.')
    userName[name].icon = filename
    print("save icon to " + filename)

def get_icon(name):
    name = name.strip()
    return userName[name].icon


