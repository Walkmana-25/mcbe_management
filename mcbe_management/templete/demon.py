from mcbe_management import exceptions, server_power, lib
import sys
import json
import os
import pkgutil

#初期確認を行う
#serverがインストールされているか確認
if lib.check_installed() == False:
    print("Server is not installed. Please run 'mcbe install'.", file=sys.stderr)
    sys.exit(1)

#/etc/mcbe_management.jsonと/var/games/mcbe/script.jsonが存在するか確認 
#存在しなかったらコピーする
exist_config = os.path.exits("/etc/mcbe_management.json")
exsit_script = os.path.exists("/var/games/mcbe/script.json")
if exist_config == false:
    with open("/etc/mcbe_management.json", "x") as f:
        f.write(pkgutil.get_data("mcbe_management", "templete/mcbe_management.json"))
if exist_script == false:
    with open("/var/games/mcbe/script.json", "x") as f:
        f.write(pkgutil.get_data("mcbe_management", "templete/script.json"))


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
if auto_backup["enable"] == True:
    #auto_backupの辞書を変数に変換する
    backup_week = auto_backup["week"]
    backup_hour = auto_backup["hour"]
    backup_minute = auto_backup["min"]

    #weekを数字に変換する
    backup_week = lib.week_to_cron(backup_week)
    #hourを数字に変換する\
    backup_hour = lib.hour_to_cron(backup_hour)

if auto_restart["enable"] == True:
    #auto_backupの辞書を変数に変換する
    restart_week = auto_restart["week"]
    restart_hour = auto_restart["hour"]
    restart_minute = auto_restart["min"]

    #weekを数字に変換する
    restart_week = lib.week_to_cron(backup_week)
    #hourを数字に変換する\
    restart_hour = lib.hour_to_cron(backup_hour)
