import random
import math
import numpy as np
from setting import parameters, globals
###########################################################################################
##################################一般GA交叉，螺絲加工廠#####################################
###########################################################################################
'''
生成交配的訂單表
'''
def generateCrossoverSet(num):
    jobNumber = globals.order_content['totalJobs']
    jobsRange = range(1, jobNumber+1)
    sizeJobset1 = random.randint(0, jobNumber)
    if num == 1:
        return np.random.choice(jobsRange, size=sizeJobset1, replace=False)
    elif num == 2:
        jobset1 = np.random.choice(jobsRange, size=sizeJobset1, replace=False)
        return jobset1, np.array([item for item in jobsRange if item not in jobset1],dtype=int)
    else:
        print('plz give crossover parameter 1 or 2')
#-----------------------------------------------------------------------------------------#
'''
OS的POC，crossover方法
'''
def precedenceOperationCrossover(p1, p2):
    
    jobset1 = generateCrossoverSet(1)

    o1 = np.zeros(p1.size, dtype=int)
    o2 = np.zeros(p2.size, dtype=int)

    # return true false
    p1kept = np.isin(p1, jobset1)
    p1fill = p1[~p1kept]
    p2kept = np.isin(p2, jobset1)
    p2fill = p2[~p2kept]

    num = 0
    for i, job in enumerate(p1kept):
        if job:
            o1[i] = p1[i]
        else:
            o1[i] = p2fill[num]
            num+=1

    num = 0
    for i, job in enumerate(p2kept):
        if job:
            o2[i] = p2[i]
        else:
            o2[i] = p1fill[num]
            num+=1

    return o1, o2
'''
OS的JBC，crossover方法
'''
def jobBasedCrossover(p1, p2):

    jobset1, jobset2 = generateCrossoverSet(2)
    o1 = np.zeros(p1.size, dtype=int)
    o2 = np.zeros(p2.size, dtype=int)

    p1kept = np.isin(p1, jobset1)
    p2kept1 = np.isin(p2, jobset1)
    p2fill = p2[~p2kept1]
    p2kept2 = np.isin(p2, jobset2)
    p1fill = p1[p1kept]

    num = 0
    for i, job in enumerate(p1kept):
        if job:
            o1[i] = p1[i]
        else:
            o1[i] = p2fill[num]
            num+=1

    num = 0
    for i, job in enumerate(p2kept2):
        if job:
            o2[i] = p2[i]
        else:
            o2[i] = p1fill[num]
            num+=1

    return o1, o2
#-----------------------------------------------------------------------------------------#
'''
雙點crossover方式
'''
def twoPointCrossover(p1, p2):
    pos1 = random.randint(0, p1.size - 1)
    pos2 = random.randint(0, p2.size - 1)

    if pos1 > pos2:
        pos2, pos1 = pos1, pos2

    offspring1 = p1
    if pos1 != pos2:
        offspring1[:pos1], offspring1[pos1:pos2], offspring1[pos2:] = p1[:pos1], p2[pos1:pos2], p1[pos2:]
    offspring1 = np.array(offspring1, dtype=int)

    offspring2 = p2
    if pos1 != pos2:
        offspring2[:pos1], offspring2[pos1:pos2], offspring2[pos2:] = p2[:pos1], p1[pos1:pos2], p2[pos2:]
    offspring2 = np.array(offspring2, dtype=int)

    return offspring1.flatten(), offspring2.flatten()
#-----------------------------------------------------------------------------------------#
'''
os的crossover
POC 和 JBC 隨機二選一
'''
def crossoverOS(p1, p2):
    if random.choice([True, False]):
        return precedenceOperationCrossover(p1, p2)
    else:
        return jobBasedCrossover(p1, p2)
#-----------------------------------------------------------------------------------------#
'''
ms的crossover
POC 和 JBC 隨機二選一
'''
def crossoverMS(p1, p2):
    return twoPointCrossover(p1, p2)
#-----------------------------------------------------------------------------------------#
'''
crossover生成染色體加入族群
'''
def getAppend(newPop, num, chromosome1, chromosome2):
    global exc

    if exc:
        newPop[num] = chromosome1
        newPop[num+1] = chromosome2
    else:
        newPop[num] = random.choice([chromosome1, chromosome2])
'''
crossover
'''
def crossover(parentPop):
    global exc
    exc = True
    
    crossNum = parameters.popSize - math.ceil(parameters.popSize * parameters.pe)

    newPop = np.zeros((crossNum,2,parentPop.shape[2]), dtype=int)
    
    tmp = np.arange(parentPop.shape[0])
    idx = 0
    for i in range(math.ceil(crossNum/2)):
        if (i+1) == math.ceil(crossNum/2) and crossNum%2 != 0  :
            exc = False
        num = np.random.choice(tmp, size=2, replace=False)
        OS1, MS1 = parentPop[num[0]]
        OS2, MS2 = parentPop[num[1]]
        if random.random() < parameters.pc:
            oOS1, oOS2 = crossoverOS(OS1, OS2)
            oMS1, oMS2 = crossoverMS(MS1, MS2)
            getAppend(newPop, idx, np.stack((oOS1, oMS1)), np.stack((oOS2, oMS2)))
        else:
            getAppend(newPop, idx, np.stack((OS1, MS1)), np.stack((OS2, MS2)))
        idx += 2

    return newPop