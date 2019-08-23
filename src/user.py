class User:
    def __init__(self, name, passwd):
        self.name = name
        self.passwd = passwd

userName = {}

def valid_login(name, passwd):
    name = name.strip()
    passwd = passwd.strip()
    return userName[name].passwd == passwd

def do_register(name, passwd):
    name = name.strip()
    passwd = passwd.strip()
    user = User(name, passwd)
    userName[name] = user

def has_name(name):
    name = name.strip()
    return name in userName
