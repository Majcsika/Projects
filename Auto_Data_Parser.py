#!/usr/bin/env python3
# Maya Fry
import os
import csv
import sys
from collections import namedtuple
from collections import defaultdict
import logging
import requests
import argparse
import matplotlib.pyplot as plt

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

logging.basicConfig(filename = 'autompg2.log', level = logging.DEBUG, filemode = 'w')

sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
logger.addHandler(sh)

def main():
    #iterate through the AutoMPG data and print out data based on command
    parser = argparse.ArgumentParser(description='analyze Auto MPG data set')
    parser.add_argument('command', choices=['print', 'mpg_by_year', 'mpg_by_make'], help='prints out data in the terminal and saves output to file')
    parser.add_argument('-s', '--sort', nargs='?', choices=['default', 'year', 'mpg'], default='default', help='sorting order for data')
    parser.add_argument('-p', '--plot', action='store_true', help='specify if graphical output should be created')
    parser.add_argument('-o', '--ofile', nargs='?', default = sys.stdout, help='specify name of file to save output')
    args = parser.parse_args()
    if args.command == 'print':
        ucidata = AutoMPGData()
        if args.sort == 'year':
            ucidata.sort_by_year()
            x = lambda a: (a.make, a.model, a.year, a.mpg)
            if args.ofile != sys.stdout:
                with open(args.ofile, 'w') as output_file:
                    writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)
                    writer.writerow(["YEAR", "MAKE", "MODEL", "MPG"])
                    for a in ucidata:
                        y = x(a)
                        writer.writerow([y[2], y[0], y[1], y[3]])
            else:
                for a in ucidata:
                    y = x(a)
                    print(y)                
        elif args.sort == 'mpg':
            ucidata.sort_by_mpg()
            x = lambda a: (a.make, a.model, a.year, a.mpg)
            if args.ofile != sys.stdout:
                with open(args.ofile, 'w') as output_file:
                    writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)
                    writer.writerow(["MPG", "MAKE", "MODEL", "YEAR"])
                    for a in ucidata:
                        y = x(a)
                        writer.writerow([y[3], y[0], y[1], y[2]])
                        print(a)
            else:
                for a in ucidata:
                    y = x(a)
                    print(y)
        else:
            ucidata.sort_by_default()
            x = lambda a: (a.make, a.model, a.year, a.mpg)
            if args.ofile != sys.stdout:
                with open(args.ofile, 'w') as output_file:
                    writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)
                    writer.writerow(["MAKE", "MODEL", "YEAR", "MPG"])
                    for a in ucidata:
                        y = x(a)
                        writer.writerow([y[0], y[1], y[2], y[3]])
                        print(a)
            else:
                for a in ucidata:
                    y = x(a)
                    print(y)
        logging.debug(f'The autoMPG data has been sorted by {args.sort} and saved to {args.ofile}')
        logging.info('The autoMPG data has been sorted')
    elif args.command == 'mpg_by_year':
        ucidata = AutoMPGData()
        ucidict = AutoMPGData.mpg_by_year(ucidata)
        if args.ofile != sys.stdout:
            with open(args.ofile, 'w') as output_file:
                writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)
                writer.writerow(["YEAR", "AVERAGE MPG"])
                for key, value in ucidict.items():
                    writer.writerow([key, value])
        else:
            print(ucidict)
        if args.plot == True:
            x = ucidict.keys() 
            y = ucidict.values()   
            plt.plot(x, y) 
            plt.xlabel('Year') 
            plt.ylabel('Average MPG') 
            plt.title('MPG By Year') 
            plt.show()
    elif args.command == 'mpg_by_make':
        ucidata = AutoMPGData()
        ucidict = AutoMPGData.mpg_by_make(ucidata)
        if args.ofile != sys.stdout:
            with open(args.ofile, 'w') as output_file:
                writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)
                writer.writerow(["MAKE", "AVERAGE MPG"])
                for key, value in ucidict.items():
                    writer.writerow([key, value])
        else:
            print(ucidict)
        if args.plot == True:
            x = ucidict.keys() 
            y = ucidict.values()   
            plt.plot(x, y) 
            plt.xlabel('Make') 
            plt.ylabel('Average MPG') 
            plt.title('MPG By Make') 
            plt.show() 


class AutoMPGData:
    #naming class attributes
    Data = []
    num = 0
    def __init__(self):
        self._load_data()
    def __iter__(self):
        return self
    def __next__(self):
        #Go through all lines of data (398 lines) in the Auot MPG data file, and stop after the last one. 
        if self.num == 397:
            raise StopIteration
        else:
            self.num += 1
            return self.Data[self.num]
    def _clean_data(self):
        #Take text file and transform the tabs to spaces. Create a new text file with the data.
        with open(('auto-mpg.data.txt'), 'r') as f:
            newfile = open(('auto-mpg.clean.txt'), 'w')
            for line in f:
                Line = line.expandtabs(1)
                newfile.write(Line)
        logging.debug('The text file has been turned into a readable text file')
        logging.info('Data cleaned')
    def _load_data(self):
        if not os.path.exists('auto-mpg.data.txt'):
            self._get_data()
        #Check to see if the clean text file exists. If not, create the clean text file. 
        if not os.path.exists('auto-mpg.clean.txt'):
            self._clean_data()
        #Create a namedtuple to assign each element a name
        Record = namedtuple('Record', 'mpg, cylinders, displacement, horsepower, weight, acceleration, year, origin, make, model')
        #read through each row in the text file, and create a list out of each row
        with open('auto-mpg.clean.txt', 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', skipinitialspace = True)
            for row in reader:                 
                x = row[8].split(' ')
                row.pop(8)
                if x[0] == "chevroelt" or x[0] == "chevy":
                    x[0] = "chevrolet"
                if x[0] == "maxda":
                    x[0] = "mazda"
                if x[0] == "mercedes-benz":
                    x[0] = "mercedes"
                if x[0] == "toyouta":
                    x[0] = "toyota"
                if x[0] == "vokswagen" or x[0] == "vw":
                    x[0] = "volkswagen"
                if len(x) == 3:
                    y = [x[1], x[2]]
                    row.append(x[0])
                    row.append(' '.join(y))
                elif len(x) == 2:
                    row.append(x[0])
                    row.append(x[1])
                else:
                    row.append(x[0])
                    row.append('unknown')
                #match elements of each row list to the namedtuple that was established above.
                Car = Record(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
                #Call the autoMPG class to pull the appropriate data for each row of data.
                vehicle = autoMPG(Car.make, Car.model, Car.year, Car.mpg)
                #add to Data list
                self.Data.append(vehicle)
            logging.debug('The autoMPGData list has been created, pulling make, model, year, and mpg for each car')
            logging.info('Data list created')
    def sort_by_default(self):
        self.Data.sort()
    def sort_by_year(self):
        self.Data.sort(key=lambda x: (x.year, x.make, x.model, x.mpg))
    def sort_by_mpg(self):
        self.Data.sort(key=lambda x: (x.mpg, x.make, x.model, x.year))
    def mpg_by_year(self):
        d = defaultdict(list)
        for row in AutoMPGData.Data:
            x = lambda a: (a.make, a.model, a.year, a.mpg)
            y = x(row)
            d[y[2]].append(y[3])
        for key, value in d.items():
            d[key] = sum(value)/len(value)
        return d
    def mpg_by_make(self):
        d = defaultdict(list)
        for row in AutoMPGData.Data:
            x = lambda a: (a.make, a.model, a.year, a.mpg)
            y = x(row)
            d[y[0]].append(y[3])
        for key, value in d.items():
            d[key] = sum(value)/len(value)
        return d
    def _get_data(self):
        url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data'
        response = requests.get(url, allow_redirects=True)
        print(f'status = {response.status_code}')
        if response:
            print("Successful request!")
        else:
            print(f'Error: {response.status_code}')
        response.raise_for_status()
        open('auto-mpg.data.txt', 'wb').write(response.content)

class autoMPG:
    def __init__(self, make, model, year, mpg):
        #establish attributes
        self.make = make
        self.model = model
        self.year = int(year)
        self.mpg = float(mpg)
    def __repr__(self):
        return f"autoMPG({self.make}, {self.model}, {self.year}, {self.mpg})"
    def __str__(self):
        return self.__repr__()
    def __eq__(self, other):
        #assert equality
        if type(self) == type(other):
            return (self.make, self.model, self.year, self.mpg) == (other.make, other.model, other.year, other.mpg) 
        else:
            return NotImplemented
    def __lt__(self, other):
        #comparing two objects to each other
        if type(self) == type(other):
            return (self.make, self.model, self.year, self.mpg) < (other.make, other.model, other.year, other.mpg)
        else:
            return NotImplemented
    def __hash__(self):
        return hash((self.make, self.model, self.year, self.mpg))

if __name__ == "__main__":
    main()