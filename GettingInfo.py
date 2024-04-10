from Dino import Dino
import os

class GettingInfo:
    """
    A class in charge of managing adding new dinosaurs and their parents
    ...

    Attributes
    ----------
    current_dinos : dict(str : Dino)
        A mapping of dinosaur names to the corresponding Dino objects
    needed_dinos : set(str)
        A set of names of dinosaurs that need to be unlocked

    Methods
    -------
    create_dino_info()
        Grabs current dinosaur information from CurrentDinos.txt, recipes from DinoRecipes.txt, and needed dinosaurs from DinosToGet.txt
    input_dinos()
        Gets new dinosaur information from the user and saves it
    save_dino_info()
        Saves dinosaur information to CurrentDinos.txt, DinoRecipes.txt, and DinosToGet.txt
    """
    
    def __init__(self) -> None:
        """
        Starts the getting dinosaur info task
        1. Grab dinosaur information from the database
        2. Add any additional dinosaur information
        3. Put all compiled dinosaur information back in the database
        """
        self.current_dinos = {}
        self.needed_dinos = set()

        self.create_dino_info()
        self.input_dinos()
        self.save_dino_info()

    def create_dino_info(self) -> None:
        """
        Grabs current dinosaur information from CurrentDinos.txt, recipes from DinoRecipes.txt, and needed dinosaurs from DinosToGet.txt
        """

        # Adds each dinosaur from CurrentDinos.txt into self.current_dinos as a map from a name to a Dino object
        dino_reader = open("CurrentDinos.txt", "r")
        self.current_dinos = {i.split(' ')[0]: Dino(i.split(' ')) for i in dino_reader.read().split('\n')}
        dino_reader.close()

        # Takes each pair of parents from DinoRecipes.txt and adds them to the corresponding child in self.current_dinos
        dino_reader = open("DinoRecipes.txt", "r")
        for recipe in dino_reader.read().split("\n"):
            child, parent_string = recipe.split(': ')
            parents = parent_string.split(' ')
            self.current_dinos[child].set_parents(parents)
        dino_reader.close()

        # Adds each needed dinosaur from DinosToGet.txt to self.needed_dinos
        dino_reader = open("DinosToGet.txt", "r")
        self.needed_dinos = set(dino_reader.read().split("\n"))
        dino_reader.close()

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

    def save_dino_info(self):
        """
        Writes each list of dinosaurs (needed, current, and their recipes) as output strings and saves them to their corresponding files
        """
        needed_dinos_output = '\n'.join(self.needed_dinos)
        current_dinos_output = '\n'.join([self.current_dinos[dino].to_string() for dino in self.current_dinos])
        recipe_output = '\n'.join([self.current_dinos[dino].parent_to_string() for dino in self.current_dinos if self.current_dinos[dino].is_hybrid()])

        dino_writer = open("DinosToGet.txt", "w")
        dino_writer.write(needed_dinos_output)
        dino_writer.close()

        dino_writer = open("CurrentDinos.txt", "w")
        dino_writer.write(current_dinos_output)
        dino_writer.close()

        dino_writer = open("DinoRecipes.txt", "w")
        dino_writer.write(recipe_output)
        dino_writer.close()
        
if __name__=='__main__':
    getting_info = GettingInfo()