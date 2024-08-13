import random
from setting import parameters, globals
import math
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
        return random.sample(jobsRange, sizeJobset1)
    elif num == 2:
        jobset1 = random.sample(jobsRange, sizeJobset1)
        return jobset1, [item for item in jobsRange if item not in jobset1]
    else:
        print('plz give crossover parameter 1 or 2')
#-----------------------------------------------------------------------------------------#
'''
OS的POC，crossover方法
'''
def precedenceOperationCrossover(p1, p2):
    
    jobset1 = generateCrossoverSet(1)

    o1 = []
    p1kept = []
    for i in range(len(p1)):
        gene = p1[i]
        if gene in jobset1:
            o1.append(gene)
        else:
            o1.append(-1)
            p1kept.append(gene)
    o2 = []
    p2kept = []
    for i in range(len(p2)):
        gene = p2[i]
        if gene in jobset1:
            o2.append(gene)
        else:
            o2.append(-1)
            p2kept.append(gene)

    for i in range(len(o1)):
        if o1[i] == -1:
            o1[i] = p2kept.pop(0)
    for i in range(len(o2)):
        if o2[i] == -1:
            o2[i] = p1kept.pop(0)
    return (o1, o2)
'''
OS的JBC，crossover方法
'''
def jobBasedCrossover(p1, p2):

    jobset1, jobset2 = generateCrossoverSet(2)

    o1 = []
    p1kept = []
    for i in range(len(p1)):
        gene = p1[i]
        if gene in jobset1:
            o1.append(gene)
            p1kept.append(gene)
        else:
            o1.append(-1)
    o2 = []
    p2kept = []
    for i in range(len(p2)):
        gene = p2[i]
        if gene in jobset2:
            o2.append(gene)
            p2kept.append(gene)
        else:
            o2.append(-1)
    for i in range(len(o1)):
        if o1[i] == -1:
            o1[i] = p2kept.pop(0)
    for i in range(len(o2)):
        if o2[i] == -1:
            o2[i] = p1kept.pop(0)
    return (o1, o2)
#-----------------------------------------------------------------------------------------#
'''
MS的POC，crossover方法
'''
def precedenceOperationCrossover2(p1, p2):
    
    jobset1 = generateCrossoverSet(1)

    o1 = []
    p1kept = []
    for i in range(len(p1)):
        jb = globals.order_content['msTable'][f'{str(i)}'][0]
        gene = p1[i]
        if jb in jobset1:
            o1.append(gene)
        else:
            o1.append(-1)
            p1kept.append(gene)
    o2 = []
    p2kept = []
    for i in range(len(p2)):
        jb = globals.order_content['msTable'][f'{str(i)}'][0]
        gene = p2[i]
        if jb in jobset1:
            o2.append(gene)
        else:
            o2.append(-1)
            p2kept.append(gene)

    for i in range(len(o1)):
        if o1[i] == -1:
            o1[i] = p2kept.pop(0)
    for i in range(len(o2)):
        if o2[i] == -1:
            o2[i] = p1kept.pop(0)
    return (o1, o2)
'''
MS的JBC，crossover方法
'''
def jobBasedCrossover2(p1, p2):

    jobset1, jobset2 = generateCrossoverSet(2)

    o1 = []
    p1kept = []
    for i in range(len(p1)):
        jb = globals.order_content['msTable'][f'{str(i)}'][0]
        gene = p1[i]
        if jb in jobset1:
            o1.append(gene)
            p1kept.append(gene)
        else:
            o1.append(-1)
    o2 = []
    p2kept = []
    for i in range(len(p2)):
        jb = globals.order_content['msTable'][f'{str(i)}'][0]
        gene = p2[i]
        if jb in jobset2:
            o2.append(gene)
            p2kept.append(gene)
        else:
            o2.append(-1)
    for i in range(len(o1)):
        if o1[i] == -1:
            o1[i] = p2kept.pop(0)
    for i in range(len(o2)):
        if o2[i] == -1:
            o2[i] = p1kept.pop(0)
    return (o1, o2)
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
    if random.choice([True, False]):
        return precedenceOperationCrossover2(p1, p2)
    else:
        return jobBasedCrossover2(p1, p2)
#-----------------------------------------------------------------------------------------#
'''
crossover生成染色體加入族群
'''
def getAppend(newPop, crossNum, chromosome1, chromosome2):
    if (crossNum-len(newPop)) % 2 == 0:
        newPop.append(chromosome1)
        newPop.append(chromosome2)
    else:
        newPop.append(random.choice([chromosome1, chromosome2]))
'''
crossover
'''
def crossover(parentPop):

    newPop = []
    crossNum = parameters.popSize - math.ceil(parameters.popSize * parameters.pe)
    tmp = [x for x in range(len(parentPop))]

    for i in range(math.ceil(crossNum/2)):
        num = random.sample(tmp, 2)
        (OS1, MS1) = parentPop[num[0]]
        (OS2, MS2) = parentPop[num[1]]
        if random.random() < parameters.pc:
            (oOS1, oOS2) = crossoverOS(OS1, OS2)
            (oMS1, oMS2) = crossoverMS(MS1, MS2)
            getAppend(newPop, crossNum, (oOS1, oMS1), (oOS2, oMS2))
        else:
            getAppend(newPop, crossNum, (OS1, MS1), (OS2, MS2))

    return newPop

# '''
# 雙點crossover方式
# '''
# def twoPointCrossover(p1, p2):
#     pos1 = random.randint(0, len(p1) - 1)
#     pos2 = random.randint(0, len(p1) - 1)

#     if pos1 > pos2:
#         pos2, pos1 = pos1, pos2

#     offspring1 = p1
#     if pos1 != pos2:
#         offspring1 = p1[:pos1] + p2[pos1:pos2] + p1[pos2:]

#     offspring2 = p2
#     if pos1 != pos2:
#         offspring2 = p2[:pos1] + p1[pos1:pos2] + p2[pos2:]

#     return (offspring1, offspring2)