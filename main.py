import FileFunctions
from GettingInfo import GettingInfo
from UnlockingInfo import UnlockingInfo
from UpdatingInfo import UpdatingInfo

try:
    current_dinos, needed_dinos = FileFunctions.create_dino_info()

    getting_info = GettingInfo(current_dinos, needed_dinos)
    current_dinos, needed_dinos = getting_info.get_all_dino_info()

    unlocking_info = UnlockingInfo(current_dinos, needed_dinos)
    current_dinos, needed_dinos = unlocking_info.get_all_dino_info()

    updating_info = UpdatingInfo(current_dinos, needed_dinos)
    current_dinos, needed_dinos = updating_info.get_all_dino_info()

    FileFunctions.save_dino_info(current_dinos, needed_dinos)
except:
    FileFunctions.save_dino_info(current_dinos, needed_dinos)