import csv
import json
from setting import parameters, globals, paths
import numpy as np
###########################################################################################
##################################一般GA交叉，螺絲加工廠#####################################
###########################################################################################

'''
dictionary記錄
工單總數(totaljobs)         : 工單總數
工序總數(totaloperators)    : 工法總數
每個job的工序總數(operators) : 每個訂單的工法總數
類型(type)                  : ex. ['A']or['B']
工序對應的型號(operator)     : ex. 'op1':110, 'op2':120, ...
msTable                     : 染色體位置 '0':工序(1,1)  工序(1,1):染色體的位置'0'
'''
def parser(path):
    order = open(path, 'r', newline='')
    orderRow = list(csv.reader(order))

    orderDict = {'totalJobs':len(orderRow)}

    jobDict = {}
    mcDict = {}
    amount = []
    theore_value = np.zeros(len(orderRow), dtype=int)
    countStart = 0
    countEnd = 0

    for i,row in enumerate(orderRow):
        jobload = len(row)-2
        countEnd+=jobload
        jobTempDict = {}
        jobTempDict = {'operators':jobload}
        num = 1
        msTempDict = {}
        for x in range(countStart,countEnd):
            msTempDict[f'{x}'] = (i+1,num)
            msTempDict[(i+1,num)] = x
            num+=1
        countStart+=jobload
        jobTempDict['type'] = orderRow[i][0]
        amount.append(jobload)
        opDict = {}
        for j,column in enumerate(orderRow[i]):
            if j+2 < len(orderRow[i]):
                theore_value[i] += globals.processMethodTime[row[j+2]]
                opDict[f'op{j+1}'] = row[j+2]
            else:
                break

        jobTempDict['operator'] = opDict
        mcDict.update(msTempDict)
        jobFinalDict = {f'job{i+1}': jobTempDict}
        jobDict.update(jobFinalDict)
    orderDict['totalOperators'] = sum(amount)
    orderDict['jobs'] = jobDict
    orderDict['msTable'] = mcDict
    order.close()

    return orderDict, theore_value
#-----------------------------------------------------------------------------------------#
'''
生成訂單設定檔 :
截止日期
利潤
延誤罰金
'''
def orderInfo(path):
    order_setting = open(path, 'r', newline='')
    setRow = list(csv.reader(order_setting))
    
    orderSetDict = {'totalJobs': len(setRow)}
    for i,row in enumerate(setRow):
        orderSetDict[f'job{i+1}'] = {'deadline':int(row[2]),'profit':int(row[3]),'delay':int(row[4])}
    order_setting.close()

    return orderSetDict
###########################################################################################
##################################插單GA解析，螺絲加工廠####################################
###########################################################################################

'''
原訂單設定檔 加入 新訂單的訂單設定檔
'''
def newAdditionOrderInfo():
    ori_order_setting = open(paths.data_origin_path + 'orderSet.csv', 'r', newline='')
    ori_setRow = list(csv.reader(ori_order_setting))

    insert_order_setting = open(paths.data_insert_path + f'insert_orderSet.csv', 'r')
    insert_setRow = list(csv.reader(insert_order_setting))

    new_setRow = ori_setRow + insert_setRow
    
    orderSetDict = {'totalJobs': len(new_setRow)}
    for i,row in enumerate(new_setRow):
        if i < len(ori_setRow):
            orderSetDict[f'job{i+1}'] = {'deadline':int(row[2])-parameters.insertTimePoint,'profit':int(row[3]),'delay':int(row[4])}
        else:
            orderSetDict[f'job{i+1}'] = {'deadline':int(row[2]),'profit':int(row[3]),'delay':int(row[4])}

    ori_order_setting.close()
    insert_order_setting.close()

    return orderSetDict
#-----------------------------------------------------------------------------------------#
'''
讀取最佳染色體資訊
json 轉換成 dictionary
'''
def getOriginalBest(path):
    with open(path, 'r') as f:
        ori_bestChromosome = json.load(fp=f)
    return ori_bestChromosome
#-----------------------------------------------------------------------------------------#
'''
生成原始訂單狀態 :
已完成
未完成
正在進行
'''
def generateJobStatus(ori_bestChromosome):
    machine_operation = ori_bestChromosome['machine_operation']
    finishedJob = []
    unfinishedJob = []
    ongoingJob = []
    for i,job in enumerate(machine_operation):
        if job:
            for op in job:
                begin = op[1]
                end = op[1] + op[2]
                if parameters.insertTimePoint < begin:
                    unfinishedJob.append(op[0])
                    # print('1')
                elif begin < parameters.insertTimePoint < end:
                    # print('2')
                    ongoingJob.append((op[0],i,(op[1]+op[2])-parameters.insertTimePoint))
                else:
                    # print('3')
                    finishedJob.append(op[0])
                    
    return sortedJob(finishedJob, ongoingJob, unfinishedJob)
#-----------------------------------------------------------------------------------------#
'''
根據訂單編號由小到大 重新排列訂單
'''
def sortedJob(finishedJob, ongoingJob, unfinishedJob):
    finished = sorted(finishedJob, key=lambda job:job[1:])
    ongoing = sorted(ongoingJob, key=lambda job:job[1:])
    unfinished = sorted(unfinishedJob, key=lambda job:job[1:])
    
    return finished, ongoing, unfinished
#-----------------------------------------------------------------------------------------#
'''
更新訂單資訊
'''
def reverseOriginOrderContent():
    
    for job in globals.finishedJob:
        jobnum, opnum = job.split(',')
        jobnum = jobnum[1:]

        del globals.order_content['jobs'][f'job{jobnum}']['operator'][f'op{opnum}']
        
        globals.order_content['totalOperators']-=1
        globals.order_content['jobs'][f'job{jobnum}']['operators']-=1
    for job in globals.ongoingJob:
        jobnum, opnum = job[0].split(',')
        jobnum = jobnum[1:]

        globals.backup_dict[job[0]] = \
        globals.order_content['jobs'][f'job{jobnum}']['operator'][f'op{opnum}']

        del globals.order_content['jobs'][f'job{jobnum}']['operator'][f'op{opnum}']

        globals.order_content['totalOperators']-=1
        globals.order_content['jobs'][f'job{jobnum}']['operators']-=1
#-----------------------------------------------------------------------------------------#
'''
插單訂單解析 :
更新原來的訂單資訊(order content)
新增訂單的最佳理想完成時間(theoretical value)
'''
#-----------------------------------------------------------------------------------------#
def insertParser(insert_path):
    globals.calculateInsertOrderEffect()

    reverseOriginOrderContent()
    # print(globals.backup_dict.items())
    ori_orderNum = globals.order_content['totalJobs']

    order = open(insert_path, 'r', newline='')
    orderRow = list(csv.reader(order))

    globals.order_content['totalJobs']+=len(orderRow)

    del globals.order_content['msTable']

    amount = 0
    countStart = 0
    countEnd = len(globals.unfinishedJob)
    ms_temp_dict = {}
    theore_value = [0 for _ in range(len(orderRow))]

    for job in globals.unfinishedJob:
        jobnum, opnum = job.split(',')
        jobnum = int(jobnum[1:])
        opnum = int(opnum)
        ms_temp_dict[f'{countStart}'] = (jobnum, opnum)
        ms_temp_dict[jobnum, opnum] = countStart
        countStart+=1
    globals.order_content['msTable'] = ms_temp_dict

    for i,row in enumerate(orderRow):
        jobload = len(row)-2
        countEnd+=jobload
        jobTempDict = {}
        jobTempDict = {'operators':jobload}

        num = 1
        msTempDict = {}

        for x in range(countStart,countEnd):
            msTempDict[f'{x}'] = (ori_orderNum+1,num)
            msTempDict[(ori_orderNum+1,num)] = x
            num+=1

        countStart+=jobload
        jobTempDict['type'] = orderRow[i][0]
        amount+=jobload
        opDict = {}

        for j,column in enumerate(orderRow[i]):
            if j+2 < len(orderRow[i]):
                theore_value[i] += globals.processMethodTime[row[j+2]]
                opDict[f'op{j+1}'] = row[j+2]

        jobTempDict['operator'] = opDict
        globals.order_content['jobs'][f'job{ori_orderNum+1}'] = jobTempDict
        globals.order_content['msTable'].update(msTempDict)
        ori_orderNum+=1
    globals.theoretical_value += theore_value
    globals.order_content['totalOperators'] += amount
    order.close()

    return