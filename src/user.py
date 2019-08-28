from flask import Flask, request, current_app
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import cv2
import json
import os
import time
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
        self.iconLarge = None
        self.iconSmall = None

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
    smallFilename = iconset.save(icon, name=name+'_small' + '.')
    icon = cv2.imread(os.path.join(app.config['UPLOADED_ICONSET_DEST'], filename))
    icon = cv2.resize(icon, (299, 299))
    cv2.imwrite(os.path.join(app.config['UPLOADED_ICONSET_DEST'], filename), icon)
    icon = cv2.resize(icon, (99, 99))
    cv2.imwrite(os.path.join(app.config['UPLOADED_ICONSET_DEST'], smallFilename), icon)
    print("save icon to {}, {}".format(filename, smallFilename))
    userName[name].iconLarge = filename
    userName[name].iconSmall = smallFilename
    

def get_icon(name, needLarge):
    name = name.strip()
    return userName[name].iconLarge if needLarge else userName[name].iconSmall

class Comment:
    def __init__(self, name, newsID, text):
        self.name = name
        self.newsID = newsID
        self.text = text

    def __str__(self):
        return self.newsID + " " + self.name + " " + self.text


comments = {}
lastCommentTime = {}

def save_comment(name, newsID, text):
    cur = time.time()
    if name in lastCommentTime and cur - lastCommentTime[name] < 3:
        print("ignore retry")
        lastCommentTime[name] = cur
        return False
    if newsID not in comments:
        comments[newsID] = []
    comments[newsID].append(Comment(name, newsID, text))
    for key, value in comments.items():
        print(key)
        for x in value:
            print(x)
    lastCommentTime[name] = cur
    return True

def get_comment(newsID):
    if newsID not in comments:
        return []
    ret = [{
            'name': x.name, 
            'newsID': x.newsID, 
            'text': x.text
        } for x in comments[newsID]]
    print(ret)
    return ret