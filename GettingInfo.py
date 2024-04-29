import os

from Dino import Dino
import FileFunctions

class GettingInfo:
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

        self.input_dinos()

    def input_dinos(self) -> None:
        """
        Prompts the user for input for dinos that need to be entered into the system
        Checks each dino for parents and adds them to the database as well
        """
        while True:
            wanted_input = input('What dinosaur would you like to get? (Type \'quit\' to quit): ')
            if (wanted_input == 'quit'):
                break
            print()
            self.get_dino_info(wanted_input)
            self.needed_dinos.add(wanted_input)
            os.system('cls')

    def get_dino_info(self, dino_name: str) -> None:
        """
        Given a dinosaur name, prompt the user for information about the dinosaur
        If the dinosaur already exists in the database, no questions are prompted
        Ask if the dinosaur is a hybrid, and if so, ask for the parents names, then run the same function with those names

        Parameters
        ----------
        dino_name : str
            The name of the dinosaur for which information is needed
        """

        # Only getting dinosaur info for dinosaurs that aren't in the database
        if dino_name not in self.current_dinos:
            os.system('cls')
            first = None
            second = None

            # Check if the dinosaur is a hybrid
            if input('Is ' + dino_name + ' a hybrid? (Type \'Y\' if so): ') == 'Y':
                print()
                first = input('Type the first parent of ' + dino_name + ': ')
                second = input('Type the second parent of ' + dino_name + ': ')

            # Get needed dinosaur info and put it in the database
            os.system('cls')
            lvl = input('What level is ' + dino_name + '? ')
            amount = input('How much DNA does ' + dino_name + ' have? ')
            rarity = input('What rarity is ' + dino_name + '? ')
            self.current_dinos[dino_name] = Dino([dino_name, lvl, amount, rarity, first, second])

            # If parents exist for the current dinosaur, check them as well
            if first: self.get_dino_info(first)
            if second: self.get_dino_info(second)

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

        
if __name__=='__main__':
    """
    Executes the following steps
        1. Grabs dinosaur information from the database
        2. Adds any additional dinosaur information using the GettingInfo class
        3. Puts all compiled dinosaur information back in the database
    """
    current_dinos, needed_dinos = FileFunctions.create_dino_info()
    getting_info = GettingInfo(current_dinos, needed_dinos)
    current_dinos, needed_dinos = getting_info.all_dino_info()
    FileFunctions.save_dino_info(current_dinos, needed_dinos)