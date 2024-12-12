import argparse
import matplotlib.pyplot as plt
from utilities import FileReader

# Made changes in this file to reflect code used in lab 4. Optimized it to make it 
# easier to store results

def plot_errors():
    
    headers, values = FileReader(filename).read_file()

    
    time_list=[]
    
    first_stamp=values[0][-1]
    
    for val in values:
        time_list.append(val[-1] - first_stamp)



    for i in range(0, len(headers) - 1):
        plt.plot(time_list, [lin[i] for lin in values], label= headers[i]+ " linear")

    plt.legend()
    plt.grid()

    plt.show()
    
    

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Process these files')
    parser.add_argument('--files', nargs='+', required=True, help='List of files to process')

    args = parser.parse_args()

    print("plotting the files", args.files)

    filenames = args.files
    for filename in filenames:
        plot_errors(filename)