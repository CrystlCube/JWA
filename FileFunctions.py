from Dino import Dino

def create_dino_info() -> tuple[dict[str: Dino], set[str]]:
    """
    Grabs current dinosaur information from CurrentDinos.txt, recipes from DinoRecipes.txt, and needed dinosaurs from DinosToGet.txt
    Makes a set of needed dinos, as well as a dictionary that maps names of current dinos to the Dino objects

    Returns
    -------
    dict[str: Dino]
        A dictionary that stores keys as names of current dinosaurs, and the values as the corresponding Dino objects
    set[str]
        A set of needed dinosaur names
    """

    # Adds each dinosaur from CurrentDinos.txt into self.current_dinos as a map from a name to a Dino object
    dino_reader = open("CurrentDinos.txt", "r")
    current_dinos = {i.split(' ')[0]: Dino(i.split(' ')) for i in dino_reader.read().split('\n')}
    dino_reader.close()

    # Takes each pair of parents from DinoRecipes.txt and adds them to the corresponding child in self.current_dinos
    dino_reader = open("DinoRecipes.txt", "r")
    for recipe in dino_reader.read().split("\n"):
        child, parent_string = recipe.split(': ')
        parents = parent_string.split(' ')
        current_dinos[child].set_parents(parents)
    dino_reader.close()

    # Adds each needed dinosaur from DinosToGet.txt to self.needed_dinos
    dino_reader = open("DinosToGet.txt", "r")
    needed_dinos = set(dino_reader.read().split("\n"))
    dino_reader.close()

    return current_dinos, needed_dinos


def save_dino_info(current_dinos, needed_dinos) -> None:
    """
    Writes each list of dinosaurs (needed, current, and their recipes) as output strings and saves them to their corresponding files

    Parameters
    ----------
    current_dinos: dict[str: Dino]
        A dictionary that stores keys as names of current dinosaurs, and the values as the corresponding Dino objects
    needed_dinos: set[str]
        A set of needed dinosaur names
    """
    needed_dinos_output = '\n'.join(sorted(needed_dinos))
    current_dinos_output = '\n'.join(sorted([current_dinos[dino].to_string() for dino in current_dinos]))
    recipe_output = '\n'.join(sorted([current_dinos[dino].parent_to_string() for dino in current_dinos if current_dinos[dino].is_hybrid()]))

    dino_writer = open("DinosToGet.txt", "w")
    dino_writer.write(needed_dinos_output)
    dino_writer.close()

    dino_writer = open("CurrentDinos.txt", "w")
    dino_writer.write(current_dinos_output)
    dino_writer.close()

    dino_writer = open("DinoRecipes.txt", "w")
    dino_writer.write(recipe_output)
    dino_writer.close()