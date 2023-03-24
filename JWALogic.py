from Dino import Dino
import math

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

def getDNAAmount(dino):
    if dino in recipes:
        parent1, parent2 = recipes[dino]
        p1DNA = getDNAAmount(parent1)
        p2DNA = getDNAAmount(parent2)
        diffP1 = dinos[dino].rarityRank() - dinos[parent1].rarityRank()
        DNAFromP1 = math.floor(p1DNA/((5 if diffP1%2 else 2)*10**int(diffP1/2)))
        diffP2 = dinos[dino].rarityRank() - dinos[parent2].rarityRank()
        DNAFromP2 = math.floor(p2DNA/((5 if diffP2%2 else 2)*10**int(diffP2/2)))
        return min(DNAFromP2, DNAFromP1)
    return dinos[dino].getDNA()

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
priorities = {}
for neededDino in neededDinos:
    if neededDino == 'Pyrorixis':
        print('yee')
    allFusingDNA = {}
    allLvlingDNA = {}
    priorities[neededDino] = [0, {}]
    ancestors = getAncestors(neededDino)
    for anc in ancestors:
        allFusingDNA[anc] = 0
        allLvlingDNA[anc] = 0
        priorities[neededDino][1][anc] = 0

    for anc in ancestors:
        if dinos[anc].getLvl() >= getFuseLvl(anc, neededDino):
            continue

        neededLVL = getFuseLvl(anc, neededDino)
        lvlingDNA = dinos[anc].DNAupToLVL(neededLVL)
        returnedFusingDNA = getAncsWithNeededDNA(anc, lvlingDNA)
        allLvlingDNA[anc] += lvlingDNA
        if len(returnedFusingDNA) != 1:
            for dinoInfo in returnedFusingDNA:
                allFusingDNA[dinoInfo[0]] += dinoInfo[1]

    for anc in ancestors:
        if dinos[anc].getLvl() >= getFuseLvl(anc, neededDino):
            continue
        if anc in recipes:
            parent1, parent2 = recipes[anc]
            if getFuseLvl(parent1, anc) > dinos[parent1].getLvl():
                continue
            if getFuseLvl(parent2, anc) > dinos[parent2].getLvl():
                continue
        
        if getDNAAmount(anc) < allLvlingDNA[anc]:
            priorities[neededDino][1][anc] = 3
        elif getDNAAmount(anc) < allFusingDNA[anc] + allLvlingDNA[anc]:
            priorities[neededDino][1][anc] = 2
        else:
            priorities[neededDino][1][anc] = 1
    priorities[neededDino][0] = max([priorities[neededDino][1][i] for i in priorities[neededDino][1]])
x = 3

        
        



# Is not at hybrid level, has enough to take it all the way
# Is not at hybrid level, has enough to get to hybrid level
# Is not at hybrid level, doesn't have enough
