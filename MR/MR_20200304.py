file_path_1 = 'E:\\work\\USE\\MR\\file\\Escherichia coli (strain K12).fasta'
file_path_2 = 'E:\\work\\USE\\MR\\file\\乙酰化蛋白.fasta'

def readfasta(FILE_PATH):
    protein = {}
    f = open(FILE_PATH)
    protein_buffer = ''
    pro_name = ''
    pro_inf = ''
    for line in f:
        if not line.startswith('>'):
            protein_buffer = protein_buffer + line.replace('\n', '')#去掉行尾的换行符真的很重要！  
        else:
            protein[pro_name] = [protein_buffer, pro_inf]
            protein_buffer = ''
            pro_name = line.split(' ')[0]
            pro_inf = line
    f.close()
    protein[pro_name] = protein_buffer
    protein.pop('')
    return protein

protein = readfasta(file_path_1)
