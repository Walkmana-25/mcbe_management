from mcbe_management import exceptions, server_power, lib, update, log
import sys
import json
import os
import pkgutil
import re
import time
from logging import getLogger, StreamHandler, DEBUG, INFO
from systemd import daemon
#loggerの設定
logger = getLogger("mcbe").getChild("daemon")

logger.info("Starting daemon.")
daemon.notify("STATUS=Starting...")

#初期確認を行う
#serverがインストールされているか確認
if lib.check_installed() == False:
    raise exceptions.server_is_not_installed()

#すでにserverが起動しているかどうか確認
if lib.check_server_started() == True:
    raise exceptions.server_is_started()

#/etc/mcbe_management.jsonと/var/games/mcbe/script.jsonが存在するか確認 
#存在しなかったらコピーする
exist_config = os.path.exists("/etc/mcbe_management.json")
logger.debug(f"/etc/mcbe_management.json exist:{exist_config}")
exist_script = os.path.exists("/var/games/mcbe/script.json")
logger.debug(f"/var/games/mcbe/script.json exist:{exist_script}")
if exist_config == False:
    logger.info("/etc/mcbe_management.json is not exsiting. start copying")
    with open("/etc/mcbe_management.json", "x") as f:
        f.write(pkgutil.get_data("mcbe_management", "templete/mcbe_management.json").decode("utf-8"))
if exist_script == False:
    logger.info("/var/games/mcbe/script.json is not exsiting. start copying")
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
logger.debug(f"auto_update:{auto_update}")
if auto_update == True:
    logger.info("Starting Auto Update")
    update.server_update(manual=False)

#jsonのauto_updateの値を読み取って、cronに書き込む
if auto_backup["enable"] == True:
    #auto_backupの辞書を変数に変換する
    backup_week = auto_backup["week"]
    backup_hour = auto_backup["hour"]
    backup_minute = auto_backup["min"]
    logger.debug("auto_backup:True")
    logger.debug(f"week{backup_week}")
    logger.debug(f"hour{backup_hour}")
    logger.debug(f"minute{backup_minute}")


    #weekを数字に変換する
    try:
        backup_week = lib.week_to_cron(backup_week)
    except exceptions.config_is_wrong:
        raise exceptions.config_is_wrong("Error. week in auto_backup is wrong. Please edit /etc/mcbe_management")
    logger.debug(f"backup_week:{backup_week}")
    
    #hourを数字に変換する
    try:
        backup_hour = lib.hour_to_cron(backup_hour)
    except exceptions.config_is_wrong:
        raise exceptions.config_is_wrong("Error. hour in auto_backup is wrong. Please edit /etc/mcbe_management")
    logger.debug(f"backup_hour:{backup_hour}")

if auto_restart["enable"] == True:
    #auto_backupの辞書を変数に変換する
    restart_week = auto_restart["week"]
    restart_hour = auto_restart["hour"]
    restart_minute = auto_restart["min"]
    logger.debug("Auto Restart:True")
    logger.debug(f"restart_week:{restart_week}")
    logger.debug(f"restart_hour:{restart_hour}")
    logger.debug(f"restart_minute:{restart_minute}")

    #weekを数字に変換する
    try:
        restart_week = lib.week_to_cron(restart_week)
    except exceptions.config_is_wrong:
        raise exceptions.config_is_wrong("Error. week in auto_restart is wrong. Please edit /etc/mcbe_management")
    logger.debug(f"restart_week:{restart_week}")    
    #hourを数字に変換する
    try:
        restart_hour = lib.hour_to_cron(restart_hour)
    except exceptions.config_is_wrong:
        raise exceptions.config_is_wrong("Error. hour in auto_restart is wrong. Please edit /etc/mcbe_management")
    logger.debug(f"restart_hour:{restart_hour}")

#crontabの書き込み
if auto_backup["enable"] == True or auto_restart["enable"] == True:
    #書き込む内容の準備
    cron = "#/etc/cron.d/mcbe: crontab entries for the mcbe_management\nSHELL=/bin/bash\nPATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin\nMAILTO=root\nHOME=/\n"
    #auto_backupの書き込みをする準備
    if auto_backup["enable"] == True:
        enable_auto_backup = auto_backup["enable"]
        cron += f"{backup_minute} {backup_hour} * * {backup_week} root mcbe backup\n"
    #auto_restartの書き込みをする準備
    if auto_restart["enable"] == True:
        enable_auto_restart = auto_restart["enable"]
        cron += f"{restart_minute} {restart_hour} * * {restart_week} root mcbe restart\n"

    logger.debug(cron)

    #現在のcronを読み込む
    #ファイルが存在しているか確認する
    if os.path.exists("/etc/cron.d/mcbe") == False:
        logger.info("Generate file for cron.")
        logger.info(f"Auto Backup:{enable_auto_backup}")
        logger.info(f"Auto Restart]{enable_auto_restart}")
        with open("/etc/cron.d/mcbe", "w") as f:
            f.write(cron)
    else:
        with open("/etc/cron.d/mcbe", "r") as f:
            cron_before = f.read()

        #ファイルの内容を比較する
        if cron_before != cron:
            logger.info("Config was updated. Updating file for cron.")
            logger.info(f"Auto Backup:{enable_auto_backup}")
            logger.info(f"Auto Restart:{enable_auto_restart}")
            with open("/etc/cron.d/mcbe", "w") as f:
                f.write(cron)

#auto_backupとauto_restartが両方falseのときに、削除する
if auto_backup["enable"] == False and auto_restart["enable"] == False and os.path.exists("/etc/cron.d/mcbe") == True:
     os.remove("/etc/cron.d/mcbe")
     logger.info("Config was updated. Updating file for cron.")
     logger.info(f"Auto Backup:False")
     logger.info(f"Auto Restart:False")

#初期確認終わり
#serverを起動する
server_power.start()

#demonが起動していることを示すファイルを作る
with open("/var/games/mcbe/lock/demon_started", "w") as f:
    f.write("")
    
#常時処理ここから
logger.info("Server Started.")
num = 0
daemon.notify("READY=1")
#================================================================
while True:
    logger.debug("Sleep 5s")
    time.sleep(5)#5秒ごとに実行する
    with open("/var/games/mcbe/server/output.txt", "r") as f:
        data = f.read()
    if "crash" in data or "Crash" in data:
        if auto_fix == True:
            logger.error("Bedrock Server Crashed.")
            logger.error("Trying Fix")
            server_power.auto_fix(num)
            num += 1
        else:
            logger.error("Bedrock Server Crashed.")
            server_power.stop(stop_demon=False)
            raise exceptions.server_crash
            
            


    #/var/games/mcbe/lock/demon_stopが存在したらdemonを止める処理を追加
    
    if os.path.exists("/var/games/mcbe/lock/demon_stop") == True:
        os.remove("/var/games/mcbe/lock/demon_started")
        logger.info("Stop Daemon.")
        sys.exit()

#================================================================