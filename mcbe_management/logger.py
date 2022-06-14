from logging import getLogger, StreamHandler, FileHandler, Formatter, ERROR, INFO
from datetime import datetime
import os
#log用のディレクトリの生成
os.makedirs("/var/log/mcbe_management", exist_ok=True)
#loggerの生成
logger = getLogger("mcbe")

#Logのフォーマットの設定
handler_format = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#StreamHandlerの設定
stream_handler = StreamHandler()
#StreamHandlerはError以上を出力する
stream_handler.setLevel(ERROR)
#Formatを登録する
stream_handler.setFormatter(handler_format)

#FileHandlerの設定
file_handler = FileHandler('/var/log/mcbe_management/{:%Y-%m-%d}.log'.format(datetime.now()))
#Info以上を出力する
file_handler.setLevel(INFO)
#Formatを登録する
file_handler.setFormatter(handler_format)

#handlerをセット
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

#loggerのテスト
if __name__ == "__main__":
    logger.critical("critical test")
    logger.error("error_test")
    logger.info("info_test")
    logger.debug("debug_error")
