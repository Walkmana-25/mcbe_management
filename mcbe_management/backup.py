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
    backup_dir = f"/var/games/mcbe/backup/backup_{today}-{now}"
    logger.debug(f"backup_dir:{backup_dir}")

    #backupが存在するか確かめる
    files = []
    backup_exist = True 
    os.makedirs("/var/games/mcbe/backup/", exist_ok=True)
    files = os.listdir("/var/games/mcbe/backup/")

    logger.debug(f"backup_exist:{backup_exist}")
    logger.debug(f"files:{files}")    

    #backupを実行する
    if files != []:
        complete_backup = []
        for i in files:
            complete_backup.append(i.replace("backup_", "")) 

        logger.debug(f"complete_backup:{complete_backup}")

        #並び替えて、0番目のフォルダーを--link-destにする
        complete_backup.sort()

        #backupを実行する
        logger.info(f"Create backup:{backup_dir}")
        logger.info(f"Link dest:/var/games/mcbe/backup/backup_{complete_backup[0]}/")
        args = [
            "rsync",
            "-a",
            f"--link-dest=/var/games/mcbe/backup/backup_{complete_backup[0]}/",
            "/var/games/mcbe/server/",
            f"{backup_dir}/"
        ]
        rsync = subprocess.run(args=args, capture_output=True)
        #rsyncが成功したか確かめる
        if rsync.returncode != 0:
            raise exceptions.backup_failed(
                error_code=rsync.returncode,
                excuted_command=rsync.args,
                stderr=rsync.stderr
            )
        logger.info("Backup Completed")
        

    else:
        logger.info("Starting backup")
        logger.info(f"backup directory:{backup_dir}")


        logger.debug("Create directory /var/games/mcbe/backup")
        logger.info(f"Create backup:{backup_dir}")

        args = ["rsync", "-a", "/var/games/mcbe/server/", f"{backup_dir}/"]
        rsync = subprocess.run(args=args, capture_output=True)
        #rsyncが成功したかしていないか確かめる
        if rsync.returncode != 0:
            raise exceptions.backup_failed(
                error_code= rsync.returncode,
                excuted_command=rsync.args,
                stderr=rsync.stderr
            )            
        logger.info("Backup Completed")

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