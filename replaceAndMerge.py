import re
import time

reg = re.compile('^[0-9]{4}[ ]([0-9]{2}[ ]){5}(open|closed|error|o)$')
reg2 = re.compile('^[0-9]{14}[ ](o|c|e)$')

def parse(path='values.txt'):
    localLog = []
    start = time.time()
    count = 0
    f = open(path, 'r')
    match = reg.match
    match2 = reg2.match
    append = localLog.append
    for line in f:
        if match(line) != None:
            #LIST.append((line[20:],datetime.datetime(int(line[0:4]), int(line[5:7]), int(line[8:10]), int(line[11:13]), int(line[14:16]), int(line[17:19]))))
            append((line[20:21],''.join((line[0:4],line[5:7],line[8:10],line[11:13],line[14:16],line[17:19]))))
            count += 1
            #if count % (1440*10) == 0:
            #    print (count)
        elif match2(line) != None:
            append((line[15:16],line[0:14]))
            count += 1
        else:
            print("failed to match line %i which was: %s" % (count,line))
    f.close()
    end = time.time()
    print("it took %f seconds" % (end-start))
    return localLog
    #Also compute how many failed..

LOG = parse('values.txt')
LOG2 = parse('errorlog.txt')
#print(LOG) 
LOG3 = LOG + LOG2
LOG3.sort(key = lambda x: x[1] )
with open('valueMERGED.txt', 'w') as f:
    for (status,date) in LOG3:
        f.write(date+''+status + '\n')
print ('\nDONE with merge')
with open('errorlogTruncated.txt', 'w') as f:
    for (status,date) in LOG2:
        f.write(date+''+status + '\n')

