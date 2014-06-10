from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/yolo/<hashtag>')
def show_hashtag(hashtag):
    # show the hashtag
    return 'HASHTAG: %s' % hashtag

if __name__ == '__main__':
    app.run(port=5001,debug=True)