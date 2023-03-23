from Dino import Dino

recipes = {}
dinos = {}

def getAncestors(child):
    if child in recipes:
        parent1, parent2 = recipes[child]
        gen1 = getAncestors(parent1)
        gen2 = getAncestors(parent2)
        return gen1 + gen2 + [child]
    return [child]

def getAncsWithNeededDNA(child, childDNA):
    if child in recipes:
        parent1, parent2 = recipes[child]
        diffP1 = dinos[child].rarityRank() - dinos[parent1].rarityRank()
        DNAForP1 = childDNA*(5 if diffP1%2 else 2)*10**int(diffP1/2)
        diffP2 = dinos[child].rarityRank() - dinos[parent2].rarityRank()
        DNAForP2 = childDNA*(5 if diffP2%2 else 2)*10**int(diffP2/2)
        return getAncsWithNeededDNA(parent1, DNAForP1) + getAncsWithNeededDNA(parent2, DNAForP2)
    return [(child, childDNA)]


def getFuseLvl(neededAnc, currentChild):
    if (currentChild == neededAnc): 
        return dinos[currentChild].activationLVL()+1
    if currentChild in recipes:
        anc1, anc2 = recipes[currentChild]
        if (anc1 == neededAnc or anc2 == neededAnc):
            return dinos[currentChild].activationLVL()
        maxLvl = 0
        if getFuseLvl(neededAnc, anc1) != None:
            maxLvl = getFuseLvl(neededAnc, anc1)
        if getFuseLvl(neededAnc, anc2) != None:
            maxLvl = max(maxLvl, getFuseLvl(neededAnc, anc2))
        return maxLvl
    return None

recipeReader = open("DinoRecipes.txt", "r")
recipeLines = recipeReader.read().split("\n")
for line in recipeLines:
    recipeDinos = line.split(" ")
    recipes[recipeDinos[0][:-1]] = [recipeDinos[1], recipeDinos[2]]

dinoReader = open("DinosToGet.txt", "r")
neededDinos = dinoReader.read().split("\n")

currentReader = open("CurrentDinos.txt", "r")
currentDinos = currentReader.read().split("\n")
for currentDino in currentDinos:
    [dinoName, dinoLVL, dinoDNA, dinoRarity] = currentDino.split(" ")
    if dinoName in dinos:
        dinos[dinoName].updateInfo(int(dinoDNA), int(dinoLVL), dinoRarity)
    else:
        dinos[dinoName] = Dino(dinoName, int(dinoLVL), int(dinoDNA), dinoRarity)


# for every needed dino, I want to look at what is required to get it
# as I go through each dino, I will sort it according to a pre-determined system

for neededDino in neededDinos:
    allFusingDNA = {}
    allLvlingDNA = {}
    priority = 1
    ancestors = getAncestors(neededDino)
    for anc in ancestors:
        allFusingDNA[anc] = 0
        allLvlingDNA[anc] = 0

    for anc in ancestors:
        if dinos[anc].getLvl() >= getFuseLvl(anc, neededDino):
            continue

        neededLVL = getFuseLvl(anc, neededDino)
        lvlingDNA = dinos[anc].DNAupToLVL(neededLVL)
        returnedFusingDNA = getAncsWithNeededDNA(anc, lvlingDNA)
        if len(returnedFusingDNA) == 1:
            allLvlingDNA[anc] += lvlingDNA
        else:
            for dinoInfo in returnedFusingDNA:
                allFusingDNA[dinoInfo[0]] += dinoInfo[1]

    for anc in ancestors:
        if dinos[anc].getDNA() < allLvlingDNA[anc]:
            priority = 3
        elif dinos[anc].getDNA() < allFusingDNA[anc] + allLvlingDNA[anc]:
            priority = 2
        



# Is not at hybrid level, has enough to take it all the way
# Is not at hybrid level, has enough to get to hybrid level
# Is not at hybrid level, doesn't have enough
