import sys

def generateScripts(exp_num, exp_times):
    with open(f'./scripts/0{exp_num}_exp.bat', 'w', newline='') as f:
        for i in range(exp_times):
            f.write(f'python .\main.py exp{exp_num} 0 {i+1}')
            f.write('\n')
        f.write(f'python .\chooseTheBest.py exp{exp_num} 1')
        f.write('\n')
        f.write(f'python .\generate_insertjson.py exp{exp_num}')
        f.write('\n')
        for i in range(exp_times):
            f.write(f'python .\main.py exp{exp_num} 1 {i+1}')
            f.write('\n')
        f.write(f'python .\chooseTheBest.py exp{exp_num} 2')
        f.write('\n')
        f.write(f'python .\chooseTheBest.py exp{exp_num} 3')
    return

if __name__ == '__main__':
    # argv : 實驗編號(1)、實驗重複次數(10)
    exp_num = sys.argv[1]
    exp_times = int(sys.argv[2])
    generateScripts(exp_num, exp_times)