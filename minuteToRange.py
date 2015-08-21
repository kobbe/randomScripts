# -*- coding: utf-8 -*-
""" program to convert data on the form yyyymmddhhmmdds where s is o (open),c (closed) or e (error) 
to data on the form yyyy-mm-dd HH:MM:SS Changed state from %s to %s" % (oldstate, state)
where oldstate and state can be None, open or closed.
The new data only writes when the state changes, unlike the old where the data is always logged.

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

if __name__ == "__main__":
    reg = re.compile('^[0-9]{14}(o|c|e)$')
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="output file to write output too")
    parser.add_argument("file", help="Input file")
    args = parser.parse_args()
    #print("after while True")
    endTime = datetime.datetime.now().replace(second=0,microsecond=0)
    log = [['y',endTime - i*datetime.timedelta(minutes=1)] for i in range(args.timeSpan -1,-1,-1)]
    #output = subprocess.check_output(["tail","-n",str(args.timeSpan+60),str(args.file)])
    
    for line in output.decode("utf-8").split("\n"):
        if reg.match(line) != None:
            date = datetime.datetime.strptime(line[0:14],"%Y%m%d%H%M%S")
            if date >= log[0][1]:
                index = int((date-log[0][1]).total_seconds()) // 60
                if line[14:15] == 'o':
                    log[index][0] = 'green'
                elif line[14:15] == 'c':
                    log[index][0] = 'r'
                #else: #use this if error values should differ from missing values
                #    log[index][0] = 'yellow'
    
    
    #print("Start after read input")
    #start = datetime.datetime.now()
    
    #log is never empty
    compressedLog = [log[0][1]]
    colors = [log[0][0]]
    widths = [1] #in fractions of days
    tempWidths = 1
    
    for (color,date) in log:
        if (color == colors[-1]):
            #same state, can be compressed, continue.
            tempWidths += 1
            widths[-1] = tempWidths/(24*60) #interval lenght +1
        else:
            #End the current streak
            compressedLog.append(date)
            widths.append(1/(24*60))
            tempWidths = 1
            colors.append(color)
    
    
    
    
    
    
    
