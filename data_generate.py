from setting import *
from src import *
import sys
from dataprocess import *


if __name__ == '__main__':
    # argv : 實驗資料夾名 生成訂單數量 生成插單數量

    # 實驗編號
    exp_num = sys.argv[1]
    # 生成訂單數量
    order_num = int(sys.argv[2])
    # 生成插單數量
    insert_num = int(sys.argv[3])

    # 初始化 path
    data_paths.initializeGeneratePaths(exp_num, insert_num)
    # 生成資料集
    data_generate.generateData(order_num, insert_num)
    # 生成 output 資料夾
    dirs_generate.generateResultDir()
    
    