import json
from setting import globals,paths
'''
json 生成機器設定(machine config)
'''
def MachineSetDict(path):
    jsonFile = open(path)
    machine_config = json.load(jsonFile)
    jsonFile.close()
    return machine_config

'''
插單初始化機器設定
生成新的機器設定 json 檔案
'''
def initializeMachineSet():
    mc_path = paths.data_origin_path + 'machine.json'
    globals.machine_config = MachineSetDict(mc_path)
    for job in globals.ongoingJob:
        mc_num = int(job[1]) + 1
        globals.machine_config[f'Machine{mc_num}']['current_time'] = job[2]
    newpath = paths.data_exp_insert_path + 'insert_machine.json'
    generateMachineJson(newpath)
    return
'''
生成 json 設定檔案
'''
def generateMachineJson(path):
    jsonfile = open(path, 'w')
    json.dump(globals.machine_config, jsonfile, indent=4)
    jsonfile.close