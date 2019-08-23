import user
from flask import request
from flask import Flask
app = Flask(__name__)


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
        return "Success"
    else:
        return "Fail"

@app.route('/register',  methods=['POST'])
def register():
    name = request.form['name']
    passwd = request.form['passwd']
    print("register: {} {}".format(name, passwd))
    if user.has_name(name):
        return "FailUserNameUsed"
    else:
        user.do_register(name, passwd)
        return "Success"



# @app.route('/user/<username>')
# def show_user_profile(username):
#     # show the user profile for that user
#     return 'User %s' % username

# @app.route('/post/<int:post_id>')
# def show_post(post_id):
#     # show the post with the given id, the id is an integer
#     return 'Post %d' % post_id

if __name__ == '__main__':
    user.do_register("heheda", "123456")
    app.run(host='0.0.0.0', debug=True)
    
