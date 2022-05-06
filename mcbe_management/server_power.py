import subprocess
import os
import time
import exceptions, lib
#TODO screen がすでに存在していた時の処理
#TODO2 標準エラー出力についての設定
#minecraft serverが正常に起動したか確かめる(output.txtからserver startedが出力されて、3秒いないにcrashが表示されないかどうか)


def start(option):
    #最低限必要なファイルが存在しているか確認
    #bedrock_server,server.properties,worldsフォルダ
    bedrock = os.path.isfile("/var/games/mcbe/server/bedrock_server")
    properties_file = os.path.isfile("/var/games/mcbe/server/server.properties")
    if not option == "force":
        if bedrock == False or properties_file == False:

            raise exceptions.Required_file_does_not_exist()#存在しなかったらエラー
    
    #サーバーがすでに起動しているか確かめる
    
    if lib.check_server_started == True:
        raise exceptions.screen_already_exists()


    #screen の準備
    server_dir = "/var/games/mcbe/server/"
    args = ["screen", "-dmS", "mcbe_server"]
    subprocess.check_output(args, cwd=server_dir)#サーバー実行用のscreenを立ち上げる

    #screen上でサーバーを起動させる
    
    args = (r"screen -S mcbe_server -X stuff 'LD_LIBRARY_PATH=. ./bedrock_server > output.txt \n'")
    result = subprocess.run(args, cwd=server_dir, shell=True)


    #bedrock serverのコンソール上でServer startedが表示されているか確認
    f = open("/var/games/mcbe/server/output.txt", "r")
    for i in range(11):
        console = f.read()
        console_out = "start" in console
        if console_out == True:
            break
        elif i == 10:
            f.close
            raise exceptions.server_timeout()
        time.sleep(1)

    f.close
    #server startしていることを示すlockファイルを生成する
    f = open("/var/games/mcbe/server/lock/started", "w")
    f.write("")
    f.close()




    return "Server Started!"

def stop():
    #サーバーが起動しているか確かめる
    if lib.check_server_started() == False:
        return "Server is not running"
    
    #サーバー停止信号を送る
    args = (r"screen -S mcbe_server -X stuff 'stop \n'")
    result = subprocess.run(args, shell=True)

    #bedrock serverのコンソール上でQuit correctlyが表示されているか確認
    f = open("/var/games/mcbe/server/output.txt", "r")
    while True:
        console = f.read()
        console_out = "Quit correctly" in console
        if console_out == True:
            break
        time.sleep(1)
    f.close

    #screenのセッションを終了する
    args = (r"screen -S mcbe_server -X stuff 'exit \n'")
    result = subprocess.run(args, shell=True)

    #lockファイルの削除
    os.remove("/var/games/mcbe/server/lock/started")

    
    return "Server Stoped"

