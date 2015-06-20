# -*- coding: utf-8 -*-




import re
import datetime
import time


def parseRadon(path='radoncat'):
    reg = re.compile('^[0-9]{10} [0-9]{2,3}$')
    localLog = []
    start = time.time()
    count = 0
    f = open(path, 'r')
    match = reg.match
    append = localLog.append
    for line in f:
        if match(line) != None:
            (UNIXtime,value) = line.split()
            append((int(value),datetime.datetime.fromtimestamp(int(UNIXtime))))
            count += 1
        else:
                print("failed to match line %i which was: %s" % (count,line))
    f.close()
    end = time.time()
    print("it took %f seconds" % (end-start))
    print("Last radon log is: ",localLog[-1])
    return localLog
    
    
    
if __name__ == "__main__":
    #LOG = parse('values.txt')
    radonLOG = parseRadon()
    with open('radoncat.easy','w') as f:
        for (value,date) in radonLOG:
            f.write(date.strftime("%Y-%m-%d %H:%M:%S") + " " + str(value) + "\n")