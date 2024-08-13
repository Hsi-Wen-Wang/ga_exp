import random
from setting import parameters, globals,testing
import sys
###########################################################################################
##################################一般GA編碼，螺絲加工廠#####################################
###########################################################################################
'''
生成 os 染色體
訂單處理順序
'''
def generateOS():
    if testing.randomswitch:
        random.seed(testing.randomseed)
    OS = []
    for i, jobKey in enumerate(globals.order_content['jobs'].keys()):
        osTemp = [i+1]
        osTemp *= globals.order_content['jobs'][jobKey]['operators']
        OS+=osTemp
    random.shuffle(OS)
    return OS
#-----------------------------------------------------------------------------------------#
'''
生成 ms 染色體
加工機器選擇
'''
def generateMS():
    MS = []
    total_num = globals.order_content['totalOperators']

    for i in range(total_num):
        jobInfo = []
        job = globals.order_content['msTable'][f'{i}']
        jobInfo.append(globals.order_content['jobs'][f'job{job[0]}']['type'])
        jobInfo.append(globals.order_content['jobs'][f'job{job[0]}']['operator'][f'op{job[1]}'])
        MS.append(randMachine(jobInfo))

    return MS

#-----------------------------------------------------------------------------------------#
'''
randmachine:
輸入 jobInfo 
['type', '工法']
輸出 machine: int
'''
def randMachine(jobInfo):
    machineList = []
    machine = 0
    if testing.randomswitch:
        random.seed(testing.randomseed)
    for i, machineName in enumerate(globals.machine_config.keys()):
        for setting in globals.machine_config[machineName]['setting']:
            if globals.machine_config[machineName]['status']:
                if jobInfo[0] in setting['type'] and jobInfo[1] == setting['process']:
                    machineList.append(i+1)
                    continue
    if not machineList:
        print('random machine has no match machine')
        sys.exit(-1)
    else:
        machine = random.choice(machineList)

    return machine
#-----------------------------------------------------------------------------------------#
'''
生成染色體(chromosome)直到族群(population)總數
'''
def initializePopulation():
    population = []
    for i in range(parameters.popSize):
        OS = generateOS()
        MS = generateMS()
        population.append((OS, MS))
    return population
