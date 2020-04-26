'''
修改下面这三个文件路径名即可
'''

FILE_PATH = 'E:\\work\\USE\\MR\\file\\MR_20200219.txt'   # 输入文件
OUT_PUT_1 = 'E:\\work\\USE\\MR\\out\\ouput_20200204\\out_MR_20200219_1.txt'  # 输出文件1, 蛋白，肽段数量，肽段列表
OUT_PUT_2 = 'E:\\work\\USE\\MR\\out\\ouput_20200204\\out_MR_20200219_2.txt'  # 输出文件2，肽段，长度

class CData:
    pep = []
    mod_loc = []
    pro = []

class COut:
    pro = []
    mod_num = []
    pep = []
    loc = []

with open(FILE_PATH, 'r') as f:
    buffer = f.readlines()
del buffer[0]
num = 0
MyData = CData()
for line in buffer:
    MyData.pep.append(line.split('\t')[1])
    MyData.mod_loc.append(line.split('\t')[6].replace('"', '').split(';'))
    MyData.pro.append(line.split('\t')[8])
    num = num + 1

out = COut()
for i in range(len(MyData.pro)):
    # 判断蛋白是否存在
    flag1 = 0
    flag2 = 0
    if MyData.pro[i] in out.pro:
        pro_index = out.pro.index(MyData.pro[i])
        if MyData.pep[i] in out.pep[pro_index]:
            pep_index = out.pep[pro_index].index(MyData.pep[i])
            for n in range(len(MyData.mod_loc[i]) - 1):
                if MyData.mod_loc[i][n].split(',')[1] == 'Acetyl[K]':
                    '''
                    if MyData.mod_loc[i][n].split(',')[0] in out.loc[pro_index][pep_index]:
                        pass
                    else:
                    '''
                    out.mod_num[pro_index] = out.mod_num[pro_index] + 1
                        #out.loc[pro_index][pep_index].append(MyData.mod_loc[i][n].split(',')[0])
        else:
            out.pep[pro_index].append(MyData.pep[i])
            out.loc[pro_index].append([])
            pep_index = out.pep[pro_index].index(MyData.pep[i])
            for n in range(len(MyData.mod_loc[i]) - 1):
                if MyData.mod_loc[i][n].split(',')[1] == 'Acetyl[K]':
                    out.mod_num[pro_index] = out.mod_num[pro_index] + 1
                    out.loc[pro_index][pep_index].append(MyData.mod_loc[i][n].split(',')[0])
    else:
        out.pro.append(MyData.pro[i])
        pro_index = out.pro.index(MyData.pro[i])
        out.pep.append([MyData.pep[i]])
        pep_index = out.pep[pro_index].index(MyData.pep[i])
        out.mod_num.append(0)
        out.loc.append([[]])
        for n in range(len(MyData.mod_loc[i]) - 1):
            if MyData.mod_loc[i][n].split(',')[1] == 'Acetyl[K]':
                out.mod_num[pro_index] = out.mod_num[pro_index] + 1
                out.loc[pro_index][pep_index].append(MyData.mod_loc[i][n].split(',')[0])
            else:
                pass

with open(OUT_PUT_1, 'w') as f:
    for i in range(len(COut.pro)):
        f.write(COut.pro[i])
        f.write('\t')
        f.write(str(COut.mod_num[i]))
        f.write('\t')
        f.write(str(COut.pep[i]))
        f.write('\n')

with open(OUT_PUT_2, 'w') as f:
    for i in range(len(CData.pep)):
        f.write(CData.pep[i])
        f.write('\t')
        f.write(str(len(CData.pep[i])))
        f.write('\n')
