import os
from dataprocess import data_paths
'''
建立資料夾
實驗的外層資料夾
mode = 0, 建立data資料夾
./data/exp1/origin/ and ./data/exp1/insert/
or
mode = 1, 建立result資料夾
./result/exp1
'''
def generateExpDirs(mode=0):
    if mode == 0:
        if not os.path.isdir(data_paths.data_exp_path):
            os.makedirs(data_paths.data_exp_path)
        if not os.path.isdir(data_paths.origin_path):
            os.makedirs(data_paths.origin_path)
        if not os.path.isdir(data_paths.insert_path):
            os.makedirs(data_paths.insert_path)
    elif mode == 1:
        if not os.path.isdir(data_paths.result_exp_path):
            os.makedirs(data_paths.result_exp_path)
        if not os.path.isdir(data_paths.result_ori_path):
            os.makedirs(data_paths.result_ori_path)
        if not os.path.isdir(data_paths.result_ins_path):
            os.makedirs(data_paths.result_ins_path)
        if not os.path.isdir(data_paths.result_exp_path+'/theBest'):
            os.makedirs(data_paths.result_exp_path+'/theBest')
    else:
        print('mode num is 0 or 1!!')
    return
'''
輸出所有資料夾名稱
'''
def getDirsNames():
    insDirNames = []
    path_info = next(os.walk(data_paths.insert_path))
    insDirNames = path_info[1]

    return insDirNames
'''
生成輸出資料夾(內部)
'''
def generateResultStorage(path_name=0, ins = False):
    if ins:
        path = data_paths.result_ins_path + path_name + '/'
    else:
        path = data_paths.result_ori_path

    if not os.path.isdir(path):
        os.makedirs(path)

    if not os.path.isdir(path+'recordbest'):
        os.makedirs(path+'recordbest')

    if not os.path.isdir(path+'/recordbest/bestchromosome'):
        os.makedirs(path+'/recordbest/bestchromosome')
    if not os.path.isdir(path+'/recordbest/bestrecord'):
        os.makedirs(path+'/recordbest/bestrecord')

    if not os.path.isdir(path+'gantt'):
        os.makedirs(path+'gantt')

    if not os.path.isdir(path+'lineChart'):
        os.makedirs(path+'lineChart')

    if not os.path.isdir(path+'lineChart/fitness/'):
        os.makedirs(path+'lineChart/fitness/')
    if not os.path.isdir(path+'lineChart/mcCost/'):
        os.makedirs(path+'lineChart/mcCost/')
    if not os.path.isdir(path+'lineChart/profit/'):
        os.makedirs(path+'lineChart/profit/')
    if not os.path.isdir(path+'lineChart/timeCost/'):
        os.makedirs(path+'lineChart/timeCost/')
    return
'''
生成輸出資料夾(外層)
'''
def generateResultDir():
    generateExpDirs(1)
    insDirNames = getDirsNames()
    generateResultStorage()
    for dirName in insDirNames:
        ins_path = dirName
        generateResultStorage(ins_path, True)
    return
