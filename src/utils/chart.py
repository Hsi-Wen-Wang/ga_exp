import random
import numpy as np
import matplotlib.pyplot as plt
import json
from setting import testing, parameters,paths
import os

'''
隨機生成顏色
'''
def randColor():
    return ["#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)])]
#-----------------------------------------------------------------------------------------#
'''
繪製折線圖
輸入 data :
每次迭代的數值
由 ga.keep.recordingProcess 生成
'''
def drawLineChart(data):
    serial_number = paths.num_exp.zfill(2)

    fig1 = plt.figure(figsize=(20, 8))
    ax = fig1.add_subplot(111)
    fitnessX = [i for i in range(len(data['fitness']))]
    fitnessY = data['fitness']
    plt.plot(fitnessX, fitnessY, color = 'red', label='fitness plot')
    plt.xlabel('iteration', fontsize = '10')
    plt.ylabel('fitness', fontsize = '10')
    plt.title('fitness')

    if testing.imageWirte:
        if not parameters.insertMode:
            plt.savefig(paths.result_origin_path+f'lineChart/fitness/fitnessLine_{serial_number}.png')
        else:
            plt.savefig(paths.result_insert_path+f'lineChart/fitness/fitnessLine_{serial_number}.png')
    if testing.imageShow:
        plt.show()
    plt.close()

    fig2 = plt.figure(figsize=(20, 8))
    ax = fig2.add_subplot(111)
    timeCostX = [i for i in range(len(data['timeCost']))]
    timeCostY = data['timeCost']
    plt.plot(timeCostX, timeCostY, color = 'red', label='timeCost plot')
    plt.xlabel('iteration', fontsize = '10')
    plt.ylabel('timeCost', fontsize = '10')
    plt.title('timeCost')
    if testing.imageWirte:
        if not parameters.insertMode:
            plt.savefig(paths.result_origin_path +f'lineChart/timeCost/timecostLine_{serial_number}.png')
        else:
            plt.savefig(paths.result_insert_path +f'lineChart/timeCost/timecostLine_{serial_number}.png')
    if testing.imageShow:
        plt.show()
    plt.close()

    fig3 = plt.figure(figsize=(20, 8))
    ax = fig3.add_subplot(111)
    mcCostX = [i for i in range(len(data['mcCost']))]
    mcCostY = data['mcCost']
    plt.plot(mcCostX, mcCostY, color = 'red', label='mcCost plot')
    plt.xlabel('iteration', fontsize = '10')
    plt.ylabel('mcCost', fontsize = '10')
    plt.title('mcCost')

    if testing.imageWirte:
        if not parameters.insertMode:
            plt.savefig(paths.result_origin_path +f'lineChart/mcCost/mccostLine_{serial_number}.png')
        else:
            plt.savefig(paths.result_insert_path +f'lineChart/mcCost/mccostLine_{serial_number}.png')
    if testing.imageShow:
        plt.show()
    plt.close()

    fig4 = plt.figure(figsize=(20, 8))
    ax = fig4.add_subplot(111)
    profitX = [i for i in range(len(data['profit']))]
    profitY = data['profit']
    plt.plot(profitX, profitY, color = 'red', label='profit plot')
    plt.xlabel('iteration', fontsize = '10')
    plt.ylabel('profit', fontsize = '10')
    plt.title('profit')

    if testing.imageWirte:
        if not parameters.insertMode:
            plt.savefig(paths.result_origin_path +f'lineChart/profit/profitLine_{serial_number}.png')
        else:
            plt.savefig(paths.result_insert_path +f'lineChart/profit/profitLine_{serial_number}.png')
    if testing.imageShow:
        plt.show()
    plt.close()
    return
#-----------------------------------------------------------------------------------------#
'''
繪製甘特圖
data :
machine operation 機器處理流程
由 ga.decoding.translateDecode2Gantt 生成
'''
def drawGanttChart(data, color_dict):
    serial_number = paths.num_exp.zfill(2)
    nb_row = len(data.keys())
    pos = np.arange(0.5, nb_row * 0.5 + 0.5, 0.5)
    fig = plt.figure(figsize=(20, 8))
    ax = fig.add_subplot(111)

    index = 0
    max_len = []
    for machine, operations in data.items():

        for op in operations:
            jobTemp, opTemp = op[2].split(',')
            job = jobTemp[1:]

            c = color_dict.setdefault(f'{job}', randColor())

            max_len.append(op[1])
            rect = ax.barh((index * 0.5) + 0.5, op[1] - op[0], left=op[0], height=0.3, align='center',
                           edgecolor=c, color=c, alpha=0.8)

            # adding label
            width = int(rect[0].get_width())
            Str = "{}".format(op[2])
            xloc = op[0] + 0.50 * width
            clr = 'black'
            align = 'center'

            yloc = rect[0].get_y() + rect[0].get_height() / 2.0
            ax.text(xloc, yloc, Str, horizontalalignment=align,
                            verticalalignment=align, color=clr, weight='bold',
                            clip_on=True, fontsize='xx-small')
        index += 1

    ax.set_ylim(ymin=-0.1, ymax=nb_row * 0.5 + 0.5)
    ax.grid(color='gray', linestyle=':')
    ax.set_xlim(0, max(10, max(max_len)))

    labelsx = ax.get_xticklabels()
    plt.setp(labelsx, rotation=0, fontsize=10)

    locsy, labelsy = plt.yticks(pos, data.keys())
    plt.setp(labelsy, fontsize=14)

    ax.invert_yaxis()

    plt.title("Solution")

    if testing.imageWirte:
        if not parameters.insertMode:
            plt.savefig(paths.result_origin_path +f'gantt/gantt_{serial_number}.png')
        else:
            plt.savefig(paths.result_insert_path +f'gantt/gantt_{serial_number}.png')
    if testing.imageShow:
        plt.show()
    plt.close()
    
    return color_dict
#-----------------------------------------------------------------------------------------#
'''
繪圖
判斷顏色表是否有建立，甘特圖的工作顏色會相同
'''
def drawChart(data, record):
    if os.path.isfile(paths.data_exp_path+'/GanttChart_color.json'):
        is_file_num = 2
    else:
        is_file_num = 1

    if is_file_num == 1:
        color_dict = {}
        color_dict = drawGanttChart(data, color_dict)
        colorfile = open(paths.data_exp_path+'/GanttChart_color.json', 'w')
        json.dump(color_dict, colorfile, indent=4)
        colorfile.close

        drawLineChart(record)

    elif is_file_num == 2:
        colorfile = open(paths.data_exp_path+'/GanttChart_color.json','r')

        color_dict = json.load(colorfile)
        colorfile.close()

        color_dict = drawGanttChart(data, color_dict)

        colorfile = open(paths.data_exp_path+'/GanttChart_color.json','w')
        json.dump(color_dict, colorfile, indent=4)
        colorfile.close

        drawLineChart(record)

    return
