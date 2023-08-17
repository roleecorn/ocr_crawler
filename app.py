from flask import Flask, render_template, jsonify, redirect, url_for
import flask
import time
from classversion import ocr_crawler
import threading

craw: ocr_crawler = None
app = Flask(__name__)

def background_task(mode):
    global craw
    craw.new_driver()
    time.sleep(3)
    if mode == 'test':
        craw.test_start()
    elif mode == 'all':
        craw.all_start()
    craw.close()

@app.route('/')
def ishome():
    return render_template('home.html')

@app.route('/start_cite')
def start_cite():
    global craw
    input_value = flask.request.args.get('input', default='', type=str)
    # 進行你需要的其他操作...
    craw = ocr_crawler(input_value)
    # 返回要重定向到的URL
    return jsonify(redirect_url=url_for('index'))

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/run_test')
def run_test():
    thread = threading.Thread(target=background_task, args=('test',))
    thread.start()
    return jsonify(message="測試執行開始")

@app.route('/run_all')
def run_all():
    thread = threading.Thread(target=background_task, args=('all',))
    thread.start()
    return jsonify(message="完整執行開始")

if __name__ == '__main__':
    app.run(debug=False)
