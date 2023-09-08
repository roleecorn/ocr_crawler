from flask import Flask, render_template, jsonify, url_for, request
import flask
import time
import yaml
from classversion import ocr_crawler
import threading
from pathlib import Path

craw: ocr_crawler = None
app = Flask(__name__)
home = Path.cwd()


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


@app.route('/yml', methods=['GET'])
def yml():
    return render_template('yml.html')


@app.route('/get_yml', methods=['GET'])
def get_yml():
    shop = request.args.get('shop')
    with open(home / 'cite_envs' / f"{shop}.yml", 'r') as file:
        cite_config = yaml.safe_load(file)
    print(shop)
    # 其他的代码...
    return jsonify(cite_config)


@app.route('/save_yml/<shop>', methods=['POST'])
def save_yml(shop):
    data_to_save = request.json

    # 检查data_to_save是否为有效数据
    if not data_to_save:
        return jsonify({"message": "Invalid data"}), 400

    # 写入文件
    with open(home / 'cite_envs' / f"{shop}.yml", 'w') as file:
        yaml.safe_dump(data_to_save, file)

    return jsonify({"message": "Data saved successfully"}), 200


if __name__ == '__main__':
    app.run(debug=False)
