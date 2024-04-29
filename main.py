import FileFunctions
from GettingInfo import GettingInfo
from UpdatingInfo import UpdatingInfo

current_dinos, needed_dinos = FileFunctions.create_dino_info()

getting_info = GettingInfo(current_dinos, needed_dinos)
current_dinos, needed_dinos = getting_info.all_dino_info()

updating_info = UpdatingInfo(current_dinos, needed_dinos)
current_dinos, needed_dinos = updating_info.all_dino_info()

FileFunctions.save_dino_info(current_dinos, needed_dinos)