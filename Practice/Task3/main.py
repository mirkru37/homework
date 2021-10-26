from datetime import datetime
import LinkedList as List
import Menu
from Logger import Logger
from Observer import ObserverLogger

if __name__ == "__main__":
    Logger.log_name = "Session " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Logger.delete_old()
    list_ = List.LinkedList()
    list_observer = ObserverLogger()
    list_.registerObserver(list_observer)
    Menu.menu(Menu.do, list_)
