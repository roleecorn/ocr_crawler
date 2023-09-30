from flask import Blueprint, request, jsonify
import yaml
from datetime import datetime
from pathlib import Path
import util
home = Path.cwd()
ymlroute = Blueprint('ymlroute', __name__)
shops = [file.name for file in (
    home / 'cite_envs').iterdir() if file.is_file()]


@ymlroute.route('/get_yml', methods=['GET'])
def get_yml():
    global shops
    base_path = home / 'cite_envs'
    shop = util.remove_non_alphanumeric(request.args.get('shop'))
    shop += '.yml'
    fullpath = base_path / shop
    if base_path not in fullpath.parents:
        return jsonify({"message": "Not allowed"}), 400
    if shop not in shops:
        return jsonify({"message": "Invalid data"}), 400
    with open(fullpath, 'r') as file:
        cite_config = yaml.safe_load(file)

    # 其他的代码...
    return jsonify(cite_config)


@ymlroute.route('/save_yml/<shop>', methods=['POST'])
def save_yml(shop):
    global shops
    shop = util.remove_non_alphanumeric(shop)
    data_to_save = request.json

    # 检查data_to_save是否为有效数据
    if not data_to_save:
        return jsonify({"message": "Invalid data"}), 400

    base_path = home / 'cite_envs'
    shop = shop + '.yml'
    fullpath = base_path / shop
    if base_path not in fullpath.parents:
        return jsonify({"message": "Not allowed"}), 400
    if shop not in shops:
        return jsonify({"message": "Invalid data"}), 400
    data_to_save['lastupdate'] = str(datetime.now())
    # 写入文件
    with open(fullpath, 'w') as file:
        yaml.safe_dump(data_to_save, file)

    return jsonify({"message": "Data saved successfully"}), 200
