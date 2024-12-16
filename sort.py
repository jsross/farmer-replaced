from Utility import *

# Array A[] has the items to sort; array B[] is a work array.
def TopDownMergeSort(array, compare_proprty):
    length = len(array)
    working_array = create_array(length, None)

    copy_array(array, working_array)
    TopDownSplitMerge(array, 0, length, working_array, compare_proprty)   # sort data from B[] into A[]

# Split A[] into 2 runs, sort both runs into B[], merge both runs from B[] to A[]
# iBegin is inclusive; iEnd is exclusive (A[iEnd] is not in the set).
def TopDownSplitMerge(working_array, start_index, end_index, src_array, compare_proprty):
    if (end_index - start_index <= 1):                     # if run size == 1
        return                                   #  consider it sorted
    
    # split the run longer than 1 item into halves
    middle_index = (end_index + start_index) // 2        # iMiddle = mid point

    # recursively sort both runs from array A[] into working_array
    TopDownSplitMerge(src_array, start_index, middle_index, working_array, compare_proprty)  # sort the left  run
    TopDownSplitMerge(src_array, middle_index, end_index, working_array, compare_proprty)  # sort the right run

    # merge the resulting runs from array B[] into A[]
    TopDownMerge(working_array, start_index, middle_index, end_index, src_array, compare_proprty)

#  Left source half is A[ iBegin:iMiddle-1].
# Right source half is A[iMiddle:iEnd-1   ].
# Result is            B[ iBegin:iEnd-1   ].
def TopDownMerge(working_array, start_index, middle_index, end_index, src_array, compare_proprty):
    i = start_index
    j = middle_index
 
    # While there are elements in the left or right runs...
    for index in range(start_index, end_index):
        # If left run head exists and is <= existing right run head.
        if (i < middle_index and (j >= end_index or src_array[i][compare_proprty] <= src_array[j][compare_proprty])):
            working_array[index] = src_array[i]
            i = i + 1
        else:
            working_array[index] = src_array[j]
            j = j + 1