from src import *
import json
import csv
from setting import parameters, paths
'''
一般排程初始化:
load 工法處理時間
load 訂單權重
ordercontent 訂單資訊, theoretical value 理想最佳值
ordersetting 訂單設定, machine config 機器設定
'''
def initializeSetting():
    global order_content
    global order_setting
    global machine_config
    global theoretical_value
    global processMethodTime
    global weight
    global completeness

    completeness = 0
    loadProcessMethodTime()
    loadOrderWeight()
    order_content, theoretical_value = utils.parser.parser(paths.data_origin_path + 'order.csv')
    order_setting = utils.parser.orderInfo(paths.data_origin_path + 'orderSet.csv')
    machine_config = utils.mcParser.MachineSetDict(paths.data_origin_path + 'machine.json')
#-----------------------------------------------------------------------------------------#
'''
插單排程初始化:
load 工法處理時間
load 訂單權重
ordercontent 訂單資訊, 先由讀取原始訂單建立模板， 再由讀取插單對原模板進行更新
theoretical value 理想最佳值
ordersetting 訂單設定, machine config 機器設定
'''
def reInitializeSetting():
    global finishedJob
    global ongoingJob
    global unfinishedJob
    global ori_bestChromosome
    global order_content
    global order_setting
    global machine_config
    global backup_dict
    global theoretical_value
    global processMethodTime
    global job_finished_time
    global weight
    global completeness

    completeness = 0
    job_finished_time = 0
    backup_dict={}
    loadProcessMethodTime()
    loadOrderWeight()
    utils.parser.insertParser(paths.data_insert_path + 'insert_order.csv')
    order_setting = utils.parser.newAdditionOrderInfo()
    machine_config = utils.mcParser.MachineSetDict(paths.data_insert + 'insert_machine.json')
#-----------------------------------------------------------------------------------------#
'''
計算插單後，原排程計畫中被影響的部分進行修正
生成完成的訂單、未完成的訂單、正在進行的訂單
'''
def calculateInsertOrderEffect():
    global finishedJob
    global ongoingJob
    global unfinishedJob
    global ori_bestChromosome
    global order_content
    global order_setting
    global machine_config
    global backup_dict
    global theoretical_value
    global processMethodTime
    global weight
    loadProcessMethodTime()
    order_content, theoretical_value = utils.parser.parser(paths.data_origin_path + 'order.csv')
    ori_bestChromosome = utils.parser.getOriginalBest(paths.data_origin_path +'bestrecord.json')
    finishedJob, ongoingJob, unfinishedJob = utils.parser.generateJobStatus(ori_bestChromosome)
#-----------------------------------------------------------------------------------------#
'''
讀取工法耗時表
'''
def loadProcessMethodTime():
    global processMethodTime

    jsonFile = open('./setting/processMethodTime.json')
    processMethodTime = json.load(jsonFile)
    jsonFile.close()
#-----------------------------------------------------------------------------------------#
'''
讀取訂單權重
'''
def loadOrderWeight():
    global weight

    with open(paths.data_origin_path + 'orderWeight.csv') as f:
        weight = []
        value_list = list(csv.reader(f))
        for value in value_list[0]:
            weight.append(float(value))
    if parameters.insertMode:
        with open(paths.data_insert_path + 'insert_orderWeight.csv') as file:
            weight = []
            value_list = list(csv.reader(file))
            if value_list:
                for value in value_list[0]:
                    weight.append(float(value))
            else:
                return
    return

