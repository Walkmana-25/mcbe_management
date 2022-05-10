import subprocess
import lib, exceptions
import datetime
import time
import os
import shutil



def backup():
    #サーバーが起動しているか判別する
    #サーバーが起動している時の処理
    if os.path.isfile("/var/games/mcbe/lock/started") == False:
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
    today = "{0:%Y-%m-%d}".format(dt)
    now = "{0:%H-%M-%S}".format(dt)

    #バックアップパスを設定
    backup_dir = f"/var/games/mcbe/backup/{today}/"
    backup_base_dir = f"{backup_dir}/backup-base/"
    backup_file = f"{backup_dir}{today}.tar.gz"
    backup_now_dir = f"{backup_dir}{now}/"



    #本日分のbackup-baseが存在するか確認し、あればbackup-baseを作成する
    #同時に、server.properties, allowlist.json, permissions.jsonもコピーする
    if os.path.exists(backup_base_dir) == False:
        os.makedirs(backup_base_dir)
        args = ["rsync", "-a", "/var/games/mcbe/server/worlds/", f"{backup_base_dir}"]
        subprocess.check_output(args)
        shutil.copy2("/var/games/mcbe/server/server.properties", f"{backup_dir}server.properties")
        shutil.copy2("/var/games/mcbe/server/allowlist.json", f"{backup_dir}allowlist.json")
        shutil.copy2("/var/games/mcbe/server/permissions.json", f"{backup_dir}permissions.json")

    #rsyncによる差分バックアップを実行する
    args = ["rsync", "-a", f"--link-dest={backup_base_dir}", "/var/games/mcbe/server/worlds/", f'{backup_now_dir}']
    result = subprocess.check_output(args)

def restore():
    #バックアップ対象の日付を選択するためにlistを取得して、その内容を出力する
    files = os.listdir("/var/games/mcbe/backup")
    print("Please select the restore target (date)")
    print("---------------------")
    for f in files:
        print(f)
    print("---------------------")

    #ユーザーの入力がリストに含まれているか確認する
    while True:
        user_input = str(input())
        if user_input in files:
            break
    


    


