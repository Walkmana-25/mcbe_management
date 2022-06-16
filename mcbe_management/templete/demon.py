from mcbe_management import exceptions, server_power, lib, update, log
import sys
import json
import os
import pkgutil
import re
import time
from logging import getLogger, StreamHandler, DEBUG, INFO
#loggerの設定
logger = getLogger("mcbe").getChild("daemon")
#daemonは、stream handlerでinfoも出力する
stream_handler = log.stream_handler
if log.debug_mode == True:
    stream_handler.setLevel(DEBUG)
else:
    stream_handler.setLevel(INFO)
logger.addHandler(stream_handler)

#初期確認を行う
#serverがインストールされているか確認
if lib.check_installed() == False:
    raise exceptions.server_is_not_installed()

#すでにserverが起動しているかどうか確認
if lib.check_server_started() == True:
    print("Server is already started")
    sys.exit(0)

#/etc/mcbe_management.jsonと/var/games/mcbe/script.jsonが存在するか確認 
#存在しなかったらコピーする
exist_config = os.path.exists("/etc/mcbe_management.json")
exist_script = os.path.exists("/var/games/mcbe/script.json")
if exist_config == False:
    with open("/etc/mcbe_management.json", "x") as f:
        f.write(pkgutil.get_data("mcbe_management", "templete/mcbe_management.json").decode("utf-8"))
if exist_script == False:
    with open("/var/games/mcbe/script.json", "x") as f:
        f.write(pkgutil.get_data("mcbe_management", "templete/script.json").decode("utf-8"))


#jsonを読み込んで変数に格納する
with open("/etc/mcbe_management.json", "r") as load_config_json:
    text = load_config_json.read()
re_text = re.sub(r'/\*[\s\S]*?\*/|//.*', '', text)
config = json.loads(re_text)

auto_update = config["auto_update"]
auto_fix = config["auto_fix"]
auto_backup = config["auto_backup"]
auto_restart = config["auto_restart"]
discord_bot = config["discord_bot"]

# auto_updateの設定
if auto_update == True:
    update.server_update(manual=False)

#jsonのauto_updateの値を読み取って、cronに書き込む
if auto_backup["enable"] == True:
    #auto_backupの辞書を変数に変換する
    backup_week = auto_backup["week"]
    backup_hour = auto_backup["hour"]
    backup_minute = auto_backup["min"]

    #weekを数字に変換する
    try:
        backup_week = lib.week_to_cron(backup_week)
    except exceptions.config_is_wrong:
        print("Error. week in auto_backup is wrong. Please edit /etc/mcbe_management", file=sys.stderr)
        sys.exit(1)
    
    #hourを数字に変換する
    try:
        backup_hour = lib.hour_to_cron(backup_hour)
    except exceptions.config_is_wrong:
        print("Error. hour in auto_backup is wrong. Please edit /etc/mcbe_management", file=sys.stderr) 
        sys.exit(1) 

if auto_restart["enable"] == True:
    #auto_backupの辞書を変数に変換する
    restart_week = auto_restart["week"]
    restart_hour = auto_restart["hour"]
    restart_minute = auto_restart["min"]

    #weekを数字に変換する
    try:
        restart_week = lib.week_to_cron(restart_week)
    except exceptions.config_is_wrong:
        print("Error. week in auto_restart is wrong. Please edit /etc/mcbe_management", file=sys.stderr)    
        sys.exit(1)
    #hourを数字に変換する
    try:
        restart_hour = lib.hour_to_cron(restart_hour)
    except exceptions.config_is_wrong:
        print("Error. hour in auto_restart is wrong. Please edit /etc/mcbe_management", file=sys.stderr)    
        sys.exit(1)

#crontabの書き込み
if auto_backup["enable"] == True or auto_restart["enable"] == True:
    #書き込む内容の準備
    cron = "#/etc/cron.d/mcbe: crontab entries for the mcbe_management\nSHELL=/bin/bash\nPATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin\nMAILTO=root\nHOME=/\n"
    #auto_backupの書き込みをする準備
    if auto_backup["enable"] == True:
        cron += f"{backup_minute} {backup_hour} * * {backup_week} root mcbe backup\n"
    #auto_restartの書き込みをする準備
    if auto_restart["enable"] == True:
        cron += f"{restart_minute} {restart_hour} * * {restart_week} root mcbe restart\n"

    #現在のcronを読み込む
    #ファイルが存在しているか確認する
    if os.path.exists("/etc/cron.d/mcbe") == False:
        with open("/etc/cron.d/mcbe", "w") as f:
            f.write(cron)
    else:
        with open("/etc/cron.d/mcbe", "r") as f:
            cron_before = f.read()

        #ファイルの内容を比較する
        if cron_before != cron:
            with open("/etc/cron.d/mcbe", "w") as f:
                f.write(cron)

#auto_backupとauto_restartが両方falseのときに、削除する
if auto_backup["enable"] == False and auto_restart["enable"] == False and os.path.exists("/etc/cron.d/mcbe") == True:
     os.remove("/etc/cron.d/mcbe")

#初期確認終わり
#serverを起動する
server_power.start()

#demonが起動していることを示すファイルを作る
with open("/var/games/mcbe/lock/demon_started", "w") as f:
    f.write("")
    
#常時処理ここから
#================================================================
while True:
    time.sleep(5)#5秒ごとに実行する
    with open("/var/games/mcbe/server/output.txt", "r") as f:
        data = f.read()
    if data in "crash" or data in "Crash":
        print("Server Crashed", file=sys.stderr)
        sys.exit(1)

    #/var/games/mcbe/lock/demon_stopが存在したらdemonを止める処理を追加
    if os.path.exists("/var/games/mcbe/lock/demon_stop") == True:
        os.remove("/var/games/mcbe/lock/demon_started")
        sys.exit()

#================================================================