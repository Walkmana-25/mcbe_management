import lib, exceptions
import datetime
import time
import os



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
    backup_dir = f"/var/games/mcbe/backup/{today}"
    backup_base_file = f"{backup_dir}/backup-base.tar.gz"
    backup_file = f"{backup_dir}/{today}.tar.gz"

    #tmpフォルダーの作成
    os.makedirs(f"/tmp/mcbe_manegement/backup/{today}/{now}")
    os.makedirs(f"/tmp/mcbe_manegement/backup/backupbase/{today}/{now}")
    

    


    


