import sys
from setting import *
from src import *

if __name__ == "__main__":
    # argv : 實驗編號(exp1)
    exp_num = sys.argv[1]
    paths.initializePaths(exp_num)
    globals.calculateInsertOrderEffect()
    utils.mcParser.initializeMachineSet()