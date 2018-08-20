target = 'R:\\exhumation\\exhumation.txt'
output = 'R:\\exhumation\\output_full.txt'

def writer(string):
    with open(output,'a') as out:
        out.write(string)

with open(target,'r') as text:
    for line in text:
        #print line
        line = str(line)
        line_2 = line.replace(' ',',')
        if not "RE" in line:
            #if not "NATURE" in line:
            #print line_2
            writer(line_2)