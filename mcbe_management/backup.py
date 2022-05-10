import subprocess
import lib, exceptions
import datetime
import time
import os
import shutil



def backup():
    #サーバーが起動しているか判別する
    server_started = lib.check_server_started

    #サーバーが起動している時の処理
    if server_started == True:
        lib.excute_inside_server("save hold")#bedrock serverで、worldsフォルダーをlockする
        #server側から、保存が終わったことを通知されるまで待つ(timeoutは5回)
        for i in range(6):
            if i == 5:
                raise exceptions.server_timeout
            save_result = lib.excute_inside_server("save resume")
            if "saved" in save_result:
                break
            time.sleep(1)

    #日時の取得
    dt = datetime.datetime.today()
    today = f"{dt.year}{dt.month}{dt.day}"
    now = f"{dt.hour}{dt.minute}{dt.second}"

    #バックアップパスを設定
    backup_dir = f"/var/games/mcbe/backup/{today}/"
    backup_base_dir = f"{backup_dir}/backup-base/"
    backup_file = f"{backup_dir}{today}.tar.gz"
    backup_now_dir = f"{backup_dir}{now}/"



    #本日分のbackup-baseが存在するか確認し、あればbackup-baseを作成する
    #同時に、server.properties, allowlist.json, permissions.jsonもコピーする
    if os.path.exists(backup_base_dir) == True:
        os.makedirs(backup_base_dir)
        args = ["rsync", "-a", "/var/games/mcbe/server/worlds/", f"{backup_base_dir}"]
        subprocess.check_output(args)
        shutil.copy2("/var/games/mcbe/server/server.properties", f"{backup_dir}server.properties")
        shutil.copy2("/var/games/mcbe/server/allowlist.json", f"{backup_dir}allowlist.json")
        shutil.copy2("/var/games/mcbe/server/permissions.json", f"{backup_dir}permissions.json")

    #rsyncによる差分バックアップを実行する
    args = ["rsync", "-a", "--link-desk=", backup_base_dir, "/var/games/mcbe/server/", backup_now_dir]
    subprocess.check_output(args)

    




    
    


    


