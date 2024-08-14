from setting import parameters, globals
from src.ga.codec import decoding
import numpy as np
###########################################################################################
################################一般GA適應性函數，螺絲加工廠#################################
###########################################################################################
'''
計算所有訂單完工時間
'''
def timeFitness(machine_operation):
    max_per_machine = []
    for mc in machine_operation:
        max_d = 0
        for job in mc:
            end = job[1]+job[2]
            if end > max_d:
                max_d = end
        max_per_machine.append(max_d)

    return max(max_per_machine)
#-----------------------------------------------------------------------------------------#
'''
計算機器運行成本
'''
def mcCostFitness(machine_operation):
    lenght = len(machine_operation)
    cost_per_machine = np.zeros(lenght, dtype=float)
    standby_per_machine = np.zeros(lenght, dtype=float)
    for i,job in enumerate(machine_operation):
        if job:
            start = job[0][1]
            end = job[-1][1]+job[-1][2]
            duration = 0
            for op in job:
                duration+=op[2]
                mc_cost = op[2] * globals.machine_config[f'Machine{i+1}']['cost']
                cost_per_machine[i]+=mc_cost
            standby_per_machine[i]+=((end-start-duration)*globals.machine_config[f'Machine{i+1}']['cost']*0.1)

    return np.sum(cost_per_machine + standby_per_machine)
#-----------------------------------------------------------------------------------------#
'''
計算訂單利潤
'''
def earnFitness():
    proFit = 0
    globals.completeness = np.zeros(globals.order_content['totalJobs'], dtype=bool)
    for i,t in enumerate(globals.job_finished_time):
        # print(t)
        if t <= globals.order_setting[f'job{i+1}']['deadline']:
            proFit += globals.order_setting[f'job{i+1}']['profit']
            globals.completeness[i] = True
        else:
            proFit += globals.order_setting[f'job{i+1}']['delay']
            globals.completeness[i] = False

    return proFit
#-----------------------------------------------------------------------------------------#
'''
單條染色體的fitness計算
'''
def singleChromosomeFitnessCalculate(os_ms):
    (os, ms) = os_ms
    if parameters.insertMode:
        addreplace_machine_operation, globals.job_finished_time = decoding.insertDecode(os, ms)
    else:
        addreplace_machine_operation, globals.job_finished_time = decoding.decode(os, ms)
    timeFit = timeFitness(addreplace_machine_operation)
    mcCostFit = mcCostFitness(addreplace_machine_operation)
    proFit = earnFitness()

    return timeFit, mcCostFit, proFit
#-----------------------------------------------------------------------------------------#
def singleChromosomeWeightedFitnessCalculate(os_ms):
    os, ms = os_ms
    if parameters.insertMode:
        addreplace_machine_operation, globals.job_finished_time = decoding.insertDecode(os, ms)
    else:
        addreplace_machine_operation, globals.job_finished_time = decoding.decode(os, ms)
    timeFit = timeFitness(addreplace_machine_operation)
    mcCostFit = mcCostFitness(addreplace_machine_operation)
    proFit = earnFitness()
    timeWeightFit = recalculateTimeFitness(1/timeFit)
    proWeightFit = recalculateProfitFitness(proFit)
    
    return timeWeightFit, mcCostFit, proWeightFit

#-----------------------------------------------------------------------------------------#
'''
正規化
'''
def normalize(data):
    data = ((data-np.min(data))/(np.max(data)-np.min(data)))
    data[np.isnan(data)] = 0
    return data
#-----------------------------------------------------------------------------------------#
'''
fitness進行正規化
'''
def normalizeFitness(timeAry, costAry, proFitAry):
    timeAry = normalize(timeAry)
    costAry = normalize(costAry)
    proFitAry = normalize(proFitAry)

    return timeAry, costAry, proFitAry
#-----------------------------------------------------------------------------------------#
'''
fitness進行訂單權重的計算
fitness取越大越好，因此 時間 與 機器成本 進行倒數
'''
def fitnessProcess(population):
    timeAry = np.zeros(parameters.popSize, dtype=float)
    costAry = np.zeros(parameters.popSize, dtype=float)
    proFitAry = np.zeros(parameters.popSize, dtype=float)
    for i, chromosome in enumerate(population):
        timeAry[i], costAry[i], proFitAry[i] = singleChromosomeWeightedFitnessCalculate(chromosome)

    return timeAry, costAry, proFitAry
#-----------------------------------------------------------------------------------------#
'''
完工時間加上訂單權重的計算
result =  sum(fitness * w_i * (理想時間_i/實際時間_i))
i = 訂單編號
'''
def recalculateTimeFitness(timeFit):
    weight_timeFit = 0
    for i,value in enumerate(globals.weight):
        if value == 0:
            continue
        if globals.completeness[i]:
            weight_timeFit += (timeFit * globals.weight[i] * (globals.theoretical_value[i] / globals.job_finished_time[i])
)
    timeFit+=weight_timeFit
    return timeFit
#-----------------------------------------------------------------------------------------#
'''
完工時間加上訂單權重的計算
result = profit_i * w_i
i = 訂單編號
'''
def recalculateProfitFitness(proFit):
    weight_proFit = 0   
    for i, value in enumerate(globals.weight):
        if value == 0:
            continue
        if globals.completeness[i]:
            weight_proFit += (globals.order_setting[f'job{i+1}']['profit'] * globals.weight[i])
    return proFit
#-----------------------------------------------------------------------------------------#
'''
總 fitness 計算
a1 : 時間
a2 : 機器成本
a3 : 利潤
'''
def fitnessCalculate(population):
    fitness = np.zeros(parameters.popSize, dtype=float)
    timeAry, costAry, proFitAry = fitnessProcess(population)
    timeAry, costAry, proFitAry = normalizeFitness(timeAry, costAry, proFitAry)
    for i in range(parameters.popSize):
        fitness[i] = (parameters.a1*timeAry[i] + parameters.a2*costAry[i] + parameters.a3*proFitAry[i])
    return fitness

