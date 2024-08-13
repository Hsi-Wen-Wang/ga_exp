from setting import parameters,globals
from setting import globals
import sys
import copy
###########################################################################################
##################################一般GA解碼，螺絲加工廠#####################################
###########################################################################################
'''
生成初始化的工作流程列表:
current opList ex. [1 2 1 4 3]
訂單1進行到op1, 訂單2進行到op2, 訂單3進行到op1...
'''
def generateCurrentOpList():
    current_opList = []
    for job in globals.order_content['jobs'].keys():
        if globals.order_content['jobs'][job]['operators'] != 0:
            for op in globals.order_content['jobs'][job]['operator'].keys():
                current_opList.append(int(op[2:]))
                break
        else:
            current_opList.append(0)
            continue
    return current_opList
#-----------------------------------------------------------------------------------------#
'''
processing_seq格式:
(job number, operation number, process machine)
(  訂單編號       工法編號          處理機器    )
'''
def decodeChrom2Seq(os, ms):
    processing_seq = []
    current_op = generateCurrentOpList()

    for job in os:
        current_operation = (job, current_op[job-1])
        ms_index = globals.order_content['msTable'][current_operation]
        machine_used = ms[ms_index]
        processing_seq.append((job,current_op[job-1],machine_used))
        current_op[job-1]+=1

    return processing_seq
#-----------------------------------------------------------------------------------------#
'''
mcProcessTable格式:
[['machine1'-(job, operation), (job, operation)...], ['machine2'-...]...]
每台機器所要處理的任務
'''
def decode2mcTable(processing_seq):
    mcProcessTable = [[] for _ in range(len(globals.machine_config.keys()))]
    # print(len(globals.machine_config.keys()))
    for deChrom in processing_seq:
        mcProcessTable[deChrom[2]-1].append((deChrom[0], deChrom[1]))

    return mcProcessTable
#-----------------------------------------------------------------------------------------#
'''
取得工法在機器上的處理時間
輸入:
op:(job number, operation number)、 machine:第幾台
            tuple                         int
'''
def getProcessingTime(op, machine):
    # print(globals.order_content)

    # print('=======')
    # print(machine)
    # print('++++++')
    # print(op)
    # print('-----')
    for info in globals.machine_config[f'Machine{machine}']['setting']:
        # print(globals.order_content['jobs'][f'job{op[0]}']['operator'][f'op{op[1]}'])
        # print(info)
        # print('-=-=-=-=-=-=-=-')
        if globals.order_content['jobs'][f'job{op[0]}']['operator'][f'op{op[1]}'] in info.values():
            prcTime = info['time']
            return prcTime
    print("[ERROR] Machine {} doesn't to be able to process this task.{}".format(machine,info))
    sys.exit(-1)
#-----------------------------------------------------------------------------------------#
'''
輸入機器處理順序表
輸出的data格式:
'machine name':[[[start time, end time, operation], [...]], [[...], [...]],....]
                      int       int     ex.(O1,1)tuple
'''
def translateDecode2Gantt(machine_operation):
    data = {}
    # print('1111111')
    # print(machine_operation)
    for idx, machine in enumerate(machine_operation):
        machine_name = "Machine-{}".format(idx + 1)
        operations = []
        for operation in machine:
            # print(operation[0])
            operations.append([operation[1], operation[1]+operation[2], operation[0]])
        data[machine_name] = operations
    # print(data)
    return data

#-----------------------------------------------------------------------------------------#
'''
初始化 current operation, job current time:
輸出 replace current_operation格式:
[current op, current mc]
'''
def resetJobSetting(replace=False):
    if parameters.insertMode:
        job_current_time = [0 for _ in range(globals.order_content['totalJobs'])]
        current_operation = generateCurrentOpList()
        for job in globals.ongoingJob:
            jobnum, opnum = job[0].split(',')
            job_current_time[int(jobnum[1:])-1] = job[2]
        if replace:
            for i, crop in enumerate(current_operation):
                current_operation[i] = [crop,0]
            return current_operation, job_current_time
        else:
            return current_operation, job_current_time
    else:
        job_current_time = [0 for _ in range(globals.order_content['totalJobs'])]
        current_operation = generateCurrentOpList()
        if replace:
            for i, crop in enumerate(current_operation):
                current_operation[i] = [crop,0]
            return current_operation, job_current_time
        else:
            return current_operation, job_current_time
'''
初始化 machine operation, machine current time, current operation
輸出 replace machine_operation格式:
[current machine time, current job]
'''
def resetMachineSetting(temp_mcop=0, current_operation=0, replace=False):
    machine_operation = [[] for _ in range(len(globals.machine_config.keys()))]
    if not replace:
        machine_current_time = [globals.machine_config[x]['current_time'] for x in globals.machine_config.keys()]
        return machine_operation, machine_current_time
    
    if parameters.insertMode:
        machine_current_time = [[globals.machine_config[x]['current_time'], 0] for x in globals.machine_config.keys()]
        for job in globals.ongoingJob:
            machine_current_time[job[1]-1][0] = job[2]
            machine_current_time[job[1]-1][1] = job[0]
    else:    
        machine_current_time = [[globals.machine_config[x]['current_time'], 0] for x in globals.machine_config.keys()]
    for i, job in enumerate(temp_mcop):
        if job:
            if not machine_current_time[i][1] == 0:
                continue
            machine_current_time[i][1] = job[0][0]
            for op in job:
                current_jobnum, current_opnum = op[0].split(',')
                if current_opnum == '1':
                    current_operation[int(current_jobnum[1:])-1][1] = i
    return machine_operation, machine_current_time, current_operation
#-----------------------------------------------------------------------------------------#
'''
machine_operation格式:
[[(operation, start time, prctime), (...), ...]. [(...), (...)], ...]
ex.('O1,1', int開始時間, int處理時間)
尚未加上換線時間
'''
def initialDecode(os, ms):
    current_operation, job_current_time = resetJobSetting()
    machine_operation, machine_current_time = resetMachineSetting()
    
    processing_seq = decodeChrom2Seq(os, ms)
    mcProcessTable = decode2mcTable(processing_seq)

    execution = True    
    while execution:
        for i,job in enumerate(mcProcessTable):
            if job:
                for op in job:
                    if op[1] == current_operation[op[0]-1]:

                        name_stack = f'O{op[0]},{op[1]}'
                        startTime = max(job_current_time[op[0]-1], machine_current_time[i])
                        prcTime = getProcessingTime(op, i+1)

                        machine_operation[i].append((name_stack, startTime, prcTime))

                        current_operation[op[0]-1] += 1
                        machine_current_time[i] = (startTime + prcTime)
                        job_current_time[op[0]-1] = (startTime + prcTime)
                        job.pop(0)

                        break
                    else:
                        break
        if not any(mcProcessTable):
            execution = False

    return machine_operation
#-----------------------------------------------------------------------------------------#
'''
解碼並加上換線時間
'''
def decode(os, ms):
    ori_machine_operation = initialDecode(os, ms)
    machine_operation, job_finished_time = addToolReplaceTime(ori_machine_operation)
    return machine_operation, job_finished_time
#-----------------------------------------------------------------------------------------#
'''
更新項目包含機器工作流程、機器完成當下作業時間、
當組作業的紀錄時間
'''
def informationSetting(new_data, start, duration, i, job_index):
    global add_machine_operation
    global add_machine_current_time
    global add_job_current_time

    add_machine_operation[i].append(new_data)
    add_machine_current_time[i][0] = start + duration
    add_job_current_time[job_index] = start + duration

    return
'''
判斷開始時間是否小於新的開始時間
小於則進行更新，否則不做變更
具體更新->informationSetting
'''
def uppdateSetting(new_start, start, new_data, ori_data, i, job_index):
    # global add_machine_operation
    # global add_machine_current_time
    # global add_job_current_time
    if start < new_start:        
        informationSetting(new_data, new_start, ori_data[2], i, job_index)
        return
    else:    
        informationSetting(ori_data, ori_data[1], ori_data[2], i, job_index)
        return
'''
判斷原有的初始時間要替換成何種新資訊
'''
def newStartTimeSetting(i, job_index, num):
    global add_machine_current_time
    global add_job_current_time

    newStartTime_mc_jobReplace = add_machine_current_time[i][0] + parameters.job_replace_time
    newStartTime_job_jobReplace = add_job_current_time[job_index] + parameters.job_replace_time
    newStartTime_mc_toolReplace = add_machine_current_time[i][0] + parameters.tool_replace_time
    newStartTime_job_toolReplace = add_job_current_time[job_index] + parameters.tool_replace_time

    if num == 1:
        return max(newStartTime_job_jobReplace, newStartTime_mc_jobReplace)
    elif num == 2:
        return max(newStartTime_job_toolReplace, newStartTime_mc_toolReplace)
    elif num == 3:
        return max(newStartTime_mc_jobReplace, newStartTime_job_jobReplace, newStartTime_mc_toolReplace, newStartTime_job_toolReplace)
    else:
        print('plz check the number!')
'''
在原有的機器作業流程中加入換線時間
'''
def addToolReplaceTime(ori_machine_operation):
    temp_mcop = copy.deepcopy(ori_machine_operation)
    global add_current_operation
    global add_job_current_time
    global add_machine_operation
    global add_machine_current_time
    
    add_current_operation, add_job_current_time = resetJobSetting(True)

    add_machine_operation, add_machine_current_time, add_current_operation = \
    resetMachineSetting(temp_mcop, add_current_operation, True)

    execution = True
    while execution:
        for i, job in enumerate(temp_mcop):
             if job:
                # temp_op = job[0]
                num = 0
                for j, op in enumerate(job):
                    current_jobnum, current_opnum = op[0].split(',')
                    job_index = int(current_jobnum[1:])-1

                    if not add_current_operation[job_index][0] == int(current_opnum):
                        break
                    tmp_jobnum, tmp_opnum = add_machine_current_time[i][1].split(',')
                    ori_data = temp_mcop[i][j]
                    start = op[1]
                    duration = op[2]
            
                    if start == globals.machine_config[f'Machine{i+1}']['current_time']:
                        if parameters.insertMode:
                            if add_machine_current_time[i][1] in globals.backup_dict:
                                previous = globals.backup_dict[add_machine_current_time[i][1]]
                                # print('???')  
                            else:
                                previous = globals.order_content['jobs'][f'job{tmp_jobnum[1:]}']['operator'][f'op{tmp_opnum}']
                            current = globals.order_content['jobs'][f'job{current_jobnum[1:]}']['operator'][f'op{current_opnum}']
                        
                            if previous == current:
                                # print('1')
                                new_start_time = newStartTimeSetting(i, job_index, 1)
                                new_data = (op[0], new_start_time, duration)

                                uppdateSetting(new_start_time, start, new_data, ori_data, i, job_index)

                            elif previous != current and\
                                add_current_operation[job_index][1] == i:
                                
                                new_start_time = newStartTimeSetting(i, job_index, 2)
                                new_data = (op[0], new_start_time, duration)

                                uppdateSetting(new_start_time, start, new_data, ori_data, i, job_index)

                            else:
                                new_start_time = newStartTimeSetting(i, job_index, 3)
                                new_data = (op[0], new_start_time, duration)

                                uppdateSetting(new_start_time, start, new_data, ori_data, i, job_index)

                        else:
                            informationSetting(ori_data, start, duration, i, job_index)
                       
                    else:
                        if parameters.insertMode:
                            if add_machine_current_time[i][1] in globals.backup_dict:
                                previous = globals.backup_dict[add_machine_current_time[i][1]]
                                # print('???')  
                            else:
                                previous = globals.order_content['jobs'][f'job{tmp_jobnum[1:]}']['operator'][f'op{tmp_opnum}']
                            current = globals.order_content['jobs'][f'job{current_jobnum[1:]}']['operator'][f'op{current_opnum}']
                        else:
                            previous = globals.order_content['jobs'][f'job{tmp_jobnum[1:]}']['operator'][f'op{tmp_opnum}']
                            current = globals.order_content['jobs'][f'job{current_jobnum[1:]}']['operator'][f'op{current_opnum}']
                        
                        if previous == current:
                            # print('1')
                            new_start_time = newStartTimeSetting(i, job_index, 1)
                            new_data = (op[0], new_start_time, duration)

                            uppdateSetting(new_start_time, start, new_data, ori_data, i, job_index)

                        elif previous != current and\
                            add_current_operation[job_index][1] == i:
                            
                            new_start_time = newStartTimeSetting(i, job_index, 2)
                            new_data = (op[0], new_start_time, duration)

                            uppdateSetting(new_start_time, start, new_data, ori_data, i, job_index)

                        else:
                            new_start_time = newStartTimeSetting(i, job_index, 3)
                            new_data = (op[0], new_start_time, duration)

                            uppdateSetting(new_start_time, start, new_data, ori_data, i, job_index)


                    add_machine_current_time[i][1] = op[0]
                    add_current_operation[job_index][0]+=1
                    add_current_operation[job_index][1] = i
                    num+=1

                del temp_mcop[i][:num]
                
        if not any(temp_mcop):
            execution = False
    # print(add_machine_operation)

    return add_machine_operation, add_job_current_time
#-----------------------------------------------------------------------------------------#
##################################插單GA解碼，螺絲加工廠#####################################
#-----------------------------------------------------------------------------------------#
'''
插單解碼
'''
def insertDecode(os, ms):
    ori_machine_operation = initialDecode(os, ms)
    replce_machine_operation, job_finished_time = addToolReplaceTime(ori_machine_operation)
    machine_operation = addOngoingJob(replce_machine_operation)
    return machine_operation, job_finished_time
#-----------------------------------------------------------------------------------------#
'''
將插單時間時，還在進行的工作加入機器的處理順序表
'''
def addOngoingJob(machine_operation):
    for job in globals.ongoingJob:
        machine_operation[job[1]-1].insert(0, (job[0], 0, job[2]))
    return machine_operation