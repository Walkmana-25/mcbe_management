from re import I
import subprocess
from mcbe_management import lib, exceptions, server_power, log
import datetime
import time
import time
import os
import shutil
import sys
from logging import getLogger


def backup():
    logger = getLogger("mcbe").getChild("backup")
    logger.info("Starting Backup")
    
    #worldsフォルダーが存在しているか確認する
    if os.path.exists("/var/games/mcbe/server/worlds") == False:
        raise exceptions.Required_file_does_not_exist("/var/games/mcbe/server/worlds")
    #サーバーが起動しているか判別する
    #サーバーが起動している時の処理
    if os.path.isfile("/var/games/mcbe/lock/started") == True:
        logger.debug("Server is running")
        save_hold = lib.excute_inside_server("save hold")#bedrock serverで、worldsフォルダーをlockする
        logger.debug(f"save hold:{save_hold}")
        #server側から、保存が終わったことを通知されるまで待つ(timeoutは5回)
        for i in range(6):
            logger.debug(f"loop:{i}")
            if i == 5:
                raise exceptions.server_timeout
            save_result = lib.excute_inside_server("save query")
            logger.debug(f"save query:{save_result}")
            if "saved" in save_result:
                break
            time.sleep(1)
    else:
        logger.debug("Server is not running.")

    #日時の取得
    dt = datetime.datetime.today()     
    today = "{0:%Y-%m-%d}".format(dt)
    now = "{0:%H-%M-%S}".format(dt)

    #backup passの設定
    backup_dir = f"/var/games/mcbe/backup/backup-{today}.{now}"
    logger.debug(f"backup_dir:{backup_dir}")

    #backupが存在するか確かめる
    files = []
    backup_exist = True 
    try:
        files = os.listdir("/var/games/mcbe/backup")
    except FileNotFoundError:
        backup_exist = False
    os.debug(f"backup_exist:{backup_exist}")

    #backupを実行する
    if backup_exist == True:
        pass

    else:
        logger.info("Starting backup")
        logger.info(f"backup directory:{backup_dir}")

        os.makedirs("/var/games/mcbe/backup")

        logger.debug("Create directory /var/games/mcbe/backup")

        args = ["rsync", "-a", "/var/games/mcbe/server/", f"{backup_dir}"]
        rsync = subprocess.run(args=args, capture_output=True)
        #rsyncが成功したかしていないか確かめる
        if args.returncode != 0:
            raise exceptions.backup_failed(
                error_code= rsync.returncode,
                excuted_command=rsync.args,
                stderr=rsync.stderr
            )            
        logger.info("Backup Completed")
        logger.info(backup_dir)

def restore():
    logger = getLogger("mcbe").getChild("backup")



if __name__ == "__main__":
    command = input("Enter Function")
    if command == "backup":
        backup()
    elif command == "restore":
        restore()
    else:
        print("error")
        sys.exit(1)