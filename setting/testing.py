randomswitch = False
randomseed = 10
imageShow = False
imageWirte = True
recordWrite = True
debugFlag = 0
'''
print flag:

debugFlag = 3: print population
debugFlag = 4: print crossover
debugFlag = 5: print fitness
debugFlag = 6: print keep
debugFlag = 7: print mutation
debugFlag = 8: print select
debugFlag = 9: print mcParser
debugFlag = 10: print parser
'''
def flag(message,num):
    # 全都不print
    if debugFlag == 0:
        return
    
    # print 所有
    elif debugFlag==1:
        print(message)
        
    # print fitness
    elif debugFlag==2 and num==2:
        print(message)

    elif debugFlag==3 and num==3:
        print(message)

    elif debugFlag==4 and num==4:
        print(message)

    elif debugFlag==5 and num==5:
        print(message)

    elif debugFlag==6 and num==6:
        print(message)

    elif debugFlag==7 and num==7:
        print(message)

    elif debugFlag==8 and num==8:
        print(message)

    elif debugFlag==9 and num==9:
        print(message)

    elif debugFlag==10 and num==10:
        print(message)

    else:
        return
    return
