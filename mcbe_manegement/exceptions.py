class Required_file_does_not_exist(Exception):
    """必要なファイルが存在していないときに発生させる例外クラス"""
    pass

class screen_already_exists(Exception):
    """screenがすでに存在しているときに発生させる例外クラス"""
    pass

class server_timeout(Exception):
    """サーバーが規定時間以内に起動しないときに発生する例外クラス"""
    pass