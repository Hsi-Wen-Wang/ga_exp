import json
import numpy as np
from src.ga.operation.fitness import singleChromosomeFitnessCalculate, singleChromosomeWeightedFitnessCalculate
###########################################################################################
##############################一般GA最佳紀錄，螺絲加工廠#####################################
###########################################################################################
'''
初始化歷代最佳解
紀錄內容 :
OS MS    : 染色體
fitness  : 適應值
timeCost : 完工時間
mcCost   : 機器成本
profit   : 利潤
'''
def initializeKeepBest(population, fitness, bestChromosome):
    idx = np.argmax(fitness)
    timeFit, mcCostFit, proFit = singleChromosomeFitnessCalculate(population[idx])
    w_timeFit, _, w_proFit = singleChromosomeWeightedFitnessCalculate(population[idx])
    bestChromosome['OS'] = population[idx][0]
    bestChromosome['MS'] = population[idx][1]
    bestChromosome['fitness'] = float(fitness[idx])
    bestChromosome['timeCost'] = int(timeFit)
    bestChromosome['mcCost'] = float(mcCostFit)
    bestChromosome['profit'] = int(proFit)
    bestChromosome['w_timeCost'] = float(w_timeFit)
    bestChromosome['w_proFit'] = int(w_proFit)
#-----------------------------------------------------------------------------------------#
'''
最佳解比較，大於等於則更新
紀錄內容 :
OS MS    : 染色體
fitness  : 適應值
timeCost : 完工時間
mcCost   : 機器成本
profit   : 利潤
'''
def keepBest(population, fitness, bestChromosome):
    idx = np.argmax(fitness)
    if fitness[idx] >= bestChromosome['fitness']:
        timeFit, mcCostFit, proFit = singleChromosomeFitnessCalculate(population[idx])
        w_timeFit, _, w_proFit = singleChromosomeWeightedFitnessCalculate(population[idx])
        bestChromosome['OS'] = population[idx][0]
        bestChromosome['MS'] = population[idx][1]
        bestChromosome['fitness'] = float(fitness[idx])
        bestChromosome['timeCost'] = int(timeFit)
        bestChromosome['mcCost'] = float(mcCostFit)
        bestChromosome['profit'] = int(proFit)
        bestChromosome['w_timeCost'] = float(w_timeFit)
        bestChromosome['w_proFit'] = int(w_proFit)
#-----------------------------------------------------------------------------------------#
'''
迭代過程記錄，為了生成迭代圖
紀錄內容 :
fitness  : 適應值
timeCost : 完工時間
mcCost   : 機器成本
profit   : 利潤
'''
def recordingProcess(recordForm, bestChromosome):
    recordForm['fitness'].append(bestChromosome['fitness'])
    recordForm['timeCost'].append(bestChromosome['timeCost'])
    recordForm['mcCost'].append(bestChromosome['mcCost'])
    recordForm['profit'].append(bestChromosome['profit'])
#-----------------------------------------------------------------------------------------#
'''
將結果輸出成 json 檔案
'''
def record2json(record, path):
    with open(path, 'w') as f:
        json.dump(record, f, indent=4)

def default_dump(obj):
    if isinstance(obj, (np.integer, np.floating, np.bool_)):
        return obj.item()
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj