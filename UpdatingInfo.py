import os

from Dino import Dino
import FileFunctions

class UpdatingInfo:
    #TODO
    def __init__(self, c_dinos, n_dinos) -> None:
        """
        A class in charge of updating dinosaur information to match the current app information from the user
        ...

        Attributes
        ----------
        current_dinos : dict[str : Dino]
            A mapping of dinosaur names to the corresponding Dino objects
        needed_dinos : set[str]
            A set of names of dinosaurs that need to be unlocked
        sorted_dinos : list[str]
            A list of current dino names sorted according to the default order in the JWA app

        Methods
        -------
        generate_sorted_dinos_list()
            Generate a list of dinosaur names that matches the deafult order of dinosaurs in the JWA app
        update_dinos()
            Display to the user each dinosaur and its information and enable updating dinosaur information by the user
        """

        self.current_dinos = c_dinos
        self.needed_dinos = n_dinos

        self.update_dinos()

    def generate_sorted_dinos_list(self) -> list[str]:
        """
        Take all current dino names from self.current_dinos and order them according to the following precedents:
            1. Have all unlocked dinos first and all locked (needed) dinos second
            2. For unlocked dinos:
                a. Order by level
                b. Order by rarity
                c. Order by name
            3. For locked dinos:
                a. Order by if current DNA is 0
                b. For dinos with non-zero DNA
                    i. Order by DNA left to unlock
                    ii. Order by name
                c. For dinos with zero DNA
                    i. Order by name 
        """
        score = {}
        for key in self.current_dinos:
            if key not in self.needed_dinos:
                score[key] = self.current_dinos[key].get_level() * 10 + self.current_dinos[key].rarity_rank()
            else:
                score[key] = -300 if not self.current_dinos[key].get_amount() else -1*(self.current_dinos[key].activation_amount()-self.current_dinos[key].get_amount())

        return sorted(sorted(self.current_dinos, reverse=True), key = lambda dino: score[dino])

    def update_dinos(self):
        """
        First, get a sorted list of dinosaur names from generate_sorted_dinos_list()
        Next, go through each dinosaur name in the sorted list and check with the user if its information is correct
        If not, change current_dinos to reflect the newer information
        """
        sorted_dinos = self.generate_sorted_dinos_list()
        print('Welcome to the Dino Updater! Each dino and its information will be displayed. If the information is correct, just press Enter.')
        print('If it is not but it is the correct dino, type \'c\' and follow the prompts.')
        print('If it is not the right dino, type \'w\' and follow the prompts.')
        input('Press Enter to continue.')
        while sorted_dinos:
            current_name = sorted_dinos[-1]
            current_dino = self.current_dinos[current_name]

            os.system('cls')
            user_input = input(current_name + '\nLevel: ' + str(current_dino.get_level()) + '\nAmount: ' + str(current_dino.get_amount()) + '\n')

            if user_input == '':
                sorted_dinos.pop()
            elif user_input == 'c': # Change
                os.system('cls')
                lvl = input('Enter the correct level for ' + current_name + '.\nLevel: ')
                os.system('cls')
                amount = input('Enter the correct amount for ' + current_name + '.\nAmount: ')

                sorted_dinos.pop()
                self.current_dinos[current_name].set_level(lvl)
                self.current_dinos[current_name].set_amount(amount)
            elif user_input == 'w': # Wrong
                os.system('cls')
                actual_name = input('Enter the name of the dino that should be next.\nName: ')
                os.system('cls')
                lvl = input('Enter the correct level for ' + actual_name + '.\nLevel: ')
                os.system('cls')
                amount = input('Enter the correct amount for ' + actual_name + '.\nAmount: ')

                sorted_dinos.remove(actual_name)
                self.current_dinos[actual_name].set_level(lvl)
                self.current_dinos[actual_name].set_amount(amount)

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
        2. Updates any additional dinosaur information using the UpdatingInfo class
        3. Puts all compiled dinosaur information back in the database
    """
    current_dinos, needed_dinos = FileFunctions.create_dino_info()
    updating_info = UpdatingInfo(current_dinos, needed_dinos)
    current_dinos, needed_dinos = updating_info.all_dino_info()
    FileFunctions.save_dino_info(current_dinos, needed_dinos)