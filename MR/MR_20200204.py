'''
修改下面这三个文件路径名即可
'''

FASTA_PATH = 'E:\\work\\USE\\MR\\CGQ_result\\UP000002524_243230.fasta'  # fasta文件
PRO_PATH = 'E:\\work\\USE\\MR\\CGQ_result\\ss.txt'   # 把找到的蛋白命存在一个文本文件里，一列存一个
OUT_PUT = 'E:\\work\\USE\\MR\\CGQ_result\\out.txt'  # 输出文件

def readfasta(FILE_PATH):
    protein = {}
    f = open(FILE_PATH)
    protein_buffer = ''
    pro_name = ''
    pro_inf = ''
    for line in f:
        if not line.startswith('>'):
            protein_buffer = protein_buffer + line
        else:
            protein[pro_name] = [protein_buffer, pro_inf]
            protein_buffer = ''
            pro_name = line.split('|')[1].replace('>', '')
            pro_inf = line
    f.close()
    protein[pro_name] = protein_buffer
    protein.pop('')
    return protein

def readpro_name(FILE_PATH):
    with open (FILE_PATH, 'r') as f:
        pro_name = f.readlines()
    return pro_name

pro = readfasta(FASTA_PATH)
pro_name = readpro_name(PRO_PATH)
del pro_name[0]
out_pro_name = []
for line in pro_name:
    line = line.replace('\n', '')
    line_split = line.split(';')
    if len(line_split) > 2:
        for i in line_split:
            if len(i) > 0:
                out_pro_name.append(i)
            else:
                pass
    else:
        out_pro_name.append(line_split[0])

out_put = {}
not_find = []
count = 0
for name in out_pro_name:
    if name in pro.keys():
        out_put[name] = pro[name]
    else:
        count = count + 1
        not_find.append(name)
print('not_find: ', count)
print(not_find)
with open(OUT_PUT, 'w') as f:
    for i in out_put.keys():
        #f.write('>')
        f.write(out_put[i][1])
        #f.write('\n')
        f.write(out_put[i][0])
        #f.write('\n')
