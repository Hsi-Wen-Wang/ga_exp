import random
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

    if pos1 == pos2:
        return p

    if pos1 > pos2:
        pos1, pos2 = pos2, pos1

    offspring = p[:pos1] + [p[pos2]] + \
          p[pos1+1:pos2] + [p[pos1]] + \
          p[pos2+1:]
    return offspring
#-----------------------------------------------------------------------------------------#
'''
os
多點突變
多點進行交換
'''
def multiPointSwappingMutation(p):
    points = random.randint(0, len(p))
    mutateRange = range(0, len(p))
    listSwapPointIndex = random.sample(mutateRange, points)
    swapValueList = []
    offspring = []
    for i in listSwapPointIndex:
        swapValueList.append(p[i])
    # random.shuffle(swapValueList)
    for i in range(len(p)):
        if i in listSwapPointIndex:
            offspring.append(swapValueList.pop())
        else:
            offspring.append(p[i])

    return offspring
#-----------------------------------------------------------------------------------------#
'''
多點突變
多點的機器進行隨機變換
'''
def multiPointMutation(p):
    offspring = []
    points = random.randint(0, len(p))
    mutateRange = range(0, len(p))
    listPointIndex = random.sample(mutateRange, points)
    # count = 0
    # temp = globals.order_content['msTable']['0'][0]
    for i in range(len(p)):
        if i in listPointIndex:
                presentJob = globals.order_content['msTable'][f'{i}'][0]
                presentOp = globals.order_content['msTable'][f'{i}'][1]

                jobInfo = [globals.order_content['jobs'][f'job{presentJob}']['type'], \
                           
                           globals.order_content['jobs'][f'job{presentJob}']['operator'][f'op{presentOp}']]
                offspring.append(randMachine(jobInfo))
        else:
            offspring.append(p[i])
            
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
    newPop = []

    for i,(OS, MS) in enumerate(population):
        if random.random() < parameters.pm:
            oOS = mutationOS(OS)
            oMS = mutationMS(MS)
            newPop.append((oOS, oMS))
        else:
            newPop.append((OS, MS))

    return newPop