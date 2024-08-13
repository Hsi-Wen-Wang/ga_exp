from setting import parameters
'''
終止條件:
1. 迭代次數達成
2. 收斂
'''
def shouldTerminate(population, gen):
    if gen == 1:
        return gen > parameters.maxGen
    if parameters.convergence or gen > parameters.maxGen:
        return True
    else:
        return gen > parameters.maxGen