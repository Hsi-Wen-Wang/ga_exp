import csv
import random
import math
import shutil
import os
from itertools import combinations
from dataprocess import data_parameters, dirs_generate, data_paths
'''
複製 base 的 machine.json
原檔案在 setting 裡面
'''
def generateMachineSet():
    src = os.getcwd() + '/setting/machine.json'
    dst = data_paths.origin_path + 'machine.json'
    shutil.copyfile(src, dst)
    return
'''
生成 order
'''
def generateOrder(path, num_order):
    current_num = data_parameters.serial_num
    ordersList = []

    while current_num < num_order+data_parameters.serial_num:
        num_op = random.randint(5,6)
        operators = list(data_parameters.operatorDictA.keys())
        generateOp = sorted(random.sample(operators, num_op))
        orderList = [random.choice(data_parameters.Type), current_num]

        for op in generateOp:
            if orderList[0] == 'A':
                orderList.append(random.choice(data_parameters.operatorDictA[op]))
            elif orderList[0] == 'B':
                orderList.append(data_parameters.operatorDictB[op])
        ordersList.append(orderList)
        current_num+=1

    with open(path,'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(ordersList)
    return
'''
生成 orderSet
'''
def generateOrderSet(ord_path, set_path):
    with open(ord_path, 'r', newline='') as ord_file:
        orders = list(csv.reader(ord_file))
        multiple = math.ceil(len(orders)/5)
        increase_range = (1,1+multiple)
        orderSets = []

        for order in orders:
            order_num = len(order) - 2
            money_num = random.randint(data_parameters.moneyRange[str(order_num)][0], data_parameters.moneyRange[str(order_num)][1])
            money = data_parameters.baseMoney * money_num
            baseTime = 0
            orderSet = [order[0], order[1]]
            for content in order:
                if content in data_parameters.processTime.keys():
                    baseTime += int(data_parameters.processTime[content])

            orderSet.append(round(baseTime * random.uniform(increase_range[0], increase_range[1])))
            orderSet.append(money)
            orderSet.append(int(money * 0.1))
            orderSets.append(orderSet)
    with open(set_path, 'w', newline='')as setfile:
        writer = csv.writer(setfile)
        writer.writerows(orderSets)

    return orderSets
'''
生成 order weight
'''
def generateOrderWeight(order_path, weight_path, ins=False):
    if ins:
        with open(order_path, 'r',newline='') as ord_file:
            orders = list(csv.reader(ord_file))
            number = len(orders)
        with open(weight_path, 'w', newline='') as w_file:
            writer = csv.writer(w_file)
            weight = ['{:.2f}'.format(random.random()) for _ in range(number)]
            writer.writerow(weight)
    else:
        with open(order_path, 'r',newline='') as ord_file:
            orders = list(csv.reader(ord_file))
            number = len(orders)
        with open(weight_path, 'w', newline='') as w_file:
            writer = csv.writer(w_file)
            weight = [0 for _ in range(number)]
            writer.writerow(weight)
'''
生成初始的 插單檔案名稱
ex. 插入3單則檔案名稱為 1-2-3
        4              1-2-3-4
'''
def generateOriginInsertName(insert_num):
    for i in range(insert_num):
        if i == 0:
            insert_name = str(i+1)
        else:
            insert_name+=('-'+str(i+1))
    return insert_name
'''
生成插單資料夾
'''
def generateInsertDirs():
    insert_name_list = []
    insert_name = data_paths.insert_filename.split('-')
    for i in range(len(insert_name)+1):
        combine = list(combinations(insert_name,i))
        for name in combine:
            tmp_name = "-".join(name)
            insert_name_list.append(tmp_name)

    for name in insert_name_list:
        if name:
            insert_dirpath = data_paths.insert_path + f'insert_{name}'
            if not os.path.isdir(insert_dirpath):
                os.makedirs(insert_dirpath)
        else:
            name = '0'
            insert_dirpath = data_paths.insert_path + f'insert_{name}'
            if not os.path.isdir(insert_dirpath):
                os.makedirs(insert_dirpath)
            with open(insert_dirpath + '/insert_order.csv', 'w',newline='') as f:
                pass
            with open(insert_dirpath + '/insert_orderSet.csv', 'w',newline='') as f:
                pass
            with open(insert_dirpath + '/insert_orderWeight.csv', 'w',newline='') as f:
                pass

    return insert_name_list
'''
生成插單排列組合
'''
def generateCombineOrder(insert_name_list):
    insert_name_list.pop(0)
    init_path = data_paths.insert_path + f'insert_{insert_name_list[-1]}/'
    begin_ins_path = init_path + 'insert_order.csv'
    begin_ins_setpath = init_path + 'insert_orderSet.csv'
    begin_ins_wpath = init_path + 'insert_orderWeight.csv'
    
    with open(begin_ins_path, 'r',newline='')as ins_file:
        ins_file_rows = list(csv.reader(ins_file))

    with open(begin_ins_setpath, 'r',newline='')as ins_setfile:
        ins_setfile_rows = list(csv.reader(ins_setfile))

    with open(begin_ins_wpath, 'r',newline='')as ins_wfile:
        ins_wfile_rows = list(csv.reader(ins_wfile))
    
    for i, name in enumerate(insert_name_list):
        if i == (len(insert_name_list)-1):
            break

        insert_dir = data_paths.insert_path + f'insert_{name}/'

        ins_path = insert_dir + 'insert_order.csv'
        ins_setpath = insert_dir + 'insert_orderSet.csv'
        ins_wpath = insert_dir + 'insert_orderWeight.csv'


        if len(name) == 1:
            generateFile(ins_path, name, ins_file_rows)
            generateFile(ins_setpath, name, ins_setfile_rows)
            generateInsertWeight(ins_wpath, name, ins_wfile_rows[0])
        else:
            num_list= name.split('-')
            
            generateFile(ins_path, num_list, ins_file_rows)
            generateFile(ins_setpath, num_list, ins_setfile_rows)
            generateInsertWeight(ins_wpath, num_list, ins_wfile_rows[0])
    return
'''
生成各種組合的檔案(order, orderSet)
'''
def generateFile(path, num_list, rows):
    with open(path, 'w', newline='') as combinefile:
        writer = csv.writer(combinefile)
        for order_num in num_list:
            writer.writerow(rows[int(order_num)-1])
    return
'''
生成各種組合的權重(weight)
'''
def generateInsertWeight(path, num_list, rows):
    with open(path, 'w', newline='') as combinefile:
        writer = csv.writer(combinefile)
        weight = []
        for order_num in num_list:
            weight.append(rows[int(order_num)-1])
        writer.writerow(weight)
    return
'''
生成資料主程式:
輸入 : 生成訂單數量 、 生成插單數量
'''
def generateData(generate_ordnum, generate_insnum):
    # 建立訂單資料夾
    dirs_generate.generateExpDirs()
    generateMachineSet()
    # 生成訂單
    generateOrder(data_paths.ori_ordpath, generate_ordnum)
    # 生成訂單設定
    generateOrderSet(data_paths.ori_ordpath, data_paths.ori_setpath)
    # 生成訂單權重
    generateOrderWeight(data_paths.ori_ordpath, data_paths.ori_wpath)

    # 生成插單的排列組合的所有組合表
    insert_name_list = generateInsertDirs()
    # 訂單起始編號更新
    data_parameters.serial_num += generate_ordnum
    # 生成訂單
    generateOrder(data_paths.ori_ins_ordpath, generate_insnum)
    # 生成訂單設定
    generateOrderSet(data_paths.ori_ins_ordpath, data_paths.ori_ins_setpath)
    # 生成訂單權重
    generateOrderWeight(data_paths.ori_ins_ordpath, data_paths.ori_ins_wpath, True)

    # 生成排列組合
    generateCombineOrder(insert_name_list)

    return insert_name_list