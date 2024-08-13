import os
input_path = os.getcwd() + '/data/'
output_path = os.getcwd() + '/result/'
input_origin_path = ''
input_insert_path = ''
num_exp = 0
insert_num = 0

def initializePaths(exp_num, numbers_exp=0):
    global data_path
    global result_path
    global data_exp_path
    global data_exp_insert_path

    global data_origin_path
    global result_origin_path

    global num_exp
    num_exp = numbers_exp
    data_path = os.getcwd() + '/data/'
    result_path = os.getcwd() + '/result/'

    data_exp_path = data_path + f'{exp_num}/'

    data_exp_insert_path = data_path+f'{exp_num}/insert/'


    data_origin_path = data_path + f'{exp_num}/origin/'
    result_origin_path = result_path + f'{exp_num}/origin/'

def initializeInsertPaths(exp_num, dirname):
    global data_path
    global result_path
    global result_insert_path
    global data_insert
    # global num_exp
    global data_insert_path
    global insert_name

    insert_name = dirname

    data_insert = data_exp_path+'insert/'

    data_insert_path = data_exp_insert_path + f'{insert_name}/'
    result_insert_path = result_path + f'{exp_num}/insert/{insert_name}/'





