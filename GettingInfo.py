from Dino import Dino
import os

def checkHybrid(dino):
    os.system('cls')
    isHybridInput = input('Is ' + dino.getName() + ' a hybrid? (Type \'Y\' if so): ')
    isHybrid = (isHybridInput == 'Y')
    if (isHybrid):
        print()

        firstInput = input('Type the first parent of ' + dino.getName() + ': ')
        print()
        first = getDinoInfo(firstInput)
        dino.setFirst(first)
        print()

        secondInput = input('Type the second parent of ' + dino.getName() + ': ')
        print()
        second = getDinoInfo(secondInput)
        dino.setSecond(second)
        print()
        recipes.add(dino.getName() + ': ' + firstInput + ' ' + secondInput)

        checkHybrid(first)
        checkHybrid(second)


def getDinoInfo(name):
    for dino in currentDinos:
        info = dino.split(' ')
        if (info[0] == name):
            return Dino(info[0], info[1], info[2], info[3])
    lvl = input('What level is ' + name + '? ')
    amount = input('How much DNA does ' + name + ' have? ')
    rarity = input('What rarity is ' + name + '? ')
    test = Dino(name, lvl, amount, rarity)
    currentDinos.add(test.toFile())
    return test




dinoReader = open("JWA2\CurrentDinos.txt", "r")
currentDinos = set(dinoReader.read().split("\n"))
dinoReader.close()

recipeReader = open("JWA2\DinoRecipes.txt", "r")
recipes = set(recipeReader.read().split("\n"))
recipeReader.close()

dinoReader = open("JWA2\DinosToGet.txt", "r")
neededDinos = set(dinoReader.read().split("\n"))
dinoReader.close()


input('Welcome to Dino Input. Type quit at any point to leave. Press Enter to begin.')
os.system('cls')

while True:
    wantedInput = input('What dinosaur would you like to get? (Type \'quit\' to quit): ')
    if (wantedInput == 'quit'):
        break
    print()
    wantedDino = getDinoInfo(wantedInput)
    checkHybrid(wantedDino)
    neededDinos.add(wantedDino.name)
    os.system('cls')


neededDinos = [i for i in neededDinos]
neededDinos.sort()
dinoWriter = open("JWA2\DinosToGet.txt", "w")
for dino in neededDinos:
    if dino != '':
        dinoWriter.write(dino + "\n")
dinoWriter.close()

recipes = [i for i in recipes]
recipes.sort()
recipeWriter = open("JWA2\DinoRecipes.txt", "w")
for recipe in recipes:
    if recipe != '':
        recipeWriter.write(recipe + "\n")
recipeWriter.close()
    
currentDinos = [i for i in currentDinos]
currentDinos.sort()
dinoWriter = open("JWA2\CurrentDinos.txt", "w")
for dino in currentDinos:
    if dino != '':
        dinoWriter.write(dino + "\n")
dinoWriter.close()

