import os
import shutil
#from mcbe_management import get_update
import get_update, exceptions
import urllib.request
import zipfile
import subprocess
import time
import hashlib

def check_installed():#インストール済みか判別
    """サーバーがインストール済みか判別"""
    return os.path.isfile("/var/games/mcbe/lock/installed")

def server_download():#MCBE ServerをDLして解凍する
    """MCBE ServerをDLして解凍するよ"""
        
    os.makedirs("/tmp/mcbe_manegement", exist_ok=True)
    print("Downloading...")
    mc_url = get_update.get_update_url()
        #zipファイルの準備
    f = open("/tmp/mcbe_manegement/server.zip", "w")
    f.write("")
    f.close
    urllib.request.urlretrieve(mc_url,"/tmp/mcbe_manegement/server.zip")#サーバーをDLしてzipを保存
    print("Extracting")
    with zipfile.ZipFile("/tmp/mcbe_manegement/server.zip", "r") as f:
        f.extractall("/tmp/mcbe_manegement/server")


def check_server_started():
    """サーバーが起動しているか判別するよ"""
    return os.path.isfile("/var/games/mcbe/lock/started")

def excute_inside_server(input):
    """Minecraft Server内でコマンドを実行して、その実行結果を取得する"""
    #サーバーが起動しているか確認
    if check_server_started() == False:
        raise exceptions.Server_is_not_running

    #output.txtの行数を取得する
    before_output_line = int(subprocess.check_output(["wc", "-l", "/var/games/mcbe/server/output.txt"]).decode().split()[0])
    #output.txtのハッシュ値の取得
    with open("/var/games/mcbe/server/output.txt","rb") as file:
        fileData = file.read()
        before_md5 = hashlib.md5(fileData).hexdigest()

    
    #screen内でcommandの実行
    args = (f"screen -S mcbe_server -X stuff '{input} \n'")
    result = subprocess.run(args, shell=True)

    #output.txtのハッシュ値が更新されるまで待つ(timeoutは5s)(1sごとに)
    for i in range(5):

        with open("/var/games/mcbe/server/output.txt","rb") as file:
            time.sleep(1)
            fileData = file.read()
            after_md5 = hashlib.md5(fileData).hexdigest()
            if after_md5 == before_md5:
                break
    #処理後のoutput.txtの行数を取得
    #after_output_line = int(subprocess.check_output(["wc", "l", "/var/games/mcbe/output.txt"]).decode().split()[0])

    #取得しないといけない行数を取得(後ろから)
    #get_line = after_output_line - before_output_line

    #データを取得
    output_file =  open("/var/games/mcbe/server/output.txt","rt")
    output = ""
    line_num = 1
    for line in output_file:
        if line_num > before_output_line:
            output += f"{line}\n"
        line_num += 1

    return output

print(excute_inside_server(input()))    



