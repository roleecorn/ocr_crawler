from flask import Flask, render_template, jsonify, url_for, request
import flask
import time
import yaml
import re
from classversion import ocr_crawler
import threading
from pathlib import Path
from datetime import datetime
import util

craw: ocr_crawler = None
app = Flask(__name__, static_folder='src', static_url_path='/src')
home = Path.cwd()
shops = [file.name for file in (home / 'cite_envs').iterdir() if file.is_file()]


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


@app.route('/yml', methods=['GET'])
def yml():
    return render_template('yml.html')


@app.route('/get_yml', methods=['GET'])
def get_yml():
    global shops
    base_path = home / 'cite_envs'
    shop = request.args.get('shop') + '.yml'
    fullpath = base_path / shop
    if base_path not in fullpath.parents:
        raise Exception("not allowed")
    if shop not in shops:
        return jsonify({"message": "Invalid data"}), 400
    with open(fullpath, 'r') as file:
        cite_config = yaml.safe_load(file)
    print(shop)
    # 其他的代码...
    return jsonify(cite_config)


@app.route('/save_yml/<shop>', methods=['POST'])
def save_yml(shop):
    global shops
    data_to_save = request.json

    # 检查data_to_save是否为有效数据
    if not data_to_save:
        return jsonify({"message": "Invalid data"}), 400
    if shop+'.yml' not in shops:
        return jsonify({"message": "Invalid data"}), 400
    data_to_save['lastupdate'] = str(datetime.now())
    # 写入文件
    with open(home / 'cite_envs' / f"{shop}.yml", 'w') as file:
        yaml.safe_dump(data_to_save, file)

    return jsonify({"message": "Data saved successfully"}), 200


if __name__ == '__main__':
    app.run(debug=False)
