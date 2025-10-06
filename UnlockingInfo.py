import os
from Dino import Dino
from HistoryPlotting import HistoryPlotting
import FileFunctions

class UnlockingInfo:
    """
    A class in charge of marking dinosaurs as unlocked and removing them and their parents from the database if no longer needed
    ...

    Attributes
    ----------
    current_dinos : dict[str : Dino]
        A current collection of dinosaur names mapped to their corresponding Dino objects
    needed_dinos : set[str]
        A set of names of dinosaurs that need to be unlocked
    """
    
    def __init__(self, c_dinos: dict[str: Dino], n_dinos: set[str]) -> None:
        """
        Initializes class variables and runs the user input process

        Parameters
        ----------
        c_dinos : dict[str : Dino]
            A current collection of dinosaur names mapped to their corresponding Dino objects
        n_dinos : set[str]
            A set of names of dinosaurs that need to be unlocked
        history : HistoryPlotting
            A class instantiation to keep track of amount history
        """
        self.current_dinos = c_dinos
        self.needed_dinos = n_dinos
        self.history = HistoryPlotting()

        self.ask_for_unlocked()

    def ask_for_unlocked(self) -> None:
        """
        Prompts the user to input dinos that have been unlocked and starts the removal process
        """
        while True:
            wanted_input = input('What dinosaur have you unlocked? (Type \'quit\' to quit): ')
            if (wanted_input == 'quit'):
                break
            print()
            self.clear_dino(wanted_input)
            self.needed_dinos.remove(wanted_input)
            os.system('cls')

    def clear_dino(self, unlocked_dino: str) -> None:
        """
        Takes the name of a recently unlocked dinosaur and clears it from the database if it is no longer used for any other dinosaur.
        This process is then recursively repeated with any dinos that are part of the first dinosaur's tree

        Parameters
        ----------
        unlocked_dino : str
            The name of the recently unlocked dino
        """
        has_other_child = False
        for dino_name in self.current_dinos:
            dino = self.current_dinos[dino_name]
            if dino.is_hybrid():
                if unlocked_dino in dino.get_parents():
                    has_other_child = True
        
        if not has_other_child:
            self.history.archive_dino(unlocked_dino)
            first = None
            if self.current_dinos[unlocked_dino].is_hybrid():
                first, second = self.current_dinos[unlocked_dino].get_parents()

            self.current_dinos.pop(unlocked_dino)
            if first:
                self.clear_dino(first)
                self.clear_dino(second)

    def get_all_dino_info(self) -> tuple[dict[str: Dino], set[str]]:
        """
        A getter for the current dinosaur information and the needed dinosaur information

        Returns
        -------
        dict[str : Dino]
            A current collection of dinosaur names mapped to their corresponding Dino objects
        set[str]
            A set of names of dinosaurs that need to be unlocked
        """
        return self.current_dinos, self.needed_dinos

        
if __name__=='__main__':
    """
    Executes the following steps
        1. Grabs dinosaur information from the database
        2. Removes any unneeded dinosaur information using the UnlockingInfo class
        3. Puts all updated dinosaur information back in the database
    """
    current_dinos, needed_dinos = FileFunctions.create_dino_info()
    unlocking_info = UnlockingInfo(current_dinos, needed_dinos)
    current_dinos, needed_dinos = unlocking_info.get_all_dino_info()
    FileFunctions.save_dino_info(current_dinos, needed_dinos)