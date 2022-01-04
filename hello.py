from flask import Flask, request

app = Flask(__name__)   # __name__ : wjdwjr vkdlfrhk xpavmffltdmf ckwsmsep TMdla


@app.route('/index')
@app.route('/')     # route는 중첩할 수 있음
def hello_world():
    return 'Hello, World!'


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