import os
import time
from datetime import datetime


class Logger:
    log_path = "logs/"
    log_name = "log"
    exist_time = 60 * 1  # time in seconds when log fill be deleted

    @staticmethod
    def Log(**kwargs):
        log_str = "Time: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for key in kwargs:
            log_str += " " + str(key) + ": " + str(kwargs[key])
        file = open(Logger.log_path + Logger.log_name + ".txt", 'a+')
        file.write(log_str + "\n")
        file.close()

    @staticmethod
    def delete_old():
        for f in os.listdir(Logger.log_path):
            f = os.path.join(Logger.log_path, f)
            if os.stat(f).st_mtime < time.time() - Logger.exist_time:
                if os.path.isfile(f):
                    os.remove(f)

