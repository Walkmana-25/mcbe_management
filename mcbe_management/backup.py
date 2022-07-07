from itertools import count
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
    logger.info("Starting Restore")

    #serverがインストールされているかどうか確かめる
    if lib.check_installed() == False:
        raise exceptions.server_is_not_installed()

    #Serverが停止しているか確かめる
    if lib.check_server_started() == True:
        raise exceptions.server_is_started()

    #backupが存在するか確かめる
    if os.path.exists("/var/games/mcbe/backup") == False:
        raise exceptions.backup_not_found()

    files = os.listdir("/var/games/mcbe/backup/")
    if files == []:
        raise exceptions.backup_not_found()

    #directoryを日付と時間に分ける
    backup_directory = {}
    backup_directory_date = []
    for i in files:
         #backup_を除去する
        i = i.replace("backup_", "")
        #yy-mm-dd-hh-mm-ssをyy/mm/dd-hh:mm:ssの形式に変換する
        #はじめの２つの-を/に変える
        i = i.replace("-", "/", 2)
        #すべての-を:に変える
        i = i.replace("-", ":")
        #1番はじめの:を-に変える
        i = i.replace(":", "-", 1)

        backup_tmp = i.split("-")
        logger.debug(f"backup:{backup_tmp}")

        #日付がdictionaryのkeyに存在するか確かめる
        try:
            backup_directory[backup_tmp[0]]
        except KeyError:
            backup_directory[backup_tmp[0]] = []
        
        backup_directory_date.append(backup_tmp[0])

        backup_directory[backup_tmp[0]].append(backup_tmp[1])

    #リストの中の重複を削除
    backup_directory_date = set(backup_directory_date)
    backup_directory_date = list(backup_directory_date)

    logger.debug(f"backup_directory:{backup_directory}")
    logger.debug(f"backup_directory_date:{backup_directory_date}")

    #復元対象の日付を表示する
    print("Please select the restore target in list.")
    for i in range(29):
        print("-", end="")
    print("-")
    for i in backup_directory_date:
        print(str(backup_directory_date))
    for i in range(29):
        print("-", end="")
    print("-")

    #ユーザーの入力がリストに含まれているか確認する
    while True:
        user_input_date = input("Date:")
        user_input_date = str(user_input_date)
        if user_input_date in backup_directory_date:
            break
        else:
            print(f"{user_input_date} is not in list.")
    
    #復元対象の時間を表示する
    print("Please select the restore target in list.")
    for i in range(29):
        print("-", end="")
    print("-")
    for i in backup_directory[user_input_date]:
        print(i)
    for i in range(29):
        print("-", end="")
    print("-")
    
    #ユーザーの入力がリストに含まれているか確認する
    while True:
        user_input_time = input("Time:")
        user_input_time = str(user_input_time)
        if user_input_time in backup_directory[user_input_date]:
            break
        else:
            print(f"{user_input_date} is not in list.")
            
    #リストアを実行するか聞く
    print(f"Restore to data as of {user_input_date} {user_input_time}")
    print("Format:yyyy:mm:dd:hh:mm:ss")
    print("Are you sure? y or n")
    logger.info(f"Try to restore:{user_input_date} {user_input_time}")

    #y or nを判定する
    while True:
        user_input_agree = str(input())
        if user_input_agree == "y":
            logger.info("User agrred to restore")
            break
        elif user_input_agree == "n":
            logger.info("User disagreed to restore")
            exit()
        else:
            print(f"Please enter y or n")

    #user_input_dateとuser_input_timeからディレクトリを作る
    restore_dir = f"/var/games/mcbe/backup/backup_{user_input_date}-{user_input_time}"    
    restore_dir = restore_dir.replace("/", "-")
    restore_dir = restore_dir.replace(":", "-")
    restore_dir = restore_dir.replace("-","/", 5)
    restore_dir += "/"

    logger.info(f"Restore From:{restore_dir}")

    backup()
    
    logger.debug("Delete:/var/games/mcbe/server")
    shutil.rmtree("/var/games/mcbe/server/")

    logger.debug("Copy Server")
    shutil.copytree(restore_dir, "/var/games/mcbe/server/")

    #完了
    logger.info("Restore Complete")
    



if __name__ == "__main__":
    command = input("Enter Function")
    if command == "backup":
        backup()
    elif command == "restore":
        restore()
    else:
        print("error")
        sys.exit(1)