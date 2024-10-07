import os
from Dino import Dino
import FileFunctions

class UnlockingInfo:
    """
    A class in charge of managing adding new dinosaurs and their parents
    ...

    Attributes
    ----------
    current_dinos : dict[str : Dino]
        A mapping of dinosaur names to the corresponding Dino objects
    needed_dinos : set[str]
        A set of names of dinosaurs that need to be unlocked

    Methods
    -------
    input_dinos()
        Gets new dinosaur information from the user and saves it
    get_dino_info()
        Gets information from the user about the specified dinosaur
    all_dino_info()
        Returns the current and needed dinosaur information
    """
    
    def __init__(self, c_dinos: dict[str: Dino], n_dinos: set[str]) -> None:
        """
        Initializes the GettingInfo class with the given current and needed dinos, then runs input_dinos()
        
        Parameters
        ----------
        c_dinos: dict[str: Dino]
            A dictionary that stores keys as names of current dinosaurs, and the values as the corresponding Dino objects
        n_dinos: set[str]
            A set of needed dinosaur names
        """
        self.current_dinos = c_dinos
        self.needed_dinos = n_dinos

        self.get_input()

    def get_input(self) -> None:
        """
        Prompts the user for input for dinos that have been unlocked
        Checks each dino and its parents and clears them out if they are no longer needed
        """
        while True:
            wanted_input = input('What dinosaur have you unlocked? (Type \'quit\' to quit): ')
            if (wanted_input == 'quit'):
                break
            print()
            self.clear_dino(wanted_input)
            self.needed_dinos.remove(wanted_input)
            os.system('cls')

    def all_dino_info(self) -> tuple[dict[str: Dino], set[str]]:
        """
        A getter for the current dinosaur information and the needed dinosaur information

        Returns
        -------
        dict[str: Dino]
            A dictionary that stores keys as names of current dinosaurs, and the values as the corresponding Dino objects
        set[str]
            A set of needed dinosaur names
        """
        return self.current_dinos, self.needed_dinos


    def clear_dino(self, unlocked_dino):
        has_other_child = False
        for dino_name in self.current_dinos:
            dino = self.current_dinos[dino_name]
            if dino.is_hybrid():
                if unlocked_dino in dino.get_parents():
                    has_other_child = True
        
        if not has_other_child:
            first = None
            if self.current_dinos[unlocked_dino].is_hybrid():
                first, second = self.current_dinos[unlocked_dino].get_parents()

            self.current_dinos.pop(unlocked_dino)
            if first:
                self.clear_dino(first)
                self.clear_dino(second)


        
if __name__=='__main__':
    """
    Executes the following steps
        1. Grabs dinosaur information from the database
        2. Adds any additional dinosaur information using the GettingInfo class
        3. Puts all compiled dinosaur information back in the database
    """
    current_dinos, needed_dinos = FileFunctions.create_dino_info()
    unlocking_info = UnlockingInfo(current_dinos, needed_dinos)
    current_dinos, needed_dinos = unlocking_info.all_dino_info()
    FileFunctions.save_dino_info(current_dinos, needed_dinos)



    # Ideas
    # Similar "enter or type quit to quit"
    # For each dino, look at if it is a child to any other dino
    # If it is, leave it alone
    # But if it is not, get rid of its recipe and info and do the same for its children