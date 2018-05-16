#!/usr/bin/env python
#_*_utf-08 encoding_*_

'''
Created by Alexander looi
Feb. 18, 2017
csvome.py: a tool to return important characteristics of a CSV file.
-h returns a help file
-r followed by an integer will return a list rows referenced by thos integer
-c followed by an integey will return a list of columns referenced by those integers

Note:
The canBeInt(), canBeFlt, and intfloat() functions are crucial for this script to work. These functions 
essentially sort cell values along int, float, or others (assumed to be str). There are Boolean variables 
however, since those can either be 1's 0's or strings, they will be treated as ints or strings by this code. 
These functions are mainly part of if then statements so they should return True or False. The intfloat 
function should read in a character string and be able to return the proper variable type.  

'''
import sys
import argparse

# a simple function to detect if a single variable can be converted to type int.
def canBeInt(s):
    
    '''

    Try a character string with no number characters should return false 
    >>> canBeInt('IsNotInt')
    False

    If there are funky letters in the string or numbers it should still return false
    >>> canBeInt('1sN0t1n7')
    False

    '''


    ## test to pass float here, should return false. 
    try:
        # can be converted to int
        int(s)
        return True
    except ValueError:
        # not convertable to int
        return False

def canBeFlt(s):

    '''
    >>> canBeFlt('IsNotFloat')
    False

    If there are funky letters in the string or numbers it should still return false
    >>> canBeFlt('1sN0tF10@7')
    False
    '''

    ## test to pass a str here to see if a false is returned
    try:
        # can be converted to float
        float(s)
        return True
    except ValueError:
        # not convertable to float
        return False

# a function to convert to a float or int with preference given to ints
def intfloat(s):
    '''
    # This should return an int the number 34.
    >>> isinstance(intfloat('34'), int)
    True

    # This should return a float number 34.34
    >>> isinstance(intfloat('34.34'), float)
    True

    # giving this function a string of non-numeric characters should return false
    >>> intfloat('not_a_float_or_int')
    False 

    '''
    try:
        # test the string to see if it can be converted to an int
        i = int(s)
        return i
    except ValueError:
        # in the case that a str that has non-numeric characters is passed
        # we want the function to return false. So another try except was used.
        try:
            i = float(s)
            return i
        except ValueError:
            #raise AttributeError('Object passed, cannot be converted to a float or int')
            return False


p = argparse.ArgumentParser(description=

        '''
        Created by Alexander looi
        Feb. 18, 2017
        csvome.py: a tool to return important characteristics of a CSV file. 
        Give options to reference specific rows and columns

        -h returns a help file
        -r followed by a integers will return a list rows referenced by those integers.
        -c followed by integers and/or strings will return a list of columns referenced by those integers or strings

        Generally this script will return general facts about the csv, such as the number of columns, number of rows, 
        and if the number of cells in a row are changing (this will be throw a warning about the irregularity in the csv).
        If there are inconsistent row lengths throughout the csv (includes the header). Then csvome will tell the user
        the row numbers where row lengths have changed. Be warned that the number returned is not necessarily the row
        with the problem, it could be the row before. 

        If referencing columns, the script will return general facts: including the number of integers in a column, 
        number of Floats, cells containing numerical values, NA's NaN's -9999's, and other data types (strings, Dates, 
        etc.). Additionally, the script will run if you reference a column that is out of bounds, a warning will be issued
        if this happens. If there are any other columns that can be summarized they will be summarized.

        To reference columns use "-c" after the python script call. Follow the flag with a space followed by integers, 
        or strings of the column headers. 

        The user can also reference specific rows. To do this use the -r command followed by integer of the row location. 
        If done properly, then csvome should return those rows. 
        '''
        )
p.add_argument('file', nargs='+', type = str) ## test here to pass "weird" characters

# read in a row number and print those row numbers
p.add_argument('-r', '--rownumbers', 
        nargs='*', dest='rown', type=int, required=False)
# read in a column number or a column name and return that entire column
# given the name or the column number
p.add_argument('-c', '--columnnumbers', 
        nargs='*', dest='coln', required=False)

## a simple test to see if the parser is working
args = p.parse_args() # have a test here to see that the args passed are in an unnested list.

print('Rows to be printed: ', args.rown) # print the rows the user wants to access
print('Columns to be printed: ',args.coln) # print the columns the user wants to access
#print(args.coln) # print the columns the user wants to access
#print(args.file[0])

#print(canBeInt(args.coln))
#print(list(map(int, args.coln)))
# process the -c arg enteries, turn int-able entries into ints, but leave
# other str's as is.
if args.coln is not None: ## a test here to test none -c entries
    is_arg_int = [] # this is used to grab the int number from arguments inputted by the user. 
    for c, sc in enumerate(args.coln):
        is_arg_int.append(canBeInt(sc))
        if canBeInt(sc):
            args.coln[c] = int(sc)
#print(is_arg_int)
#print(args.coln)
#is_col_s = instance
# open the file
f = open(args.file[0], 'r', errors='ignore') ## 'ignore' tells open to ignore weird characters
print('Opened file:' , args.file[0])

# read in the file to memory
# note: may want to eventually change this to reading
# to avoid memory problems in the future
csv_file = f.readlines()
data_table = [] # create a "table" or a list of lists
# initilize a value to keep track of line lengths
# also come up with a method to determine if line lengths change
# as you loop row by row
line_min = 0  # store the min number of cells per line/row
line_max = 0  # store the max number of cells per line/row
line_len = 0  # store the length of each line
len_rows = [] # store all the length of rows in the data set.
row_ref = []  # store the row numbers in a list
all_rows = [] # store all the data as a list of lists 
col_sel = []  # a reorganization of the data where only user selected columns are captured
all_cols = [] # store all columns the use wants in a list
head_sel = [] # get all the str versions of the headers
row_chang = []# store where row length changes

for ln, line in enumerate(csv_file):
    # create a list to temporarily store all cells in a row
    # later this list will be appended to another list
    line_list = []

    # loop through all the elements in a row and append them 
    for en in line.split(','):
        line_list.append(en)
    all_rows.append(line_list)
    LofL = len(line_list)
    row_ref.append(ln)
    len_rows.append(LofL)
    # find the total number of cells per row and find the row with
    # the most cells.

    # for the first row just get number of cells in that row to intialize things
    if ln == 0:
        #isinstance()
        # store the header (maybe have an arg that states if "true"
        # store the header to be printed.
        header = line_list
        LofL = len(header)
        line_max = LofL
        line_min = LofL
        # if col references were given header names and not references
        # then find the col number.
        # first make sure the header names entered by the user exist in the file
        # if one doesn't exits print an error.
    # if the current row was longer than the previous row make note of it
    elif LofL > line_len:
        line_max = LofL
        line_len = LofL
        row_chang.append(ln)
    # if the current row was shorter than the previous row make a note of it
    elif LofL < line_len:
        line_min = LofL
        line_len = LofL
        row_chang.append(ln)
    #print(line_list)
    # if an argument was passed for columns then being extracting 
    # the desired columns.
    # loop through all rows to "grab" specific columns. If more than one column
    # requested by the user then make sure output format is the same as the input
    # file
    if args.coln is not None:
        c_row = [] # a list to contain all the cell values for the columns the user wants.
        for c, cs in enumerate(args.coln):
            # if the arg passed is an integer don't bother looking 
            # in the header list for a matching header to get the header
            # location.
            if isinstance(cs, int) == True:
                # if canBeInt(cs) or canBeFlt(cs):
                if cs < len(header):
                    c_row.append(line_list[args.coln[c]])            
            else:
            # check to see if the user enter header exists in the data set.     
                if any(cs in header for s in header):
                    args.coln[c] = header.index(cs) # having this here is a little inefficient.
                    c_row.append(line_list[args.coln[c]])            
        all_cols.append(c_row)                
        # print(c_row, '\n')
        # still need an error if integers outside of header range, 
        # misspelled headers, or non-names are entered
#min_len =  reduce(lambda x, y: min(x,y), line_len)
# print(args.coln)
# print the header
print('printing header:')
print(header)
print() # print additional line to space things out
# print general features of the csv to the prompt.
print('number of columns: ', LofL)
print('number of rows: ', ln)
print('max number of cells in a row: ', line_max)
print('min number of cells in a row: ', line_min)
print() # print additional line to space things out

# print the rows called from row args
# tell the user if there were no rows selected
if args.rown is not None:
    for pr in args.rown:
        if pr > len(all_rows):
            print(pr, 'This row subscript is out of bounds')
        else:
            print('printing row ', pr)
            print('This row is',all_rows[pr], 'cells long')
            print(all_rows[pr])
            print()
else:
    print('No Rows selected')


#min_len = min(line_len, key = ft.)
coln_ref = []
# this loops through and removes all the out of bound subscripts that 
# the user may use as input
# it also creates header names 
if args.coln is not None:
    for c, cs in enumerate(args.coln):
        # check to see if the user enter header exists in the data set. 
        if any(cs in header for s in header) or canBeInt(cs):
            # check to see if any of the subscripts are out of bounds
            if cs < len(header):
                # having this here is a little inefficient.
                head_sel.append(header[cs])
                coln_ref.append(cs)
                # print(coln_ref)
            else:
                print()
                print(cs, '--> This column subscript is out of bounds')
                print()
        else:
            print(args.coln[c], 'is not a header')
            

if args.coln is None:
    print('No Columns selected')
    print()
else:
    print('\n') # print additional line to space things out
    # here determine the column data type.
    # if the data type is a character, print only the first 10 unique enteries
    # If the type is a "date" print the range of days.
    # Also need something to catch NA's, NaN's, and -9999
    # print(head_sel)
    for c, cs in enumerate(coln_ref):
        isIntCount = 0   # count the integers in a column
        isNACount = 0    # count the NA's in a column
        isOtherCount = 0 # count all other data types 
        emptyCount = 0   # count the number of empty cells
        floatCount = 0   # count number of float numbers in data set
        isNumber = 0     # count the number of ints or floats in data set
        for rn, r in enumerate(all_cols):
            if rn == 0:
                # grab header here
                head_row = r
            # check to see if the cell contains a number (int or float)
            elif canBeInt(r[c]) or canBeFlt(r[c]):
                ## write a test here to make sure non-numeric don't get past here
                isNumber = isNumber + 1
                # check to see if the cell is empty
                if not r[c]:
                    emptyCount = emptyCount + 1
                # check to see if value is an int
                elif isinstance(intfloat(r[c]), int): ## another place to test a str? though 
                                                  ## theorhetically a test shouldn't get past here
                    isIntCount = isIntCount + 1
                else:
                    # check to see if the value is a float                    
                    floatCount = floatCount + 1
            # is there a not a number, NA or -9999 place holder?
            elif r[c] == 'NA' or r[c] == 'NaN' or r[c] == '-9999': ## a test can be written here.
                isNACount = isNACount + 1
            # check to see if the cell is empty
            elif not r[c]:
                emptyCount = emptyCount + 1
                # other character/string variables            
            else:
                isOtherCount = isOtherCount + 1
        print()
        # print out the total numer data types from each of the the columns 
        print('some characteristics of the', head_sel[c], 'column') 
        print('There are', isIntCount, 'Integers')
        print('There are', floatCount, 'Floats')
        print('There are', isNumber, 'cells with numerics')
        print('There are', isNACount, 'NA cells')
        print('There are', emptyCount, 'empty cells')
        print('There are', isOtherCount, 'Other Data types (strings)')
    print('\n') # print additional line to space things out

if line_max != line_min:
    print('some rows have more rows than others, \n check for missing or extra commas')
    print()
    print('These rows have different numbers of cells relative to others')
    print()
    print('These are the row numbers where row length changes:', row_chang)
    print()
    print('If you see row 1 listed, this means the first row has a different length than the header.')
    print()

f.close()
print('Closed file:', args.file[0])


# Do the doctests to make sure the functions are working properly
if __name__ == '__main__':
    import doctest
    doctest.testmod()
