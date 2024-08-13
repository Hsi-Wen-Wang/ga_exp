import os
from dataprocess import data_generate

data_path = os.getcwd() + '/data/'
result_path = os.getcwd() + '/result/'
mode = 0
if not os.path.isdir(data_path):
    os.makedirs(data_path)
if not os.path.isdir(result_path):
    os.makedirs(result_path)
'''
初始化路徑(一般)
'''
def initializeGeneratePaths(exp_num, generate_insnum):
    global origin_path
    global insert_path
    global data_exp_path
    global result_exp_path
    global ori_ordpath
    global ori_setpath
    global ori_wpath
    global ori_ins_ordpath
    global ori_ins_setpath
    global ori_ins_wpath
    global insert_filename
    global result_ori_path
    global result_ins_path
    
    data_exp_path = data_path + exp_num
    result_exp_path = result_path + exp_num
    # ./data/exp1/origin/
    origin_path = data_exp_path + '/origin/'
    # ./data/exp1/insert/
    insert_path = data_exp_path + '/insert/'

    result_ori_path = result_exp_path + '/origin/'
    result_ins_path = result_exp_path + '/insert/'

    # ./data/exp1/origin/order.csv
    ori_ordpath = origin_path + 'order.csv'
    # ./data/exp1/origin/orderSet.csv
    ori_setpath = origin_path + 'orderSet.csv'
    # ./data/exp1/origin/orderSet.csv
    ori_wpath   = origin_path + 'orderWeight.csv'

    # 1-2-3
    insert_filename = data_generate.generateOriginInsertName(generate_insnum)
    # ./data/exp1/insert/insert_1-2-3/insert_order.csv
    ori_ins_ordpath = insert_path + f'insert_{insert_filename}/insert_order.csv'
    # ./data/exp1/insert/insert_1-2-3/insert_orderSet.csv
    ori_ins_setpath = insert_path + f'insert_{insert_filename}/insert_orderSet.csv'
    # ./data/exp1/insert/insert_1-2-3/insert_orderWeight.csv
    ori_ins_wpath   = insert_path + f'insert_{insert_filename}/insert_orderWeight.csv'

    return
'''
初始化路徑(插單)
'''
def initializePaths(exp_num, insert_name='0'):
    global origin_path
    global insert_path
    global data_exp_path
    global result_exp_path
    global record_ori_path
    global record_ins_path
    global record_thebest_path
    global ins_name

    # ex. insert_0, insert_1
    ins_name = insert_name
    # ./data/exp
    data_exp_path = data_path + exp_num
    # ./result/exp
    result_exp_path = result_path + exp_num
    # ./data/exp1/origin/
    origin_path = data_exp_path + '/origin/'
    # ./data/exp1/insert/
    insert_path = data_exp_path + '/insert/'
    # ./result/exp/origint/recordbest/bestchromosome
    record_ori_path = result_exp_path + '/origin/recordbest/bestchromosome/'
    # ./result/exp/insert/insert_0/recordbest/bestchromosome
    record_ins_path = result_exp_path + f'/insert/{insert_name}/recordbest/bestchromosome/'
    # ./result/exp/theBest/
    record_thebest_path = result_exp_path + '/theBest/'

    return