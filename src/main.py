import user
from flask import *
from flask_api import status
import os

app = Flask(__name__)
app.config['UPLOADED_ICONSET_DEST'] = '/home/gznews/icon'
user.setapp(app)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/login', methods=['POST'])
def login():
    print(request.values)
    name = request.form['name']
    passwd = request.form['passwd']
    print("login: {} {}".format(name, passwd))
    if user.valid_login(name, passwd):
        return jsonify({"msg": "Success"})
    else:
        return jsonify({"msg": "Wrong username or password"}), status.HTTP_401_UNAUTHORIZED

@app.route('/register',  methods=['POST'])
def register():
    name = request.form['name']
    passwd = request.form['passwd']
    print("register: {} {}".format(name, passwd))
    if user.has_name(name):
        return jsonify({"msg": "Username is used"}), status.HTTP_401_UNAUTHORIZED
    else:
        user.do_register(name, passwd)
        return jsonify({"msg": "Success"})

@app.route('/uploadIcon',  methods=['POST'])
def uploadIcon():
    print(request.files)
    name = request.form['name']
    icon = request.files['icon']
    if not user.has_name(name):
        return jsonify({"msg": "No such user"}), status.HTTP_401_UNAUTHORIZED
    user.save_icon(name, icon)
    return jsonify({"msg": "Success"})

@app.route('/getIcon', methods=['GET'])
def get_icon():
    print(request.args)
    name = request.args.get('name')
    needLarge = (request.args.get('size').strip() == 'large')
    if not user.has_name(name):
        return jsonify({"msg": "No such user"}), status.HTTP_401_UNAUTHORIZED
    icon_path = user.get_icon(name, needLarge)
    if icon_path is None:
        return jsonify({"msg": "No icon"}), status.HTTP_401_UNAUTHORIZED
    print("get icon from " + icon_path)
    return send_from_directory(app.config['UPLOADED_ICONSET_DEST'], icon_path)

@app.route('/postComment', methods=['post'])
def post_comment():
    name = request.form['name']
    newsID = request.form['newsID']
    text = request.form['text']
    print("postComment: {} {} {}".format(name, newsID, text))
    if not user.has_name(name):
        return jsonify({"msg": "No such user"}), status.HTTP_401_UNAUTHORIZED
    else:
        user.save_comment(name, newsID, text)
        return jsonify({"msg": "Success"})

@app.route('/getComment', methods=['GET'])
def get_comment():
    print(request.args)
    newsID = request.args.get("newsID")
    comments = user.get_comment(newsID)
    return jsonify({"msg": comments})

if __name__ == '__main__':
    user.do_register("heheda", "123456")
    app.run(host='0.0.0.0', debug=True)
    
