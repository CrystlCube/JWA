from Dino import Dino
import math
DNA_PER_FUSE = 20

def checkIfLvlingEligible(dino, child):
    if dinos[dino].getLvl() > dinos[dino].activationLvl():
        if dinos[child].activationLvl() > dinos[dino].getLvl():
            return [dino]
    else:
        if dino in recipes:
            p1, p2 = recipes[dino]
            return checkIfLvlingEligible(p1, dino) + checkIfLvlingEligible(p2, dino)
    return []

def getChild(anc, neededDino):
    if neededDino in recipes:
        p1, p2 = recipes[neededDino]
        if (p1 == anc) or (p2 == anc):
            return neededDino
        return getChild(anc, p1) + getChild(anc, p2)
    return ''

def getDNAandCost(dino):
    if dino in recipes:
        p1, p2 = recipes[dino]
        p1DNA, p1Cost = getDNAandCost(p1)
        p1Fuses = math.floor(p1DNA/DNAforEachFuse(dinos[p1], dinos[dino]))
        p2DNA, p2Cost = getDNAandCost(p2)
        p2Fuses = math.floor(p2DNA/DNAforEachFuse(dinos[p2], dinos[dino]))
        rR = dinos[dino].rarityRank()
        costPerFuse = 10*(2 if rR%2 else 1)*10**int(rR/2)
        minFuses = min(p1Fuses, p2Fuses)
        totalFuseCost = minFuses*costPerFuse
        return DNA_PER_FUSE*minFuses+dinos[dino].getDNA(), p1Cost+p2Cost+totalFuseCost
    return dinos[dino].getDNA(), 0

def DNAforEachFuse(dinosaur, childDino):
    diff = childDino.rarityRank() - dinosaur.rarityRank()
    return 10*(5 if diff%2 else 2)*10**int(diff/2)
    
def neededForFusing(dinosaur, childDino, neededChildDNA):
    neededFuses = math.ceil(neededChildDNA/DNA_PER_FUSE)
    return neededFuses*DNAforEachFuse(dinosaur, childDino)


def getCost(dino, child):
    enoughForFusing = False
    allTheWay = False
    addedCost = 0
    dinosaur = dinos[dino]
    childDino = dinos[child]
    DNAleft, addedCost = getDNAandCost(dino)
    currentLvl = dinosaur.getLvl()
    while DNAleft >= dinosaur.DNAforLvl(currentLvl+1):
        currentLvl += 1
        DNAleft -= dinosaur.DNAforLvl(currentLvl)
        addedCost += levelingCost[currentLvl]
        if currentLvl == childDino.activationLvl():
            enoughForFusing = True
            break
    
    if enoughForFusing:
        allTheWay = DNAleft >= neededForFusing(dinosaur, childDino, childDino.activationDNA() - childDino.getDNA())
    
    priority = (not allTheWay) + (not enoughForFusing) + 1
    return priority, addedCost, dino


def getNeededAmounts(dino, neededAmount, amountForH):
    tag = 'blue'
    dinosaur = dinos[dino]
    readyToLvl = True
    if dino in recipes:
        p1, p2 = recipes[dino]
        p1Dino = dinos[p1]
        p2Dino = dinos[p2]
        p1DNA = neededForFusing(p1Dino, dinosaur, neededAmount)
        p2DNA = neededForFusing(p2Dino, dinosaur, neededAmount)
        if p1Dino.getLvl() < dinosaur.activationLvl():
            readyToLvl = False
            temp = p1Dino.getLvl()
            while temp < dinosaur.activationLvl():
                temp += 1
                p1DNA += p1Dino.DNAforLvl(temp)

        if p2Dino.getLvl() < dinosaur.activationLvl():
            readyToLvl = False
            temp = p2Dino.getLvl()
            while temp < dinosaur.activationLvl():
                temp += 1
                p2DNA += p2Dino.DNAforLvl(temp)
            
    totalDNA = (getDNAandCost(dino)[0] if readyToLvl else dinosaur.getDNA())
    if totalDNA < neededAmount:
        if amountForH != 0:
            if totalDNA < amountForH:
                tag = 'purple'
        else:
            if totalDNA < dinosaur.DNAforLvl(dinosaur.getLvl()+1):
                tag = 'purple'
        if dino in recipes:
            return getNeededAmounts(p1, p1DNA, DNAforEachFuse(p1Dino, dinosaur)) + getNeededAmounts(p2, p2DNA, DNAforEachFuse(p2Dino, dinosaur))
        return [(dino, tag)]

    if dino in recipes:
            p1, p2 = recipes[dino]
            return getNeededAmounts(p1, 0, 0) + getNeededAmounts(p1, 0, 0)
    return [(dino, 'orange')]

#--------------------------------------------------------------------------------------------------------------------------------------------------

recipes = {}
dinos = {}

levelingCost = {2: 5, 3: 10, 4: 25, 5: 50, 6: 100, 7: 200, 8: 400, 9: 600, 10: 800,
                11: 1000, 12: 2000, 13: 4000, 14: 6000, 15: 8000, 16: 10000, 17: 15000, 18: 20000, 19: 30000, 20: 40000,
                21: 50000, 22: 60000, 23: 70000, 24: 80000, 25: 100000}

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

# --------------------------------------------------------------------------------------------------------------------

dinosForLvling = {}

for neededDino in neededDinos:
    dinosForLvling[neededDino] = checkIfLvlingEligible(neededDino, None)

priorities = []
for neededDino in neededDinos:
    requirements = dinosForLvling[neededDino]
    for req in requirements:
        child = getChild(req, neededDino)
        cost = getCost(req, child)
        if (cost[1] != 0):
            priorities.append(getCost(req, child))

priorities = sorted(priorities)

amounts = []
for neededDino in neededDinos:
    neededDNA = dinos[neededDino].activationDNA() - dinos[neededDino].getDNA()
    needed = getNeededAmounts(neededDino, neededDNA, 0)
    origIn = False
    for i in needed:
        if neededDino == i[0]:
            origIn = True
            break
    
    if origIn: needed = needed.remove(i)
    if needed:
        amounts += needed

print(sorted(amounts))


# First, is the dinosaur above its activation level?
    # If it is not, check its children
    # If it is, is it not yet at fuse level?
        # If it is at fuse level, don't bother
        # If it is not, it is viable for leveling



# For each dino in requirements:
    # Hypothetically, level up each dino as far as it can go
    # If it is a hybrid, take that into account









# def getAncestors(child):
#     if child in recipes:
#         parent1, parent2 = recipes[child]
#         gen1 = getAncestors(parent1)
#         gen2 = getAncestors(parent2)
#         return gen1 + gen2 + [child]
#     return [child]

# def getAncsWithNeededDNA(child, childDNA):
#     if child in recipes:
#         parent1, parent2 = recipes[child]
#         diffP1 = dinos[child].rarityRank() - dinos[parent1].rarityRank()
#         DNAForP1 = childDNA*(5 if diffP1%2 else 2)*10**int(diffP1/2)
#         diffP2 = dinos[child].rarityRank() - dinos[parent2].rarityRank()
#         DNAForP2 = childDNA*(5 if diffP2%2 else 2)*10**int(diffP2/2)
#         return getAncsWithNeededDNA(parent1, DNAForP1) + getAncsWithNeededDNA(parent2, DNAForP2)
#     return [(child, childDNA)]


# def getFuseLvl(neededAnc, currentChild):
#     if (currentChild == neededAnc): 
#         return dinos[currentChild].activationLVL()+1
#     if currentChild in recipes:
#         anc1, anc2 = recipes[currentChild]
#         if (anc1 == neededAnc or anc2 == neededAnc):
#             return dinos[currentChild].activationLVL()
#         maxLvl = 0
#         if getFuseLvl(neededAnc, anc1) != None:
#             maxLvl = getFuseLvl(neededAnc, anc1)
#         if getFuseLvl(neededAnc, anc2) != None:
#             maxLvl = max(maxLvl, getFuseLvl(neededAnc, anc2))
#         return maxLvl
#     return None


# for every needed dino, I want to look at what is required to get it
# as I go through each dino, I will sort it according to a pre-determined system

# for neededDino in neededDinos:
#     allFusingDNA = {}
#     allLvlingDNA = {}
#     priority = 1
#     ancestors = getAncestors(neededDino)
#     for anc in ancestors:
#         allFusingDNA[anc] = 0
#         allLvlingDNA[anc] = 0

#     for anc in ancestors:
#         if dinos[anc].getLvl() >= getFuseLvl(anc, neededDino):
#             continue

#         neededLVL = getFuseLvl(anc, neededDino)
#         lvlingDNA = dinos[anc].DNAupToLVL(neededLVL)
#         returnedFusingDNA = getAncsWithNeededDNA(anc, lvlingDNA)
#         if len(returnedFusingDNA) == 1:
#             allLvlingDNA[anc] += lvlingDNA
#         else:
#             for dinoInfo in returnedFusingDNA:
#                 allFusingDNA[dinoInfo[0]] += dinoInfo[1]

#     for anc in ancestors:
#         if dinos[anc].getDNA() < allLvlingDNA[anc]:
#             priority = 3
#         elif dinos[anc].getDNA() < allFusingDNA[anc] + allLvlingDNA[anc]:
#             priority = 2
        



# Is not at hybrid level, has enough to take it all the way
# Is not at hybrid level, has enough to get to hybrid level
# Is not at hybrid level, doesn't have enough
