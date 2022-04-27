import subprocess
import os
import exceptions
#TODO screen がすでに存在していた時の処理
#TODO2 標準エラー出力についての設定
#minecraft serverが正常に起動したか確かめる(output.txtからserver startedが出力されて、3秒いないにcrashが表示されないかどうか)


def start(option):
    
    #最低限必要なファイルが存在しているか確認
    #bedrock_server,server.properties,worldsフォルダ
    bedrock = os.path.isfile("./server/bedrock_server")
    properties_file = os.path.isfile("./server/bedrock_server")
    worlds_dir = os.path.isdir("./server/worlds")
    if not option == "force":
        if bedrock == False or properties_file == False or worlds_dir == False:

            raise exceptions.Required_file_does_not_exist()#存在しなかったらエラー
    
    #screenがすでに存在しているか確かめる
    screen_test = subprocess.run(["screen","-ls"], encoding="utf-8", stdout=subprocess.PIPE)
    if not option == "force":
        screen_exist = "There are" in screen_test.stdout
        if screen_exist == True:
            raise exceptions.screen_already_exists()#screenがすでに存在してたらエラー



    #screen の準備
    server_dir = os.path.abspath("./server/")
    args = ["screen", "-dmS", "mcbe_server"]
    subprocess.check_output(args, cwd=server_dir)#サーバー実行用のscreenを立ち上げる

    #screen上でサーバーを起動させる
    
    args = (r"screen -S mcbe_server -X stuff 'LD_LIBRARY_PATH=. ./bedrock_server > output.txt \n'")
    result = subprocess.run(args, cwd=server_dir, shell=True)


    #bedrock serverのコンソール上でServer startedが表示されているか確認
    f = open("./server/output.txt", "r")
    for i in range(11):
        console = f.read()
        console_out = "start" in console
        if console_out == True:
            break
        elif i == 10:
            f.close
            raise exceptions.server_timeout()

    f.close
    return "Server Started!"
