#reading file
import pprint
import copy

# This program is a sudoku solver
# made for this problem https://projecteuler.net/problem=96
# The text file sudoku.txt contains fifty different Su Doku puzzles
# ranging in difficulty, but all with unique solutions

# Reading in sudokus, stripping whitespaces, formatting
file = open("p096_sudoku.txt", "r")
sudoku_str =  file.read()
sudoku_str = sudoku_str.replace("\"","")
sudoku_lis = sudoku_str.split("Grid ")
sudoku_lis=sudoku_lis[1:]
for sudoku in range(len(sudoku_lis)):
    sudoku_lis[sudoku]=sudoku_lis[sudoku][2:]
    sudoku_lis[sudoku]=sudoku_lis[sudoku].split("\n")
    # remove line break after each sudoku but the last
    if sudoku!=49:
        sudoku_lis[sudoku]=sudoku_lis[sudoku][1:-1]
    else:
         sudoku_lis[sudoku]=sudoku_lis[sudoku][1:]
        

print(len(sudoku_lis))

# init array with all the numbers that are still possible for each cell
# if nothing is there, at the beginning every number from 1  to 9 is possible
# else the number is already given and we take that
def fill_with_lists_of_posible_nums(sudoku):
 possible =[[[]for i in range(9)] for j in range(9)]
 for row in range(9):
    for column in range(9):
        if sud[row][column]!='0':
            possible[row][column]=sud[row][column]
        else:
            possible[row][column]='123456789'
 return possible
        
        
#cancel values in same row
def cli(possible):
 for row in range(9):
    nums_in_line=[]
    wholeline=""
    for column in range(9):
        el=possible[row][column]
        # if exactly 1 number is possible, it must be in the line
        if len(el)==1:
            nums_in_line.append(el)
    for column in range(9):        
        if len(possible[row][column])!=1:
            for k in nums_in_line:
                possible[row][column] = possible[row][column].replace(k,"")
        wholeline += possible[row][column]
    for anumber in range(1,10):
        if wholeline.count(str(anumber)) ==1:
            for column in range(9):
                if str(anumber) in possible[row][column]:
                    possible[row][column]=str(anumber)
            

        
#cancel values in same column
def csp(av):
 for j in range(9):
    inl=[]
    wholeline=""
    for i in range(9):
        el=av[i][j]
        if len(el)==1:
            inl.append(el)
    for i in range(9):        
        if len(av[i][j])!=1:
            for k in inl:
                av[i][j] = av[i][j].replace(k,"")
        wholeline += av[i][j]
    for anumber in range(1,10):
        if wholeline.count(str(anumber)) ==1:
            for i in range(9):
                if str(anumber) in av[i][j]:
                    av[i][j]=str(anumber)
               


#cancel values in same square
def cq(av):
 inq=[]
 wholeq=[]
 for q in range(9):
    inq.append([])
    wholeq.append("")
 for i in range(9):
    for j in range(9):
        q=divmod(i,3)[0]*3+divmod(j,3)[0]
        if len(av[i][j]) ==1:
            inq[q].append(av[i][j])

 for i in range(9):
    for j in range(9):
        q=divmod(i,3)[0]*3+divmod(j,3)[0]
        if len(av[i][j]) !=1:
             for k in inq[q]:
                 av[i][j] = av[i][j].replace(k,"")
        wholeq[q] += av[i][j]
 for i in range(9):
    for j in range(9):
        q=divmod(i,3)[0]*3+divmod(j,3)[0]
        for anumber in range(1,10):
            if wholeq[q].count(str(anumber)) ==1:
               for i2 in range(9):
                   for j2 in range(9):
                       q2=divmod(i2,3)[0]*3+divmod(j2,3)[0]
                       if q2==q and str(anumber) in av[i2][j2]:
                         av[i2][j2]=str(anumber)

#try out choosing a value and see if it solves
def prob(av):
 backup=copy.deepcopy(av)
 for i in range(9):
    for j in range(9):
        av=copy.deepcopy(backup)
        if len(av[i][j])==2:               
               av[i][j]=av[i][j][0]
               if solve(av)==1:
                   #pprint.pprint(av)
                   return av              
               else:
                    av=copy.deepcopy(backup)
                    av[i][j]=av[i][j][1]
                    if solve(av)==1:
                        #pprint.pprint(av)
                        return av

 
                 
def count(av):
    ssum=0
    for i in range(9):
        for j in range(9):
            if len(av[i][j]) ==1:
                ssum+=1
    return ssum




def solve(av):
    x=0
    while count(av)>x:
        x=count(av)
        cli(av)
        csp(av)
        cq(av)
    if count(av)==81:
        return 1

    else:
        return 0

answer = 0
for i in range(50):
    print("Sudoku ",i)
    sud=sudoku_lis[i]
    av=fill_with_lists_of_posible_nums(sud)
    if solve(av)==1:                    
        #pprint.pprint(av)
        print("\n\n")
    else:
        #pprint.pprint(av)
        av = prob(av)
    num=int(av[0][0]+av[0][1]+av[0][2])
    print(num)
    answer+=num

print(answer)
