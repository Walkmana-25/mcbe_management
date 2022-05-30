from mcbe_management import exceptions, server_power, lib
import sys
import json

#初期確認を行う
#serverがインストールされているか確認
if lib.check_installed() == False:
    print("Server is not installed. Please run 'mcbe install'.", file=sys.stderr)
    sys.exit(1)

#jsonを読み込んで変数に格納する
with open("/etc/mcbe_manegement.json", "r") as load_config_json:
    config = json.load(load_config_json)

auto_update = config["auto_update"]
auto_fix = config["auto_fix"]
auto_backup = config["auto_backup"]
auto_restart = config["auto_restart"]
discord_bot = config["discord_bot"]

#TODO auto_updateの設定

#jsonのauto_updateの値を読み取って、cronに書き込む
if auto_backup["enalbe"] == True:
    #auto_backupの辞書を変数に変換する
    week = auto_backup["week"]
    hour = auto_backup["hour"]
    minute = auto_backup["min"]


