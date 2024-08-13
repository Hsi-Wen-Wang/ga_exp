import json
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
    sort_fitness = sorted(range(len(fitness)), key=lambda k : fitness[k], reverse=True)
    timeFit, mcCostFit, proFit = singleChromosomeFitnessCalculate(population[sort_fitness[0]])
    w_timeFit, _, w_proFit = singleChromosomeWeightedFitnessCalculate(population[sort_fitness[0]])
    bestChromosome['OS'] = population[sort_fitness[0]][0]
    bestChromosome['MS'] = population[sort_fitness[0]][1]
    bestChromosome['fitness'] = fitness[sort_fitness[0]]
    bestChromosome['timeCost'] = timeFit
    bestChromosome['mcCost'] = mcCostFit
    bestChromosome['profit'] = proFit
    bestChromosome['w_timeCost'] = w_timeFit
    bestChromosome['w_proFit'] = w_proFit
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
    sort_fitness = sorted(range(len(fitness)), key=lambda k : fitness[k], reverse=True)
    # print(fitness[sort_fitness[0]])
    if fitness[sort_fitness[0]] >= bestChromosome['fitness']:
        # print('hi')
        timeFit, mcCostFit, proFit = singleChromosomeFitnessCalculate(population[sort_fitness[0]])
        w_timeFit, _, w_proFit = singleChromosomeWeightedFitnessCalculate(population[sort_fitness[0]])
        bestChromosome['OS'] = population[sort_fitness[0]][0]
        bestChromosome['MS'] = population[sort_fitness[0]][1]
        bestChromosome['fitness'] = fitness[sort_fitness[0]]
        bestChromosome['timeCost'] = timeFit
        bestChromosome['mcCost'] = mcCostFit
        bestChromosome['profit'] = proFit
        bestChromosome['w_timeCost'] = w_timeFit
        bestChromosome['w_proFit'] = w_proFit
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