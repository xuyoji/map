import os, json
while True:
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
    with open('lcation' + name, 'w') as f:
        json.dump(b, f, indent = 4)
        print('location'+name+' is done')