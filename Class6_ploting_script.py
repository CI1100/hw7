import argparse
import os.path as op
import csv
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.cm as cm


def convert_type(data_value):
    try:
        return int(data_value)
    except ValueError:
        try:
            return float(data_value)
        except ValueError:
            return data_value


def lines_to_dict(lines, header=False):

    print('Converting lines ...')
    if header:
        column_titles = lines[0]
        lines = lines[1:]
    else:
        column_titles = list(range(1, len(lines[0])+1))
    
    data_dict = {}
    for idx, column in enumerate(column_titles):
        data_dict[column] = []
        for row in lines:
            data_dict[column] += [row[idx]]
    return data_dict

def parse_file(data_file, delimiter, debug=False):
    # Verify the file exists
    assert(op.isfile(data_file))
    print('Parsing file ... ', data_file)

    # open it as a csv (not checking delimiters, so you can do better)
    with open(data_file, 'r') as fhandle:
        csv_reader = csv.reader(fhandle, delimiter=delimiter)
        # Add each line in the file to a list
        lines = []
        if debug:
            count = 0
        for line in csv_reader:
            if debug:
                if count > 2:
                    break
                count += 1
            newline = []
            for value in line:
                newline += [convert_type(value)]

            if len(newline) > 0:
                lines += [newline]
    # Return all the contents of our file
    return lines

def draw_poly(axes, column1, column2, degree):
    min = np.min(column1)
    max = np.max(column1)
    
    xp = np.linspace(min, max, 20)
    print('Min max:', min, max, xp)
    
    coef = np.polyfit(column1, column2, degree)
    poly = np.poly1d(coef)
    line, = axes.plot(xp, poly(xp), '--')
    return line
   
def plot_data(dd, debug=False):
    # dd stands for data_dictionary
    if debug:
        number_combinations = 0
        
    fig = plt.figure()
                
    for column1 in dd.keys():
        for column2 in dd.keys():
            if debug:
                number_combinations += 1
                print(column1, column2)
            else:  
                print('Columns: ', dd[column1], dd[column2])
                fig.clf()
                ax = fig.add_subplot(1, 1, 1)    
                plt.style.use('seaborn')
                ax.scatter(x=dd[column1], y=dd[column2], cmap=cm.summer, label='Points', edgecolor='black', marker='o', linewidth=1, alpha=0.75)
                legend1 = ax.legend(loc=0)
                line = draw_poly(ax, dd[column1], dd[column2], 3)
                ax.add_artist(legend1)
                legend2 = ax.legend([line], ['Interpolation'], loc=1)
                ax.add_artist(legend2)
                #ax.legend(["Poly deg: 3"])
               
                #ax.set_xscale('log')
                #ax.set_yscale('log')
                ax.set_xlabel(column1)
                ax.set_ylabel(column2)
                ax.set_title("{0} x {1}".format(column1, column2))
                #cbar = ax.colorbar(cm.hot)
                #cbar.set_label('Correlated/Not_correlated')
                #plt.show()
                name = 'image_%s_%s.png' % (column1, column2)
                print('Saving figure: ', name)
                plt.savefig(name)

    if debug:
        print(len(dd.keys()), number_combinations)
    return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", type=str,
                        help="Input CSV data file for plotting")
    parser.add_argument("delimiter", type=str,
                        help="the delimiter used in your file")
    parser.add_argument('-x', '--debug', action="store_true",
                        help="only prints start of file")
    parser.add_argument('-H', '--header', action="store_true",
                        help="determines if a header is present")
    
    args = parser.parse_args()
    print('Args:', args)
    my_data = parse_file(args.data_file, args.delimiter, debug=args.debug)
    data_dictionary = lines_to_dict(my_data, header=args.header)
    print(data_dictionary.keys())
    plot_data(data_dictionary, debug=args.debug)

if __name__ == "__main__":
    main()