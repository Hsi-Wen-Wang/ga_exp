import time
import sys
import numpy as np
from setting import *
from src import *
from dataprocess.findThebest import getDirsname

def main():
    bestChromosome = {}
    recordForm = {'fitness':[], 'timeCost':[], 'mcCost':[], 'profit':[]}

    convergence_record = 0
    gen = 1
    num = 0

    globals.initializeSetting()
    population = ga.encoding.initializePopulation()
    
    while not ga.operation.termination.shouldTerminate(population, gen):
        fitness = ga.fitness.fitnessCalculate(population)

        if gen == 1:
            ga.keep.initializeKeepBest(population, fitness, bestChromosome)
            ga.keep.recordingProcess(recordForm, bestChromosome)

            convergence_record = bestChromosome['fitness']

        else:
            ga.keep.keepBest(population, fitness, bestChromosome)
            ga.keep.recordingProcess(recordForm, bestChromosome)
            
            if abs(convergence_record - bestChromosome['fitness']) < parameters.convergence_rate:
                num+=1
            else:
                num = 0
            convergence_record = bestChromosome['fitness']

        selectPop, parentPop= ga.select.select(population, fitness)

        crossPop = ga.crossover.crossover(parentPop)

        population = np.vstack((selectPop , crossPop), dtype=int)

        population = ga.mutation.mutation(population)

        if num >= parameters.convergence_num:
            parameters.convergence = True

        fit = bestChromosome['fitness']
        timefit = bestChromosome['timeCost']
        profit = bestChromosome['profit']
        mcfit = bestChromosome['mcCost']
        print(f'iteration : {gen}, best fitness : {fit}, minimum work time : {timefit}, maximum profit : {profit}, minimum mcCost : {mcfit}')
        gen += 1       
  
    fitness = ga.fitness.fitnessCalculate(population)

    ga.keep.keepBest(population, fitness, bestChromosome)
    ga.keep.recordingProcess(recordForm, bestChromosome)

    add_mcop,job_finished_time = ga.decoding.decode(bestChromosome['OS'], bestChromosome['MS'])

    bestChromosome['machine_operation'] = add_mcop
    data = ga.decoding.translateDecode2Gantt(add_mcop)

    utils.chart.drawChart(data, recordForm)
    serial_number = paths.num_exp.zfill(2)
    if testing.recordWrite:
        bestChromosome['OS'] = bestChromosome['OS'].tolist()
        bestChromosome['MS'] = bestChromosome['MS'].tolist()
        ga.keep.record2json(bestChromosome, paths.result_origin_path + f'recordbest/bestchromosome/bestchromosome_{serial_number}.json')
        ga.keep.record2json(recordForm, paths.result_origin_path + f'recordbest/bestrecord/bestrecord_{serial_number}.json')
    
    return bestChromosome,gen

def insert_main():
    parameters.insertMode = True
    globals.reInitializeSetting()
    population = ga.encoding.initializePopulation()

    bestChromosome = {}
    recordForm = {'fitness':[], 'timeCost':[], 'mcCost':[], 'profit':[]}

    convergence_record = 0
    gen = 1
    num = 0

    while not ga.termination.shouldTerminate(population, gen):
        fitness = ga.fitness.fitnessCalculate(population)

        if gen == 1:
            ga.keep.initializeKeepBest(population, fitness, bestChromosome)
            ga.keep.recordingProcess(recordForm, bestChromosome)
            
            convergence_record = bestChromosome['fitness']
            # recordForm

        else:
            ga.keep.keepBest(population, fitness, bestChromosome)
            ga.keep.recordingProcess(recordForm, bestChromosome)
            if convergence_record + parameters.convergence_rate == bestChromosome['fitness'] or \
               convergence_record - parameters.convergence_rate == bestChromosome['fitness']:
                convergence_record = bestChromosome['fitness']
                num+=1
            else:
                num = 0

        selectPop, parentPop= ga.select.select(population, fitness)

        crossPop = ga.crossover.crossover(parentPop)

        population = np.vstack((selectPop , crossPop), dtype=int)

        population = ga.mutation.mutation(population)

        if num >= parameters.convergence_num:
            parameters.convergence = True

        fit = bestChromosome['fitness']
        timefit = bestChromosome['timeCost']
        profit = bestChromosome['profit']
        mcfit = bestChromosome['mcCost']
        print(f'iteration : {gen}, best fitness : {fit}, minimum work time : {timefit}, maximum profit : {profit}, minimum mcCost : {mcfit}')
        gen += 1

    fitness = ga.fitness.fitnessCalculate(population)
    ga.keep.keepBest(population, fitness, bestChromosome)
    ga.keep.recordingProcess(recordForm, bestChromosome)

    add_mcop,job_finished_time = ga.decoding.insertDecode(bestChromosome['OS'], bestChromosome['MS'])

    bestChromosome['machine_operation'] = add_mcop

    data = ga.decoding.translateDecode2Gantt(add_mcop)
    utils.chart.drawChart(data, recordForm)
    serial_number = paths.num_exp.zfill(2)
    if testing.recordWrite:
        bestChromosome['OS'] = bestChromosome['OS'].tolist()
        bestChromosome['MS'] = bestChromosome['MS'].tolist()
        ga.keep.record2json(bestChromosome, paths.result_insert_path + f'recordbest/bestchromosome/insert_bestchromosome_{serial_number}.json')
        ga.keep.record2json(bestChromosome, paths.result_insert_path + f'recordbest/bestrecord/insert_bestrecord_{serial_number}.json')

    return bestChromosome,gen


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("plz enter experiment number!!!")
    else:
        # argv : 實驗編號(exp1)、模式(1 or 2)、實驗第幾次的編號(1)
        # 模式 1 為一般排程、 模式 2 為插單排程
        exp_num = sys.argv[1]
        num_mode = int(sys.argv[2])
        numbers_exp = sys.argv[3]

        if num_mode == 0:
            paths.initializePaths(exp_num, numbers_exp)

            t0 = time.time()
            best,gen = main() 
            t1 = time.time()
            total_time = t1 - t0
            fitness = best['fitness']
            print(f'execution time : {total_time}, total iteration : {gen}, best fitness : {fitness}')
            print('Sucess')
            
        elif num_mode == 1:
            paths.initializePaths(exp_num, numbers_exp)
            dirsnames = getDirsname(paths.data_exp_insert_path)
            for i,dirname in enumerate(dirsnames):
                paths.initializeInsertPaths(exp_num, dirname)

                t0 = time.time()
                best,gen = insert_main() 
                t1 = time.time()
                total_time = t1 - t0
                fitness = best['fitness']
                print(f'execution time : {total_time}, total iteration : {gen}, best fitness : {fitness}')
                print('Sucess')
        else:
            print('Error input number!! First input number must be 0 or 1!!')
       