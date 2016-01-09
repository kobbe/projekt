#!/usr/bin/python -u
# -*- coding: utf-8 -*-

"""radongraph.py

Program to plot radon levels.

Hans Koberg, 2015

Usage:

radongraph.py -t TIMESPAN -o OUTFILE FILE

Data in the input file is assumed to be on form <timestamp> <value>
where <timestamp> is the Unix time corresponding to the logged value
and <value> is given in Bq/m^3.
"""


# Change backend before importing pyplot in order
# to run the script without a running X server.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as dat
import matplotlib.dates as mdates
import argparse
import datetime
import re
import logging
reg = re.compile('^[0-9]* [0-9]{1,4}$')

LOG_FILE = "/var/log/radongraph.log"


#To make sure that some of the arguments are positive.
def positive_int(val):
    try:
        assert(int(val) > 0)
    except:
        raise ArgumentTypeError("'%s' is not a valid positive int" % val)
    return int(val)

    
def logger_setup():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)-8s %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        filename=LOG_FILE,
                        filemode="a")


def main():
    # Do stuff
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--timespan", dest='timeSpan', help="The last number of hours to display", type=positive_int,required=True)
    parser.add_argument("-o", "--output", help="output file to write picture to",required=True)
    parser.add_argument("file", help="Input file")
    args = parser.parse_args()
    endTime = datetime.datetime.now().replace(minute=0,second=0,microsecond=0)
    startTime = endTime + datetime.timedelta(hours=-int(args.timeSpan)+1)
    
    # Create a list of all datetime we want to use
    dateList = [[endTime - i*datetime.timedelta(hours=1), None] for i in range(args.timeSpan - 1,-1,-1)]

    with open(args.file, 'r') as f:
        for line in f:
            if reg.match(line) != None:
                fields = line.split(" ")
                timestamp = int(fields[0])
                date = datetime.datetime.fromtimestamp(timestamp)
                if date >= startTime:
                    value = int(fields[1])
                    index = int((date-startTime).total_seconds())//(60*60)
                    dateList[index][1] = value
    
    x = [i[0] for i in dateList]
    y = [i[1] for i in dateList]

    fig, ax = plt.subplots()
    fig.autofmt_xdate()

    plt.xlabel('Datum')
    plt.ylabel('Bq/m$^{3}$')
    plt.title(u'Radonmätvärden från Moebius källare\n(Genererad: ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ")")

    ax.plot_date(x,y,'-',marker='.')
    ax.plot(x, [200 for i in x], '-', color='red')

    ax.xaxis.set_major_formatter( mdates.DateFormatter('%Y-%m-%d %H:00:00') )
    plt.gcf().subplots_adjust(bottom=0.25)

    # Prevent truncation of the axes. Set ymax to be slightly larger
    # than the calculated value to make extreme values visible.
    if len(x) > 0:
        plt.xlim(x[0],x[-1])
    plt.ylim(ymin=0, ymax=plt.gca().get_ylim()[1]*1.1)

    plt.savefig(args.output)

if __name__ == "__main__":
    logger_setup()
    try:
        logging.info("Starting program")
        main()
    except Exception as e:
        logging.exception(e)
        raise # Throw the same exception again such that a user can watch it