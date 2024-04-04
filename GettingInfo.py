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
    """
    
    def __init__(self) -> None:
        self.current_dinos = {}
        self.needed_dinos = set()

        self.create_dino_info()

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


# def checkHybrid(dino):
#     os.system('cls')
#     isHybridInput = input('Is ' + dino.getName() + ' a hybrid? (Type \'Y\' if so): ')
#     isHybrid = (isHybridInput == 'Y')
#     if (isHybrid):
#         print()

#         firstInput = input('Type the first parent of ' + dino.getName() + ': ')
#         print()
#         first = getDinoInfo(firstInput)
#         dino.setFirst(first)
#         print()

#         secondInput = input('Type the second parent of ' + dino.getName() + ': ')
#         print()
#         second = getDinoInfo(secondInput)
#         dino.setSecond(second)
#         print()
#         recipes.add(dino.getName() + ': ' + firstInput + ' ' + secondInput)

#         checkHybrid(first)
#         checkHybrid(second)


# def getDinoInfo(name):
#     for dino in currentDinos:
#         info = dino.split(' ')
#         if (info[0] == name):
#             return Dino(info[0], info[1], info[2], info[3])
#     lvl = input('What level is ' + name + '? ')
#     amount = input('How much DNA does ' + name + ' have? ')
#     rarity = input('What rarity is ' + name + '? ')
#     test = Dino(name, lvl, amount, rarity)
#     currentDinos.add(test.toFile())
#     return test

# input('Welcome to Dino Input. Type quit at any point to leave. Press Enter to begin.')
# os.system('cls')

# while True:
#     wantedInput = input('What dinosaur would you like to get? (Type \'quit\' to quit): ')
#     if (wantedInput == 'quit'):
#         break
#     print()
#     wantedDino = getDinoInfo(wantedInput)
#     checkHybrid(wantedDino)
#     neededDinos.add(wantedDino.name)
#     os.system('cls')


# neededDinos = [i for i in neededDinos]
# neededDinos.sort()
# dinoWriter = open("JWA2\DinosToGet.txt", "w")
# for dino in neededDinos:
#     if dino != '':
#         dinoWriter.write(dino + "\n")
# dinoWriter.close()

# recipes = [i for i in recipes]
# recipes.sort()
# recipeWriter = open("JWA2\DinoRecipes.txt", "w")
# for recipe in recipes:
#     if recipe != '':
#         recipeWriter.write(recipe + "\n")
# recipeWriter.close()
    
# currentDinos = [i for i in currentDinos]
# currentDinos.sort()
# dinoWriter = open("JWA2\CurrentDinos.txt", "w")
# for dino in currentDinos:
#     if dino != '':
#         dinoWriter.write(dino + "\n")
# dinoWriter.close()

if __name__=='__main__':
    getting_info = GettingInfo()