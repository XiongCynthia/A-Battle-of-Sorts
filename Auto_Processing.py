import fileinput
import os
import matplotlib.pyplot as plt
from datetime import datetime as dt

def process_counts():
    # Store all lines in the cover file in an array
    lines = []
    with fileinput.input('Sort.cover') as f:
        for line in f:
            lines.append(line)

    # Extract specific lines associated with the insert_sort and selection_sort functions
    insert_lines = lines[4:12]
    select_lines = lines[13:26]
    
    # Extract the run counts from each line, and convert them from str to int types
    insert_total = 0
    for i in range(len(insert_lines)):
        colon_idx = insert_lines[i].find(':') # Find the colon furthest to the left
        if colon_idx != -1:
            insert_total = insert_total+int(insert_lines[i][0:colon_idx])
            # Double-count the double-statement in the insertion_sort function
            if i == 4: insert_total = insert_total+int(insert_lines[i][0:colon_idx])
    select_total = 0
    for i in range(len(select_lines)):
        colon_idx = select_lines[i].find(':')
        if colon_idx != -1: select_total = select_total+int(select_lines[i][0:colon_idx])
    
    return insert_total, select_total

tStart = dt.now()
# arr_sizes = [10000,20000,30000,40000,50000]
# initial_orders = ['increasing', 'decreasing', 'random']
print('Formatting example: 10000 20000 30000 40000 50000')
arr_sizes = [int(x) for x in input('Enter array sizes to test: ').split()]
print('Formatting example: increasing decreasing random')
initial_orders = input('Enter orientation types to test: ').split()
for order in initial_orders:
    insertion_counts = []
    selection_counts = []
    for size in arr_sizes:
        # Keep track of progress in real time
        print(f'Processing {size} elements in {order} order -', dt.now()-tStart)
        # Run Sort.py
        os.system(f'python -m trace --count -C . Sort.py {size} {order}')
        # Process counts for the insertion and selection sort functions from the cover file
        inser,selec = process_counts()
        insertion_counts.append(inser)
        selection_counts.append(selec)
    #Create a graph for the order type and save it
    fig,ax = plt.subplots(figsize=(12,8))
    ax.plot(arr_sizes, insertion_counts, '.-', label='Insertion Sort')
    ax.plot(arr_sizes, selection_counts, '.-', label='Selection Sort')
    ax.set_title('Instruction Execution Counts for Insertion and Selection Sorts')
    ax.set_xlabel('Number of Elements')
    ax.set_ylabel('Total Number of Instruction Executions')
    ax.set_xticks(arr_sizes)
    ax.legend()
    fig.savefig(order)
print('Runtime:', dt.now()-tStart) # Signify the end of the program
