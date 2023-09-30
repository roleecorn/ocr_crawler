from flask import Flask, render_template, jsonify, request
import flask
import time
import re
from classversion import ocr_crawler
import threading
from pathlib import Path
from views.ymls import ymlroute
import util

craw: ocr_crawler = None
app = Flask(__name__, static_folder='src', static_url_path='/src')
app.register_blueprint(ymlroute)
home = Path.cwd()
shops = [file.name for file in (
    home / 'cite_envs').iterdir() if file.is_file()]


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
    global craw, shops
    input_value = flask.request.args.get('input', default='', type=str)
    input_value = util.remove_non_alphanumeric(input_value)
    if not re.match("^[A-Za-z0-9]*$", input_value):
        return jsonify({"message": "Invalid data"}), 400
    if input_value + '.yml' not in shops:
        return jsonify({"message": "Invalid data"}), 400
    # 進行你需要的其他操作...
    craw = ocr_crawler(input_value)
    # 返回要重定向到的URL
    return jsonify(redirect_url='/src/index.html')


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
