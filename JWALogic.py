from Dino import Dino

recipes = {}
dinos = {}

recipeReader = open("JWA2\DinoRecipes.txt", "r")
recipeLines = recipeReader.read().split("\n")
for line in recipeLines:
    recipeDinos = line.split(" ")
    recipes[recipeDinos[0][:-1]] = [recipeDinos[1], recipeDinos[2]]

dinoReader = open("JWA2\DinosToGet.txt", "r")
neededDinos = dinoReader.read().split("\n")

currentReader = open("JWA2\CurrentDinos.txt", "r")
currentDinos = currentReader.read().split("\n")
for currentDino in currentDinos:
    [dinoName, dinoLVL, dinoDNA, dinoRarity] = currentDino.split(" ")
    if dinoName in dinos:
        dinos[dinoName].updateInfo(int(dinoDNA), int(dinoLVL), dinoRarity)
    else:
        dinos[dinoName] = Dino(dinoName, dinoRarity, int(dinoDNA), int(dinoLVL))

for neededDino in neededDinos:
    nDino = dinos[neededDino]
    for parent in recipes[neededDino]:
        pDino = dinos[parent]
        LvlToGetTo = min(nDino.activationLVL, )
