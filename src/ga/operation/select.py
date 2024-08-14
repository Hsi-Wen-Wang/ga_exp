import math
import numpy as np
from setting import parameters
###########################################################################################
##################################一般GA選擇，螺絲加工廠#####################################
###########################################################################################
'''
菁英選擇
保留族群(population)前 1% 進入下一代
並加入交配池
'''
def eliteSelect(population, fitness):
    keptPopSize = math.ceil(parameters.pe * parameters.popSize)
    newPop = np.zeros((keptPopSize, population.shape[1], population.shape[2]), dtype=int)

    sort_idx = np.argsort(-fitness)
    for i in range(keptPopSize):
        newPop[i] = population[sort_idx[i]]

    return  newPop
#-----------------------------------------------------------------------------------------#
'''
競爭法:
兩兩比對
較好的一方進入交配池
'''
def competeSelect(population, fitness):
    newPop = np.zeros((math.ceil(parameters.popSize/2), 2, population.shape[2]), dtype=int)
    if parameters.popSize%2 == 0:
        num = parameters.popSize
        idx = 0
        for i in range(0, num, 2):
            if fitness[i] > fitness[i+1]:
                newPop[idx] = population[i]
                idx+=1
            else:
                newPop[idx] = population[i+1]
                idx+=1
    else:
        num = parameters.popSize - 1
        idx = 0
        for i in range(0, num, 2):
            if fitness[i] > fitness[i+1]:
                newPop[idx] = population[i]
                idx+=1
            else:
                newPop[idx] = population[i+1]
                idx+=1
        newPop[-1] = population[-1]

    return newPop
#-----------------------------------------------------------------------------------------#
'''
透過菁英選擇與競爭法建立交配池
'''
def selectSpace(population, fitness):
    parentSpace_elite = eliteSelect(population, fitness)
    parentSpace_compete = competeSelect(population, fitness)
    parentSpace = np.vstack((parentSpace_elite, parentSpace_compete))
    return parentSpace
#-----------------------------------------------------------------------------------------#
'''
選擇
族群前 1% 進入下一代
並透過菁英選擇與競爭法建立交配池
'''
def select(population, fitness):
    newPop = eliteSelect(population, fitness)
    parentSpace = selectSpace(population, fitness)
    return newPop, parentSpace
#-----------------------------------------------------------------------------------------#
