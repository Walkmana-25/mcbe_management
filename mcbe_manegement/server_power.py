import subprocess
def start(self, option):
    args = ["screen", "-S", "mcbe_server"]
    subprocess.check_output(args)#サーバー実行用のscreenを立ち上げる
    
