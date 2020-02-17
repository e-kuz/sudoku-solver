# reading file
import pprint
import copy

# This program is a sudoku solver
# made for this problem https://projecteuler.net/problem=96
# The text file sudoku.txt contains fifty different Su Doku puzzles
# ranging in difficulty, but all with unique solutions

# Reading in sudokus, stripping whitespaces, formatting
file = open("p096_sudoku.txt", "r")
sudoku_str = file.read()
sudoku_str = sudoku_str.replace("\"", "")
sudoku_lis = sudoku_str.split("Grid ")
sudoku_lis = sudoku_lis[1:]
for sudoku in range(len(sudoku_lis)):
    sudoku_lis[sudoku] = sudoku_lis[sudoku][2:]
    sudoku_lis[sudoku] = sudoku_lis[sudoku].split("\n")
    # remove line break after each sudoku but the last
    if sudoku != 49:
        sudoku_lis[sudoku] = sudoku_lis[sudoku][1:-1]
    else:
        sudoku_lis[sudoku] = sudoku_lis[sudoku][1:]



# init array with all the numbers that are still possible for each cell
# if nothing is there, at the beginning every number from 1  to 9 is possible
# else the number is already given and we take that
def fill_with_lists_of_posible_nums(sudoku):
    possible = [[[] for i in range(9)] for j in range(9)]
    for row in range(9):
        for column in range(9):
            if sudoku[row][column] != '0':
                possible[row][column] = sudoku[row][column]
            else:
                possible[row][column] = '123456789'
    return possible


# manage numbers in same row 
def manage_row(possible):
    for row in range(9):
        nums_already_in_line = []
        whole_line = ""
        for column in range(9):
            possible_nums_for_cell = possible[row][column]
            # if exactly 1 number is possible in this cell, it must be in the line
            if len(possible_nums_for_cell) == 1:
                nums_already_in_line.append(possible_nums_for_cell)
        for column in range(9):
            # if a number is already somewhere in the line, remove it from the possible numbers for this cell
            if len(possible[row][column]) != 1:
                for k in nums_already_in_line:
                    possible[row][column] = possible[row][column].replace(k, "")
            whole_line += possible[row][column]
        # if a num only appears once in the whole line, it must be in the cell where it appears
        for anumber in range(1, 10):
            if whole_line.count(str(anumber)) == 1:
                for column in range(9):
                    if str(anumber) in possible[row][column]:
                        possible[row][column] = str(anumber)


# manage numbers in same column
def manage_column(possible):
    for column in range(9):
        nums_already_in_column = []
        whole_column = ""
        for row in range(9):
            possible_nums_for_cell = possible[row][column]
            # if exactly 1 number is possible in this cell, it must be in the column
            if len(possible_nums_for_cell) == 1:
                nums_already_in_column.append(possible_nums_for_cell)
        for row in range(9):
            # if a number is already somewhere in the column, remove it from the possible numbers for this cell
            if len(possible[row][column]) != 1:
                for k in nums_already_in_column:
                    possible[row][column] = possible[row][column].replace(k, "")
            whole_column += possible[row][column]
        # if a num only appears once in the whole column, it must be in the cell where it appears
        for anumber in range(1, 10):
            if whole_column.count(str(anumber)) == 1:
                for row in range(9):
                    if str(anumber) in possible[row][column]:
                        possible[row][column] = str(anumber)


# manage numbers in same square
def manage_square(possible):
    nums_already_in_square = []
    whole_square = []
    for square in range(9):
        nums_already_in_square.append([])
        whole_square.append("")
    for row in range(9):
        for column in range(9):
            square = (row//3) * 3 + column//3
            # if exactly 1 number is possible in this cell, it must be in the square
            if len(possible[row][column]) == 1:
                nums_already_in_square[square].append(possible[row][column])

    for row in range(9):
        for column in range(9):
            square = (row//3) * 3 + column//3
            if len(possible[row][column]) != 1:
                # if a number is already somewhere in the square, remove it from the possible numbers for this cell
                for num in nums_already_in_square[square]:
                    possible[row][column] = possible[row][column].replace(num, "")
            whole_square[square] += possible[row][column]
    for row in range(9):
        for column in range(9):
            square = (row//3) * 3 + column//3
            # if a num only appears once in the whole square, it must be in the cell where it appears
            for anumber in range(1, 10):
                if whole_square[square].count(str(anumber)) == 1:
                    #finding where it appears
                    for row2 in range(9):
                        for column2 in range(9):
                            square2 = (row2//3) * 3 + column2//3
                            if square2 == square and str(anumber) in possible[row2][column2]:
                                possible[row2][column2] = str(anumber)


# backtracking: for every cell with only 2 possible numbers
# try choosing each number and see if it solves
def backtracking_for_two_numbers(possible):
    backup = copy.deepcopy(possible)
    for row in range(9):
        for column in range(9):
            possible = copy.deepcopy(backup)
            if len(possible[row][column]) == 2:
                possible[row][column] = possible[row][column][0]
                if solve(possible) == 1:
                    return possible
                else:
                    possible = copy.deepcopy(backup)
                    possible[row][column] = possible[row][column][1]
                    if solve(possible) == 1:
                        return possible

# count how many cells with only one possible number there are
# needed for the solve function, as a sudoku is solved, when there is 1 possible number
# in all 81 cells
def count_possible(possible):
    sum_of_possible = 0
    for row in range(9):
        for column in range(9):
            if len(possible[row][column]) == 1:
                sum_of_possible += 1
    return sum_of_possible


def solve(possible):
    x = 0
    while count_possible(possible) > x:
        x = count_possible(possible)
        manage_row(possible)
        manage_column(possible)
        manage_square(possible)
    return count_possible(possible) == 81



project_euler_answer = 0
for i in range(50):
    sudoku = sudoku_lis[i]
    possible = fill_with_lists_of_posible_nums(sudoku)
    if not solve(possible):
        possible = backtracking_for_two_numbers(possible)
        
    proj_euler_sub_answer = int(possible[0][0] + possible[0][1] + possible[0][2])
    project_euler_answer += proj_euler_sub_answer
    print("Sudoku", i,": ",proj_euler_sub_answer)

print(project_euler_answer)
