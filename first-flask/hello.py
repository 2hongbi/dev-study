from flask import Flask, render_template, redirect, url_for, abort
from flask.views import View

# __name__ : 이 인자는 정적 파일과 템플릿을 찾는 데 쓰임
app = Flask(__name__, static_folder='static', template_folder='templates')


class UserList(View):
    methods = ['GET', 'POST']   # GET, POST, PUT, DELETE

    def dispatch_request(self):
        users = []
        return render_template('users.html', users=users)


app.add_url_rule('/users', view_func=UserList.as_view('user_list'))


@app.route('/')
def index():
    return redirect(url_for('user_list'))


@app.errorhandler(403)
def permission_denied(error):
    return '페이지를 찾을 수 없습니다', 403


@app.route('/users')
def user_list():
    # abort(403)
    users = []
    return render_template('users.html', users=users)


@app.route('/index')    # route는 중첩할 수 있음
def hello_world():
    return 'Hello, World!'


@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/users/<username>')
def get_user(username):
    return username


@app.route('/posts/<int:post_id>')
def get_post(post_id):
    return str(post_id)


@app.route('/uuid/<uuid:uuid>')
def get_uuid(uuid):
    return str(uuid)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
