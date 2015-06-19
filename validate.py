import re
import time

#reg = re.compile('^[0-9]{4}[ ]([0-9]{2}[ ]){5}(open|closed|error|o|c)$')
reg = re.compile('^[0-9]{14}(o|c|e)$')

def parse(path='values.txt'):
    localLog = []
    start = time.time()
    count = 0
    f = open(path, 'r')
    match = reg.match
    append = localLog.append
    for line in f:
        if match(line) != None:
            #LIST.append((line[20:],datetime.datetime(int(line[0:4]), int(line[5:7]), int(line[8:10]), int(line[11:13]), int(line[14:16]), int(line[17:19]))))
            append((line[15:16],line[0:14]))
            count += 1
            #if count % (1440*10) == 0:
            #    print (count)
        else:
            print("failed to match line %i which was: %s" % (count,line))
    f.close()
    end = time.time()
    print("it took %f seconds" % (end-start))
    return localLog
    #Also compute how many failed..

LOG = parse('values.txt')
LOG.sort(key = lambda x: x[1] )
for i in range(len(LOG)-2):
    if LOG[i][1][0:12] == LOG[i+1][1][0:12]:
        print (LOG[i][1], " ",LOG[i+1][1], " same!\n")

