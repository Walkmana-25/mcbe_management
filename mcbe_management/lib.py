import os
import shutil
#from mcbe_management import get_update
from mcbe_management import get_update, exceptions
import urllib.request
import zipfile
import subprocess
import time
import hashlib
from logging import getLogger
logger = getLogger("mcbe").getChild("lib")


def check_installed():#インストール済みか判別
    """サーバーがインストール済みか判別"""
    if os.path.isfile("/var/games/mcbe/lock/installed") == True:
        return True
    else:
        return False

def server_download(url=None):#MCBE ServerをDLして解凍する
    """MCBE ServerをDLして解凍するよ"""
    logger.info("Starting server_download")
    os.makedirs("/tmp/mcbe_manegement", exist_ok=True)
    print("Downloading...")
    if url == None:
        mc_url = get_update.get_update_url()
    else:
        mc_url = url
        #zipファイルの準備
    f = open("/tmp/mcbe_manegement/server.zip", "w")
    f.write("")
    f.close
    logger.debug(f"download from{mc_url}")
    urllib.request.urlretrieve(mc_url,"/tmp/mcbe_manegement/server.zip")#サーバーをDLしてzipを保存
    print("Extracting")
    with zipfile.ZipFile("/tmp/mcbe_manegement/server.zip", "r") as f:
        f.extractall("/tmp/mcbe_manegement/server")
    logger.info("server_download completed")
    return mc_url


def check_server_started():
    """サーバーが起動しているか判別するよ"""
    return os.path.isfile("/var/games/mcbe/lock/started")

def excute_inside_server(input):
    logger.info(f"starting excute_inside_server:input:{input}")
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
    logger.info(f"excute:{args}")
    #output.txtのハッシュ値が更新されるまで待つ(timeoutは5s)(1sごとに)
    for i in range(5):
        logger.debug(f"loop:{i}")
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
    logger.info(f"excute_inside_server completed")
    logger.info(f"output:{output}")
    return output

def week_to_cron(input_week):
    if type(input_week) is list == False:
        raise exceptions.variable_class_exception("week format error")

    cron_week = ""
    l = len(input_week)
    j = 1
    
    for i in input_week:
        if i == "Sunday":
            cron_week += "0"
        elif i == "Monday":
            cron_week += "1"
        elif i == "Tuesday":
            cron_week += "2"
        elif i == "Wednesday":
            cron_week += "3"
        elif i == "Thursday":
            cron_week += "4"
        elif i == "Friday":
            cron_week += "5"
        elif i == "Saturday":
            cron_week += "6"
        else:
            raise exceptions.config_is_wrong()

        if j != l:
            j += 1
            cron_week += ","
    #cron_weekが空白になったときにエラーを吐くようにする
    if cron_week == "":
        raise exceptions.config_is_wrong("week format error")

    return cron_week


def hour_to_cron(input_hour):
    if type(input_hour) is list == False:
        raise exceptions.variable_class_exception(("hour format error"))
    
    cron_hour = ""
    l = len(input_hour)
    j = 1

    for i in input_hour:
        try:
            k = int(i)
        except ValueError():
            raise exceptions.config_is_wrong("hour format error")
        if k >= 0 and k <= 24:
            pass
        else:
            raise exceptions.config_is_wrong("hour format error")
        cron_hour += i

        if j != l:
            j += 1
            cron_hour += ","

    #cron_hourが空白になったときにエラーが吐くようにする
    if cron_hour == "":
        raise exceptions.config_is_wrong("hour format error")

    return cron_hour

def url_to_version(url):
    url_list = url.split("/")
    #urlからversionがあるところを抜き出す
    r1= str(url_list[len(url_list) - 1])
    #-の以前を消す
    r2 = r1.split("-")
    r3 = str(r2[len(r2) - 1])
    #bedrock-serverとzipを削除する
    r4 = r3.replace("bedrock-server", "")
    r5 = r4.replace("zip", "")
    #末尾の.を削除する
    mc_version = r5.strip(".")
    
    return mc_version
