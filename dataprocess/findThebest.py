import pandas as pd
import shutil
import os
import json
from setting import parameters
from dataprocess import data_paths

'''
mode 1:
篩選 origin 的最佳解
mode 2:
篩選 insert 的最佳解
mode 3:
篩選 the best 的最佳解
-------------------
功能 :
讀取 bestchromosome.json 建立 dataFrame
'''
def readRecord(filename):
    record = []
    for name in filename:
        if data_paths.mode == 1:
            with open(data_paths.record_ori_path + name, 'r', newline='') as file:
                dt = json.load(file)
                del dt['OS'], dt['MS'], dt['machine_operation']
                record.append(dt)
        elif data_paths.mode == 2:
            with open(data_paths.record_ins_path + name, 'r', newline='') as file:
                dt = json.load(file)
                del dt['OS'], dt['MS'], dt['machine_operation']
                record.append(dt)
        elif data_paths.mode == 3:
            with open(data_paths.record_thebest_path + name, 'r', newline='') as file:
                dt = json.load(file)
                del dt['OS'], dt['MS'], dt['machine_operation']
                record.append(dt)
        else:
            print('[ERROR] error mode number! mode num is 1 to 3!')
    record_df = pd.DataFrame(record)
    return record_df
'''
取得目錄下所有檔案的名稱，包含副檔名
ex. bestchromosome.json
'''
def getFilename(path):
    filename = os.listdir(path)
    return filename
'''
取得目錄下所有目錄名稱
os.walk()回傳的第二個為 dirsname
需轉換成list, next為下一層(同時會轉換成list)
'''
def getDirsname(path):
    result = next(os.walk(path))
    return result[1]
'''
正規化資料
'''
def normalize(data):
    maximum = data.max()
    minimum = data.min()

    if maximum == minimum:
        return 0
    else:
        return ((data - minimum)/(maximum - minimum))
'''
計算 fitness 加權
'''   
def calculateFitness(record_df):
    return parameters.a1 * record_df['w_timeCost'] + parameters.a2 * record_df['mcCost'] + parameters.a3 * record_df['w_proFit']
'''
重新計算fitness
'''
def calculateNewFitness(record_df):
    record_df['w_timeCost'] = normalize(record_df['w_timeCost'])
    record_df['mcCost'] = normalize(record_df['mcCost'])
    record_df['w_proFit'] = normalize(record_df['w_proFit'])

    record_df['fitness'] = calculateFitness(record_df)

    return record_df.loc[:,'fitness'].idxmax()
'''
選擇最佳解 main
'''
def chooseBest(path):
    filename = getFilename(path)
    record_df = readRecord(filename)
    best_idx = calculateNewFitness(record_df)
    return best_idx
'''
移動最佳解到目標資料夾
'''
def movetheBestResultToData(chrom_num, insert_name=0):
    serial_num = str((chrom_num + 1)).zfill(2)
    if data_paths.mode == 1:
        src = data_paths.record_ori_path + f'bestchromosome_{serial_num}.json'
        dst = data_paths.origin_path + 'bestrecord.json'        
    elif data_paths.mode == 2:
        src = data_paths.record_ins_path + f'insert_bestchromosome_{serial_num}.json'
        dst = data_paths.record_thebest_path + f'{data_paths.ins_name}_bestchromosome_{serial_num}.json'        
    elif data_paths.mode == 3:
        src = data_paths.record_thebest_path + insert_name
        dst = data_paths.record_thebest_path + f'thebest_{insert_name}'       
    else:
        print('mode numbers is 1 to 3 !!')

    shutil.copyfile(src, dst)
    return
