import subprocess
from mcbe_management import lib, exceptions, server_power, log
import datetime
import time
import time
import os
import shutil
import sys
from logging import getLogger


def backup():
    logger = getLogger("mcbe").getChild("backup")


def restore():
    logger = getLogger("mcbe").getChild("backup")



if __name__ == "__main__":
    command = input("Enter Function")
    if command == "backup":
        backup()
    elif command == "restore":
        restore()
    else:
        print("error")
        sys.exit(1)