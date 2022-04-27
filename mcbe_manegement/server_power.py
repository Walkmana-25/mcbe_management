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

            raise exceptions.Required_file_does_not_exist()
    

    #screen の準備
    server_dir = os.path.abspath("./server/")
    args = ["screen", "-dmS", "mcbe_server"]
    subprocess.check_output(args, cwd=server_dir)#サーバー実行用のscreenを立ち上げる

    #screen上でサーバーを起動させる
    
    args = (r"screen -S mcbe_server -X stuff 'LD_LIBRARY_PATH=. ./bedrock_server >> output.txt \n'")
    result = subprocess.run(args, cwd=server_dir, shell=True)

    return 
