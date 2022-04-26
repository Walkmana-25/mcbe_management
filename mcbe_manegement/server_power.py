from ast import arg
from operator import truediv
import subprocess
import os


def start(option):
    
    #最低限必要なファイルが存在しているか確認
    #bedrock_server,server.properties,worldsフォルダ
    bedrock = os.path.isfile("./server/bedrock_server")
    properties_file = os.path.isfile("./server/bedrock_server")
    worlds_dir = os.path.isdir("./server/worlds")
    if not option == "force":
        if bedrock == False or properties_file == False or worlds_dir == False:
            return "Can not start server. Required file does not exist"
    
    #screen の準備
    server_dir = os.path.abspath("./server/")
    args = ["screen", "-dmS", "mcbe_server"]
    subprocess.check_output(args, cwd=server_dir)#サーバー実行用のscreenを立ち上げる

    #screen上でサーバーを起動させる
    
    args = (r"screen -S mcbe_server -X stuff 'LD_LIBRARY_PATH=. ./bedrock_server >> output.txt \n'")
    result = subprocess.run(args, cwd=server_dir, shell=True)

    return 
