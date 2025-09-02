import os
from Dino import Dino
import FileFunctions

class UpdatingInfo:
    """
    A class in charge of verifying and updating all total info
    ...

    Attributes
    ----------
    current_dinos : dict[str : Dino]
        A current collection of dinosaur names mapped to their corresponding Dino objects
    needed_dinos : set[str]
        A set of names of dinosaurs that need to be unlocked
    """
    
    def __init__(self, c_dinos, n_dinos) -> None:
        """
        Initializes class variables and runs the user input process

        Parameters
        ----------
        c_dinos : dict[str : Dino]
            A current collection of dinosaur names mapped to their corresponding Dino objects
        n_dinos : set[str]
            A set of names of dinosaurs that need to be unlocked
        """

        self.current_dinos = c_dinos
        self.needed_dinos = n_dinos

        self.update_dinos()

    def generate_sorted_dinos_list(self) -> list[str]:
        """
        Takes all current dinosaur names from self.current_dinos and orders them according to the following rules (the default setting in the JWA app):
            1. Have all unlocked dinos first and all locked (needed) dinos second
            2. For unlocked dinos:
                a. Order by level (desc)
                b. Order by rarity (desc)
                c. Order by name (A-Z)
            3. For locked dinos:
                a. Order by if current DNA is 0 (non-zero DNA goes first)
                    For dinos with non-zero DNA
                        i. Order by DNA left to unlock (asc)
                        ii. Order by name (A-Z)
                    For dinos with zero DNA
                        i. Order by name (A-Z)
        Returns
        -------
        list[str]
            A list of names of all current dinosaurs, sorted according the aforementioned rules
        """
        score = {}
        for key in self.current_dinos:
            if key not in self.needed_dinos:
                score[key] = self.current_dinos[key].get_level() * 10 + self.current_dinos[key].rarity_rank()
            else:
                score[key] = -300 if not self.current_dinos[key].get_amount() else -1*(self.current_dinos[key].activation_amount()-self.current_dinos[key].get_amount())

        return sorted(sorted(self.current_dinos, reverse=True), key = lambda dino: score[dino])

    def update_dinos(self) -> None:
        """
        Goes through each dinosaur and checks with the user if the information is current and updates the dinosaur if it isn't current
        """
        sorted_dinos = self.generate_sorted_dinos_list()
        print('Welcome to the Dino Updater! Each dino and its information will be displayed. If the information is correct, just press Enter.')
        print('If it is not but it is the correct dino, type \'c\' and follow the prompts.')
        print('If it is not the right dino, type \'w\' and follow the prompts.')
        input('Press Enter to continue.')
        while sorted_dinos:
            # Retrieve next dinosaur
            current_name = sorted_dinos[-1]
            current_dino = self.current_dinos[current_name]

            # Display the next dinosaur
            os.system('cls')
            user_input = input(current_name + '\nLevel: ' + str(current_dino.get_level()) + '\nAmount: ' + str(current_dino.get_amount()) + '\n')

            # Check info
            if user_input == '': # All correct information
                sorted_dinos.pop()
            elif user_input == 'c': # Correct dinosaur, but incorrect information
                os.system('cls')
                user_input = input('Enter the correct amount for ' + current_name + ', and the level if it has changed.\nAmount: ').split(' ')
                amount = int(user_input[0])
                level = current_dino.get_level() if len(user_input) == 1 else int(user_input[1])

                sorted_dinos.pop()
                self.current_dinos[current_name].set_level(level)
                self.current_dinos[current_name].set_amount(amount)
            elif user_input == 'w': # Wrong dinosaur
                os.system('cls')
                actual_name = input('Enter the name of the dino that should be next.\nName: ')
                os.system('cls')
                level = int(input('Enter the correct level for ' + actual_name + '.\nLevel: '))
                os.system('cls')
                amount = int(input('Enter the correct amount for ' + actual_name + '.\nAmount: '))

                if actual_name in self.needed_dinos and level > self.current_dinos[actual_name].activation_level():
                    self.needed_dinos.remove(actual_name)

                sorted_dinos.remove(actual_name)
                self.current_dinos[actual_name].set_level(level)
                self.current_dinos[actual_name].set_amount(amount)

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
        2. Updates any additional dinosaur information using the UpdatingInfo class
        3. Puts all compiled dinosaur information back in the database
    """
    current_dinos, needed_dinos = FileFunctions.create_dino_info()
    updating_info = UpdatingInfo(current_dinos, needed_dinos)
    current_dinos, needed_dinos = updating_info.get_all_dino_info()
    FileFunctions.save_dino_info(current_dinos, needed_dinos)