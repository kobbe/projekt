#!/usr/bin/env python3
# -- coding: utf-8 --
""" program to make a graph from door log in moebius.

--timespan, -t : The number of minutes to generate a graph for
--output, -o   : The output file to write the graph to (use .png)
--sleep, -s    : How long in minutes to sleep between graphs
file(last arg) : Which file to read for input

The input file are used with tail -n timespan in order to filter out the last 
timespan rows of the file, in case the file is huge.

The filtered output vill be unnessecary large but at least it not a huge file
and <10000 rows is fast to read anyway.

The program can fail if the door changes state more than once every minute for 
the whole duration of the specified timespan. 

The program will produce the wrong output if the script generating the output
dies. In that case the last output from the program will seem like the current
output even despite it beeing very old!

The program draws the graph with a bargraph where each bar is next to each other and all of height 1,
they only differ in color and legth.

The data is assumed to be on the form "yyyy-mm-dd HH:MM:SS Changed state from %s to %s" % (oldstate, state)
oldstate and state can be None, open or closed.

Hans Koberg, 2015.
"""

import argparse
import sys
import matplotlib
matplotlib.use('SVG') #Use SVG for speed!
#matplotlib.use('Agg') #default without display
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import datetime
import time
import subprocess
import logging

LOG_FILE = "/var/log/doorsensor/graph.log"

#To make sure that some of the arguments are positive.
def positive_int(val):
    try:
        assert(int(val) > 0)
    except:
        raise ArgumentTypeError("'%s' is not a valid positive int" % val)
    return int(val)

    
def translate(name):
    if name == "open":
        return 'g'
    elif name == "closed":
        return 'r'
    else:
        return 'y'
        
        
def logger_setup():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)-8s %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        filename=LOG_FILE,
                        filemode="a")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--timespan", dest='timeSpan', help="The number of minutes to show", type=positive_int,required=True)
    parser.add_argument("-o", "--output", help="output file to write picture to",required=True)
    parser.add_argument("-c", "--compressed", help="output file to write compressed intervals to",required=True)
    parser.add_argument("-s", "--sleep",help="how long in minutes to sleep between plots",type=positive_int,required=True)
    parser.add_argument("file", help="Input file")
    args = parser.parse_args()
    sleepUntil = datetime.datetime.now().replace(second=0,microsecond=0) + datetime.timedelta(minutes=(args.sleep+1))
    while True:
        output = subprocess.check_output(["tail","-n",str(args.timeSpan+10),str(args.file)])
        endTime = datetime.datetime.now() # .replace(second=0,microsecond=0) try without the replacement!
        startTime = endTime - datetime.timedelta(minutes=args.timeSpan -1)
        #The input to the plotter needs to be date in compressedLog, widths
        #is how long that date is and colors is the color on that date interval
        compressedLog = [startTime]
        colors = []
        widths = [] #in fractions of days
        lastnewstate = "y"
        foundLastNewState = False
        for line in output.decode("utf-8").split("\n"):
            try: #in order to filter out error rows on the input
                date = datetime.datetime.strptime(line[0:19],"%Y-%m-%d %H:%M:%S")
                splitLine = line.split()
                if date < startTime: # not in spcified date range
                    # Get the lastnewstate that is outside the date range 
                    # in case the specified date range is empty.
                    
                    lastnewstate = translate(splitLine[7])
                    foundLastNewState = True
                    continue
                    
                
                oldstate = translate(splitLine[5])
                newstate = translate(splitLine[7])
                    
                #length of interval in fractions of days
                width = (date - compressedLog[-1]).total_seconds() / (60*60*24)
                widths.append(width)
                compressedLog.append(date)
                if colors != [] or foundLastNewState:
                    if lastnewstate == oldstate:
                        colors.append(oldstate)
                    else: #The last newstate and this oldstate does not match! Write "y"
                        colors.append("y")
                else:
                    colors.append(oldstate)
                lastnewstate = newstate
            except:
                pass
                
        
        #Add the last missing color and width here!
        colors.append(lastnewstate)
        width = (endTime - compressedLog[-1]).total_seconds() / (60*60*24)
        widths.append(width)
        
        #color to state for interval texts
        openText = "<font color='green'>Öppet</font>"
        closedText = "<font color='red'>Stängt</font>"
        unknownText = "<font color='FFC200'>Ingen data</font>" 
        
        state = [openText if i=="g" else closedText if i=="r" else unknownText for i in colors]
        
        #Save the intervals in a text file.
        with open(args.compressed,'w') as f:
            for i in range(len(compressedLog)-1):
                f.write(compressedLog[i].strftime('%Y-%m-%d %H:%M:%S') + " till " + 
                        compressedLog[i+1].strftime('%Y-%m-%d %H:%M:%S ') + state[i] + '\n')
            f.write(compressedLog[-1].strftime('%Y-%m-%d %H:%M:%S') + " till " + 
                    endTime.strftime('%Y-%m-%d %H:%M:%S ') + state[-1])
                
        #Makes each of the bars in the bar graph height one.
        y = len(compressedLog)*[1]
        
        fig, ax = plt.subplots()
        ax.axes.get_yaxis().set_visible(False)
        fig.autofmt_xdate()
        
        #Sets the description of colors box to the right of the graph
        closed_patch = mpatches.Patch(color='red', label='Stängt')
        open_patch = mpatches.Patch(color='green', label='Öppet')
        error_patch = mpatches.Patch(color='yellow', label='Ingen data')
        legend = plt.legend(handles=[open_patch,closed_patch,error_patch],loc=6, bbox_to_anchor=(1, 0.5))
        
        plt.title("Möbius dörr\n(Genererad: " + endTime.strftime('%Y-%m-%d %H:%M:00') + ")")
        
        barlist = ax.bar(compressedLog,y,width=widths)
        for i,bar in enumerate(barlist): #Set colors
            bar.set_color(colors[i])
        
        #Set major and minor axis locators
        ax.xaxis.set_major_formatter( mdates.DateFormatter('%Y-%m-%d %H:%M:00') )
        ax.xaxis_date()
        #
        
        plt.tick_params(which='major', length=10,width=1)
        plt.tick_params(which='minor', length=4,width=1)
        
        if args.timeSpan == 1440:
            ax.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(1/24))
        elif args.timeSpan == 10080:
            ax.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(1/4))
            
        plt.savefig(args.output,bbox_extra_artists=(legend,), bbox_inches='tight')
        plt.close('all')

        #it can actually sleep to little, (0.000200) s to little, add 0.1 to compensate.
        sleepSeconds = (sleepUntil-datetime.datetime.now()).total_seconds() + 0.1

        time.sleep(sleepSeconds)
        sleepUntil = sleepUntil + datetime.timedelta(minutes=args.sleep)
        
        
if __name__ == "__main__":
    logger_setup()
    try:
        logging.info("Starting program")
        main()
    except Exception as e:
        logging.exception(e)
        raise # Throw the same exception again such that a user can watch it