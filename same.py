#!/usr/bin/python3 -u
# -*- coding:utf-8 -*-


import gc
import re
import time
import random
import calendar
import datetime
import itertools

def parse(path='values.txt'):
    reg = re.compile('^[0-9]{14}(o|c)$') #Only include valid open or closed, not errors.
    localLog = []
    start = time.time()
    count = 0
    f = open(path, 'r')
    match = reg.match
    append = localLog.append
    for line in f:
        if match(line) != None:
            append((line[14:15],datetime.datetime(int(line[0:4]),int(line[4:6]),int(line[6:8]),int(line[8:10]),int(line[10:12]),int(line[12:14]))))
            count += 1
        #else:
        #    #print("failed to match line %i which was: %s" % (count,line))
    f.close()
    end = time.time()
    print("it took %f seconds" % (end-start))
    return localLog
    
def makeInput(LOG):
    #Useful attributes: Use 1 or 0 as input, not continious if they do not have any purpose.
    #Weekday, (Month, day = day of year?), hour, minute
    #Holiday? Terminstider uu
    
    #Not useful
    #Year, second
    
    #7 Weekdays, 365 days, 24hr,
    
    retLOG = []
    for (state,date) in LOG:
        weekDay = [date.weekday()]
        #weekDay[0] = date.weekday()
        
        dayOfYear = [0] #We have 366 days now.
        if calendar.isleap(date.year):
            dayOfYear[0] = date.timetuple().tm_yday-1
        else:
            if date.timetuple().tm_yday >= 60:
                dayOfYear[0] = date.timetuple().tm_yday-1+1
            else:
                dayOfYear[0] = date.timetuple().tm_yday-1
        
        hour = [date.hour]
        #hour[date.hour] = 1
        
        # 7 Weekdays, 366 days, 24 hours, 
        tempLog = [state] + weekDay + dayOfYear + hour
        retLOG.append(tempLog)
        if len(retLOG) % (len(LOG) // 10) == 0:
            print("done with ", len(retLOG) / len(LOG) , "%")
            print("Running GC...")
            gc.collect()
            print("GC done...")
    return retLOG

    
if __name__ == "__main__":

    print("Reading data...")
    #parse data, list of (state,datetime,yyyymmddHHMMSS)
    LOG = parse("values.txt") 
    
    
    #Test if any two inputs have the same dayOfYear, weekday and hour with different open/closed
    
    LOG2 = makeInput(LOG)
    c = 0
    d = []
    for (i,j) in itertools.combinations(LOG2,2):
        if i[1:]==j[1:] :
            if i[0] != j[0]:
                print(i, " NOT!! Same as ", j)
                d.append(i)
                d.append(j)
            #print(i, " Same as ", j)
        c = c+1
        if c % 1000000 ==0:
            print("done with " , c)
    
    