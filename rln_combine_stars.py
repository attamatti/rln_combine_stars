#!/usr/bin/env python

# merge two starfiles that have different headers 

import sys

###---------function: read the star file get the header, labels, and data -------------#######
def read_starfile(f):
    inhead = True
    alldata = open(f,'r').readlines()
    labelsdic = {}
    data = []
    header = []
    count = 0
    labcount = 0
    for i in alldata:
        if '_rln' in i and '#' in i:
            labelsdic[i.split('#')[0]] = labcount
            labcount+=1
        if inhead == True:
            header.append(i.strip("\n"))
            if '_rln' in i and '#' in i and  '_rln' not in alldata[count+1] and '#' not in alldata[count+1]:
                inhead = False
        elif len(i.split())>=1:
            data.append(i.split())
        count +=1
    
    return(labelsdic,header,data)
#---------------------------------------------------------------------------------------------#

if len(sys.argv) != 3 or '.star' not in sys.argv[1] or '.star' not in sys.argv[2]:
    sys.exit('USAGE: rln_combine_stars.py <star file 1> <star file 2>')
    
labels1,header1,data1 = read_starfile(sys.argv[1])
labels2,header2,data2 = read_starfile(sys.argv[2])

common_labels = []
for i in labels1:
    if i in labels2:
        common_labels.append(i)
print('\n.oO                            Combine Relion Star Files                                       Oo.')
print('.oO   2017 Matt Iadanza - University of Leeds Astbury Centre for Structural Molecular Biology  Oo.')
print('\nThe two starfiles have the following column labels in common:')
n = 1
for i in common_labels:
    print('{0})  {1}'.format(n,i))
    n+=1
print('\nWhich columns do you want in the output star file?')
try:
    columns = raw_input("comma separated or type 'a' for all common columns: ")
except:
    columns = input("comma separated or type 'a' for all common columns: ")
final_cols = []
if columns =='a':
    final_cols = common_labels
else:
    for i in columns.split(','):
        final_cols.append(common_labels[int(i)-1])


top_header = """data_

loop_

"""
header_cols = []
n=1
for i in final_cols:
   header_cols.append('{0}  #{1}\n'.format(i,n))
   n+=1

output = open('merged.star','w')
output.write(top_header)
for i in header_cols:
    output.write(i)
for i in data1:
    line = []
    for j in final_cols:
        line.append('{0}'.format(i[labels1[j]]))
    line.append('\n')
    line = '    '.join(line)
    output.write(line)
for i in data2:
    line = []
    for j in final_cols:
        line.append('{0}'.format(i[labels2[j]]))
    line.append('\n')
    line = '    '.join(line)
    output.write(line)
print('wrote merged.star')
output.close()
