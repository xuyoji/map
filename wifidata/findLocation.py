import json, os, heapq, math, random
n = 0

#-----------replace the line below to WHILE TRUE: to use online version----------
for name in range(1, 31): 
    
    #---------online version code------------
    '''
    name = input('please input current location\n')
    a = str(os.popen('netsh wlan show networks mode=bssid').readlines())
    a = '[' + str(a).replace('\'\\n\',', '],[') + ']'
    a =  eval(a.replace('\\n', ''))
    b = {}
    for j in range(1, len(a)):
        c = {}
        k = 0
        for i in range(0, len(a[j])-5, 6):
            if '%' in a[j][i+4-k][30:]:
                k+=1
            c[a[j][i+4-k][30:].replace(' ', '')] = a[j][i+5-k][30:-2]        
        b[a[j][0][9:]] = c
    with open('location' + name, 'w') as f:
        json.dump(b, f, indent = 4)        
    '''
    
    try: 
        with open('location'+str(name), 'r') as f:
            testData = json.load(f)
        valueList = [0 for i in range(30)]

        for i in range(1, 31):
            with open('new'+str(i), 'r') as f:
                data = json.load(f)
                newData= {}
            for SSID, BSSIDs in testData.items():
                for BSSID, signal in BSSIDs.items():
                    try:
                        signal = int(signal[:-1])
                        a = BSSID[:-1].replace(' ', '')
                        if a not in newData:
                            newData[a] = (signal, 1)
                        else:
                            oldSinal, oldNum =  newData[a]
                            newNum = 1 + oldNum
                            newData[a]  = (int(signal/newNum + oldSinal*(1-1/newNum)), newNum)
                    except:
                        pass
            
            factor1 = sum([_[0] for _ in newData.values()])
            factor2 = data['--factor--']
            maxTestData, secondTestData, thirdTestData = 0, 0, 0          
            maxTestNum, secondTestNum, thirdTestNum = 0, 0, 0             
            maxData, secondData, thirdData = 0, 0, 0             
            maxNum, secondNum, thirdNum = 0, 0, 0 
            for BSSID, signal in newData.items():
                if signal[0] > maxTestNum:
                    thirdTestData = secondTestData
                    thirdTestNum = secondTestNum
                    secondTestData = maxTestData
                    secondTestNum = maxTestNum
                    maxTestData = BSSID
                    maxTestNum = signal[0]
                if BSSID in data:
                    valueList[i - 1] += (signal[0] * data[BSSID][0] / (factor1 * factor2))**0.28
                #else:
                    #valueList[i - 1] -= ((signal[0] / factor1)  ** 0.5)
            for BSSID, signal in data.items():
                if BSSID != '--factor--':
                    if signal[0] > maxNum:
                        thirdData = secondData
                        thirdNum = secondNum
                        secondData = maxData
                        secondNum = maxNum
                        maxData = BSSID
                        maxNum = signal[0]
                    #else:
                    #    valueList[i - 1] -= ((signal[0] / factor2)  ** 0.5)
                    
            #if i in [15, 16]:
            #        print(i, '  ',maxData,  '  ',maxTestData)
            a = [maxData, secondData, thirdData]
            b = [maxTestData, secondTestData, thirdTestData]
            for _ in a:
                if _ in b:
                    valueList[i - 1] += (0.2 - 0.1 * abs(a.index(_) - b.index(_)))
                else:
                    valueList[i - 1] -= 0.025 * (3 - a.index(_))
            for _ in b:
                if _ not  in a:
                    valueList[i - 1] -= 0.025 * (3 - b.index(_))
            if a[:2] == b[:2]:
                temp = (maxNum / secondNum) / (maxTestNum / secondTestNum)
                if 0.6 <temp <1.67:
                    print('hit1!')
                    if temp > 1:
                        temp /= 1
                        valueList[i - 1] += 3**(temp-0.6) - 1
            if (a[0] == b[1] and a[1] ==b[0]):
                temp1 = secondTestNum/(maxTestNum+secondTestNum)
                temp2 = secondNum / (maxNum+ secondNum)
                if temp1 > 0.35 and temp2 > 0.35:
                    temp = min(temp1, temp2) / max(temp1, temp2)
                    if temp  > 0.6:
                        print('hit2!')
                        valueList[i - 1] += 3**(temp-0.6) - 1
        #print([int(i*10000) for i in valueList][14:16])
        result = valueList.index(max(valueList)) + 1
        secodResult = valueList.index(heapq.nlargest(2, valueList)[1]) + 1
        delta = (valueList[result - 1] - valueList[secodResult - 1]) * 10000
        print('result=%d, '%result, end = 'delta=%d,' %delta)
        if result == name:
            print(' valid!')
        else:
            print()
    except FileNotFoundError:
        pass

    

    
    
    
    