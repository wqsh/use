def PeptideAndModloc(test):
    '''
    :param test:鉴定出的带修饰的肽段
    :return: 返回list,包括肽段和发生修饰的位点
    '''

    new = ''
    cut = 0
    num = 0
    loc = []
    flag = 1
    for i in range(len(test)):
        if (test[i] >= 'A') & (test[i] <= 'Z'):
            new = new + test[i]
            flag = 0
            cut = cut + num
            num = 0
        else:
            num = num + 1
            if flag == 0:
                loc.append(i - cut)
                flag = 1
    output = [new, loc]
    return output
'''
修改文件路径
'''
FILE_NAME = 'E:\\work\\USE\\FILE\\Phospho (ST)Sites.txt'
with open(FILE_NAME, 'r') as f:
    buffer = f.readlines()
Phospho = []
'''
要需要的那一列数据
'''
for line in buffer:
    Phospho.append(line.split('\t')[17])

'''
第一行没用
'''
del Phospho[0]
'''
判断要找的位点是不是满足前后都有六个氨基酸 
'''
out = []
need_out = []
for line in Phospho:
    pep = PeptideAndModloc(line)
    pep_len = len(pep[0])
    out_buffer = []
    for i in pep[1]:
        if (i > 6) & (pep_len - i >= 6):
            need_pep = pep[0][(i - 7):(i + 6)]
            out_buffer.append(need_pep)
            need_out.append(need_pep)
    out.append(out_buffer)
'''
去重,不需要保持顺序就直接下面这句就可以了
need_out = list(set(need_out))
'''
output = []
for i in need_out:
    if i in output:
        pass
    else:
        output.append(i)
need_out = output
str = ''
for i in need_out:
    str = str + i + '\n'
'''
找到的肽段结果输出在这个文件里
'''
with open('result.txt', 'w') as f:
    f.write(str)
print('haha')