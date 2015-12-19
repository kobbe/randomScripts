# -*- coding: utf-8 -*-
""" program to convert data on the form yyyymmddhhmmdds where s is o (open),c (closed) or e (error) 
to data on the form yyyy-mm-dd HH:MM:SS Changed state from %s to %s" % (oldstate, state)
where oldstate and state can be None, open or closed.
The new data only writes when the state changes, unlike the old where the data is always logged.

ONLY convert data point before 2015 09 12 15:06:03 (inclusive)

A LOT of data is missing for only a minute (due to poor logging in the past)
Need to correct theese intervals.

Just scan the log for missing holes of data...

Hans Koberg, 2015.

"""

import argparse
import datetime
import time
import re

#Makes sure the time interval is >0
def positive_int(val):
    try:
        assert(int(val) > 0)
    except:
        raise ArgumentTypeError("'%s' is not a valid positive int" % val)
    return int(val)
    
def translate(name):
    if name == "o":
        return 'open'
    elif name == "c":
        return 'closed'
    else:
        return 'None'

if __name__ == "__main__":
    reg = re.compile('^[0-9]{14}(o|c|e)$')
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="output file to write output too")
    parser.add_argument("file", help="Input file")
    args = parser.parse_args()
    endTime = datetime.datetime.strptime("2015 09 12 15:06:00","%Y %m %d %H:%M:%S") # 2015 09 12 15:06:03
    
    with open(args.file, 'r') as f:
        for line in f:
            if reg.match(line) == None:
                continue
            startTime = datetime.datetime.strptime(line[0:14],"%Y%m%d%H%M%S").replace(second=0,microsecond=0)
            break
    minutesToLog = int((endTime-startTime).total_seconds() // 60)
    log = [['e',startTime + i*datetime.timedelta(minutes=1)] for i in range(0,minutesToLog+1)]
    print("Log size is", len(log))
    
    endTimeCheck = endTime.replace(second=59,microsecond=0)
    
    with open(args.file, 'r') as f:
        for line in f:
            if reg.match(line) == None:
                continue
            date = datetime.datetime.strptime(line[0:14],"%Y%m%d%H%M%S")
            if date > endTimeCheck:
                continue
            index = int((date-startTime).total_seconds()) // 60
            if line[14:15] == 'o':
                log[index][0] = 'o'
            elif line[14:15] == 'c':
                log[index][0] = 'c'

    print("Done reading in all values")
    
    # The data contains missing values ("e") in a lot of places due to poor logging skills
    # Fix it!
    for i in range(1,len(log)-1):
        if log[i][0] == "e" and log[i-1][0] == log[i+1][0]:
            log[i][0] = log[i-1][0]
         
    print("Done filling error gaps of size 1")
    
    compressedLog = ["%s Changed state from None to %s\n" % (log[0][1].strftime("%Y-%m-%d %H:%M:%S"),translate(log[0][0]))]
    lastState = log[0][0]
    last = True
    counter = 0
    occurenceOpen = [0] * 100000
    occurenceClosed = [0] * 100000
    occurenceError = [0] * 100000
    
    for (state,date) in log:
        if (state == lastState):
            last = False
            counter += 1
        else:
            #End the current streak
            compressedLog.append("%s Changed state from %s to %s\n" % (date.strftime("%Y-%m-%d %H:%M:%S"),translate(lastState),translate(state)))
            if lastState == "o":
                occurenceOpen[counter] += 1
            elif lastState == "c":
                occurenceClosed[counter] += 1
            else:
                occurenceError[counter] += 1
                
            lastState = state
            last = True
            
            counter = 1
            
    print("open:", occurenceOpen[0:100])
    print("closed:", occurenceClosed[0:100])
    print("error:", occurenceError[0:100])
    
    #We might need to close the last range if it did not write a change at the endTime time.
    if not last:
        compressedLog.append("%s Changed state from %s to %s\n" % (endTime.strftime("%Y-%m-%d %H:%M:%S"),translate(lastState),"None"))
    
    print("Compressed log size is", len(compressedLog))

    with open(args.output, 'w') as f:
        for line in compressedLog:
            f.write(line)
    
    
    
    
    
    
    
