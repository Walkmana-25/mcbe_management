
from msilib.schema import Error
import subprocess
import os
def start(self, option):
    args = ["screen", "-S", "mcbe_server"]
    subprocess.check_output(args)#サーバー実行用のscreenを立ち上げる
    
    #最低限必要なファイルが存在しているか確認
    #bedrock_server,server.properties,worldsフォルダ
    bedrock = os.path.isfile("../server/bedrock_server")
    properties_file = os.path.isfile("../server/bedrock_server")
    worlds_dir = os.path.isdir("../server/worlds")
    if bedrock == True or properties_file == True or worlds_dir == True:
        return "Can not start server. Required file does not exist"
        