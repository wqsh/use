FILE_NAME = 'C:\\Users\\dell\\Documents\\Tencent Files\\767275138\\FileRecv\\danbaihuzuo.tsv'
class data:
    node1 = []
    node2 = []
with open(FILE_NAME, 'r') as f:
    buffer = f.readlines()
for line in buffer:
    data.node1.append(line.split('\t')[0])
    data.node2.append(line.split('\t')[1])
with open('danbairesult.txt', 'w') as f:
    for i in range(len(data.node1)):
        f.write(data.node1[i])
        f.write('\t')
        f.write('interacts')
        f.write('\t')
        f.write(data.node2[i])
        f.write('\n')
print('haha')