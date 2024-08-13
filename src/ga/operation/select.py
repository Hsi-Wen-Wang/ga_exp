from setting import parameters
import math
###########################################################################################
##################################一般GA選擇，螺絲加工廠#####################################
###########################################################################################
'''
菁英選擇
保留族群(population)前 1% 進入下一代
並加入交配池
'''
def eliteSelect(population, fitness):
    
    keptPopSize = math.ceil(parameters.pe * len(population))

    sort_fitness_index = sorted(range(len(fitness)), key=lambda k : fitness[k], reverse=True)

    newPop = [population[x] for x in sort_fitness_index[:keptPopSize]]

    return  newPop
#-----------------------------------------------------------------------------------------#
'''
競爭法:
兩兩比對
較好的一方進入交配池
'''
def competeSelect(population, fitness):
    newPop = []
    if len(population)%2 == 0:
        num = int(len(population))
        for i in range(0, num, 2):
            if fitness[i] > fitness[i+1]:
                newPop.append(population[i])
            else:
                newPop.append(population[i+1])
    else:
        num = int(len(population)-1)
        
        for i in range(0, num, 2):
            if fitness[i] > fitness[i+1]:
                newPop.append(population[i])
            else:
                newPop.append(population[i+1])
        newPop.append(population[-1])

    return newPop
#-----------------------------------------------------------------------------------------#
'''
透過菁英選擇與競爭法建立交配池
'''
def selectSpace(population, fitness):
    parentSpace = eliteSelect(population, fitness)
    parentSpace+=competeSelect(population, fitness)
    # print(parentSpace)
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
