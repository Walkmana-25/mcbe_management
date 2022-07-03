import subprocess
from mcbe_management import lib, exceptions, server_power, log
import datetime
import time
import os
import shutil
import sys
from logging import getLogger





def backup():#Loggerの設定
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

    #バックアップパスを設定
    backup_dir = f"/var/games/mcbe/backup/{today}/"
    backup_base_dir = f"{backup_dir}/backup-base/"
    backup_now_dir = f"{backup_dir}{now}/"
    logger.debug(f"backup_dir:{backup_dir}")
    logger.debug(f"backup_base_dir:{backup_base_dir}")



    #本日分のbackup-baseが存在するか確認し、あればbackup-baseを作成する
    #同時に、server.properties, allowlist.json, permissions.jsonもコピーする
    if os.path.exists(backup_base_dir) == False:
        logger.info(f"Create backup base:{backup_base_dir}")
        os.makedirs(backup_base_dir)
        args = ["rsync", "-a", "/var/games/mcbe/server/worlds/", f"{backup_base_dir}"]
        subprocess.check_output(args)
        shutil.copy2("/var/games/mcbe/server/server.properties", f"{backup_dir}server.properties")
        shutil.copy2("/var/games/mcbe/server/allowlist.json", f"{backup_dir}allowlist.json")
        shutil.copy2("/var/games/mcbe/server/permissions.json", f"{backup_dir}permissions.json")
        logger.debug("Create backup base:Done")

    #rsyncによる差分バックアップを実行する
    logger.info(f"Create backup:{backup_now_dir}")
    args = ["rsync", "-a", f"--link-dest={backup_base_dir}", "/var/games/mcbe/server/worlds/", f'{backup_now_dir}']
    result = subprocess.check_output(args)

def restore():
    #Loggerの設定
    logger = getLogger("mcbe").getChild("restore")
    #バックアップ対象の日付を選択するためにlistを取得して、その内容を出力する
    files = os.listdir("/var/games/mcbe/backup")
    print("Please select the restore target in list")
    print("---------------------")
    for f in files:
        print(f)
    print("---------------------")

    #ユーザーの入力がリストに含まれているか確認する
    while True:
        user_input_date = str(input())
        if user_input_date in files:
            break
        else:
            print(f"{user_input_date} is not in list")

    #バックアップ対象の時間を選択するためにlistを取得して、その内容を出力する
    files = os.listdir(f"/var/games/mcbe/backup/{user_input_date}")
    files_dir = [f for f in files if os.path.isdir(os.path.join(f"/var/games/mcbe/backup/{user_input_date}", f))]
    print("Please select the restore target in list")
    print("---------------------")
    for f in files_dir:
        if not f == "backup-base":
           print(f)
    print("---------------------")

    #ユーザーの入力がリストに含まれているか確認する
    while True:
        user_input_time = str(input())
        if user_input_time in files_dir:
            break
        else:
            print(f"{user_input_time} is not in list")
    
    #リストアを実行するか聞く
    print(f"Restore to data as of {user_input_date} {user_input_time}")
    print("Format:yyyy:mm:dd:hh:mm:ss")
    print("Are you sure? y or n")

    #y or nを判定する
    while True:
        user_input_agree = str(input())
        if user_input_agree == "y":
            break
        elif user_input_agree == "n":
            exit()
        else:
            print(f"Please enter y or n")
    
    #worldsの中身をバックアップのやつに入れ替える
    #サーバーが起動しているか確認する
    if os.path.isfile("/var/games/mcbe/lock/started") == True:
        server_power.stop()
        print("Server stopped")

    print("Worlds Data backup...")
    backup()#念のためのバックアップ実行

    #コピーソースの指定(二次元配列)
    restore_source_dir = f"/var/games/mcbe/backup/{user_input_date}/{user_input_time}/"
    copy_file_source = [
        [
            f"/var/games/mcbe/backup/{user_input_date}/allowlist.json",
            "allowlist.json"
        ],
        [
            f"/var/games/mcbe/backup/{user_input_date}/permissions.json",
            "permission.json"
        ],
        [
            f"/var/games/mcbe/backup/{user_input_date}/server.properties",
            "server.properties"
        ]
    ]

    #削除するフォルダー、ファイルの指定
    delete_dir = "/var/games/mcbe/server/worlds/"
    delete_files = [
        "/var/games/mcbe/server/allowlist.json",
        "/var/games/mcbe/server/permissions.json",
        "/var/games/mcbe/server/server.properties"
    ]

    #ファイルの削除の実行
    #delete_filesの中のファイルの削除
    for file in delete_files:
        try:
            os.remove(file)
        except FileNotFoundError:
            print(f"{file} is not found. Cannot Delete.", file=sys.stderr)
        
    #フォルダーの削除
    shutil.rmtree(delete_dir)

    #ファイルコピーの実行
    for i in copy_file_source:
        shutil.copy2(i[0], f"/var/games/mcbe/server/{i[1]}")

    shutil.copytree(restore_source_dir, "/var/games/mcbe/worlds")

    #完了!!!
    print("Restore Completed!!")

if __name__ == "__main__":
    print("Enter Function")
    input = input()
    if input == "backup":
        backup()
    elif input == "restore":
        restore()
    else:
        print("error")
        sys.exit(1)
    
    