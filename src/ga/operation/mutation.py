import random
import numpy as np
from setting import parameters, globals
from src.ga.codec.encoding import randMachine
###########################################################################################
##################################一般GA變異，螺絲加工廠#####################################
###########################################################################################
'''
os
雙點突變:
任兩點進行交換
'''
def twoPointSwappingMutation(p):
    pos1 = random.randint(0, len(p) - 1)
    pos2 = random.randint(0, len(p) - 1)
    offspring = np.zeros(p.size, dtype=int)

    if pos1 == pos2:
        return p

    if pos1 > pos2:
        pos1, pos2 = pos2, pos1

    offspring[:pos1], offspring[pos2], offspring[pos1+1:pos2], offspring[pos1], offspring[pos2+1:] \
        = p[:pos1], p[pos2], p[pos1+1:pos2], p[pos1], p[pos2+1:]
    return offspring
#-----------------------------------------------------------------------------------------#
'''
os
多點突變
多點進行交換
'''
def multiPointSwappingMutation(p):
    points = random.randint(0, p.size)
    mutateRange = range(0, p.size)
    listSwapPointIndex = random.sample(mutateRange, points)
    swapValueList = np.zeros(len(listSwapPointIndex), dtype=int)
    offspring = np.zeros(p.size, dtype=int)
    for i, idx in enumerate(listSwapPointIndex):
        swapValueList[i] = p[idx]
    num = 0
    for i in range(p.size):
        if i in listSwapPointIndex:
            offspring[i] = swapValueList[num]
            num+=1
        else:
            offspring[i] = p[i]

    return offspring
#-----------------------------------------------------------------------------------------#
'''
ms
多點突變
多點的機器進行隨機變換
'''
def multiPointMutation(p):
    offspring = np.zeros(p.size, dtype=int)
    points = random.randint(0, p.size)
    mutateRange = range(0, p.size)
    listPointIndex = random.sample(mutateRange, points)
    
    for i in range(len(p)):
        if i in listPointIndex:
                presentJob = globals.order_content['msTable'][f'{i}'][0]
                presentOp = globals.order_content['msTable'][f'{i}'][1]

                jobInfo = [globals.order_content['jobs'][f'job{presentJob}']['type'], \
                           
                           globals.order_content['jobs'][f'job{presentJob}']['operator'][f'op{presentOp}']]
                offspring[i] = randMachine(jobInfo)
        else:
            offspring[i] = p[i]
            
    return offspring
#-----------------------------------------------------------------------------------------#
'''
os 突變
雙點突變、多點突變(位移) 隨機二選一
'''
def mutationOS(p):
    if random.choice([True, False]):
        return twoPointSwappingMutation(p)
    else:
        return multiPointSwappingMutation(p)
#-----------------------------------------------------------------------------------------#
'''
ms 突變
任意多點機器隨機變換
'''
def mutationMS(p):
    return multiPointMutation(p)
#-----------------------------------------------------------------------------------------#
'''
突變
'''
def mutation(population):
    newPop = np.zeros(population.shape, dtype=int)

    for i,(OS, MS) in enumerate(population):
        if random.random() < parameters.pm:
            newPop[i][0] = mutationOS(OS)
            newPop[i][1] = mutationMS(MS)
        else:
            newPop[i][0] = OS
            newPop[i][1] = MS

    return newPop