import json
for i in range(1, 31):
    with open('lcation'+str(i), 'r') as f:
        data = json.load(f)
    newData= {}
    for SSID, BSSIDs in data.items():
        for BSSID, signal in BSSIDs.items():
            signal = int(signal[:-1])
            a = BSSID[:-1]
            if a not in newData:
                newData[a] = (signal, 1)
            else:
                oldSinal, oldNum =  newData[a]
                newNum = 1 + oldNum
                newData[a]  = (int(signal/newNum + oldSinal*(1-1/newNum)), newNum)

    factor = sum([_[0] for _ in newData.values()])
    newData['--factor--'] = factor 
    with open('new'+str(i), 'w') as f:
        json.dump(newData, f, indent = 4)
    
    

    
    
    
    