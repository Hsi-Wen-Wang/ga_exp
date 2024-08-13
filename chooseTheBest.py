import sys
from dataprocess import findThebest, data_paths

if __name__ == "__main__":
    # argv : 實驗編號(exp1)、模式選擇(1~3)
    # 1 : 選出一般排程最佳、 2 : 選出各個插單結果最佳、 3 : 選出所有插單結果最佳
    exp_num = sys.argv[1]
    data_paths.mode = int(sys.argv[2])

    if data_paths.mode == 1:
        data_paths.initializePaths(exp_num)
        best_num = findThebest.chooseBest(data_paths.record_ori_path)
        findThebest.movetheBestResultToData(best_num)
    elif data_paths.mode == 2:
        data_paths.initializePaths(exp_num)
        dirsName = findThebest.getDirsname(data_paths.insert_path)
        for name in dirsName:
            data_paths.initializePaths(exp_num, name)
            best_num = findThebest.chooseBest(data_paths.record_ins_path)
            findThebest.movetheBestResultToData(best_num, name)
    elif data_paths.mode == 3:
        data_paths.initializePaths(exp_num)
        filenames = findThebest.getFilename(data_paths.record_thebest_path)
        best_num = findThebest.chooseBest(data_paths.record_thebest_path)
        findThebest.movetheBestResultToData(best_num, filenames[best_num])
    else:
        print('mode numbers is 1 to 3 !!!')
