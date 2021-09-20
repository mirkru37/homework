import numpy as np
import random

sort_iterations = 0


def partition(start, end, array):
    global sort_iterations
    pivot_index = start
    pivot = array[pivot_index]
    while start < end:
        while start < len(array) and compare_num_with_string(array[start], pivot, lambda a, b: a <= b):
            start += 1
        while compare_num_with_string(array[end], pivot, lambda a, b: a > b):
            sort_iterations += 1
            end -= 1
        if start < end:
            sort_iterations += 1
            array[start], array[end] = array[end], array[start]
    sort_iterations += 1
    array[end], array[pivot_index] = array[pivot_index], array[end]
    return end


def quick_sort(start, end, array):
    if start < end:
        p = partition(start, end, array)
        quick_sort(start, p - 1, array)
        quick_sort(p + 1, end, array)


def generate_random_arr(size, range_):
    arr = []
    for i in range(size):
        arr.append(random.choice(range_))
    return arr


def input_int(message):
    try:
        val = int(input(message))
    except ValueError:
        print("Invalid value. Try again!!")
        return input_int(message)
    return val


def input_upper_zero_int(message):
    res = input_int(message)
    if res <= 0:
        print("You've entered wrong value. Try again!!")
        return input_upper_zero_int(message)
    return res


def print_matrix(matrix):
    for row in matrix:
        print(row)


def auto_matrix(n, m, range_):
    matrix = []
    for i in range(n):
        matrix.append(generate_random_arr(m, range_))
    return matrix


def fill_matrix_by_rows(n, m):
    matrix = []
    print("Please enter numbers separating by ' '.\n "
          f"If your row will be shorter than {m} or empty,"
          " it will be automatically filled with duplicate of first element")
    for i in range(n):
        row = [num for num in input(f"Enter row {i + 1}: ").split()]
        row = np.resize(row, m)
        matrix.append(row)
    return matrix


def fill_matrix_manual(n, m):
    matrix = []
    for i in range(n):
        row = []
        for j in range(m):
            row.append(input(f"Enter [{i + 1}][{j + 1}] element: "))
        matrix.append(row)
    return matrix


def input_range():
    option = get_menu_option("1-enter array of available values"
                             "\n2-enter borders"
                             "\n3-return")
    if option == '1':
        print("Enter values:")
        range_ = input().split()
    elif option == '2':
        a = input_int("Enter A: ")
        b = input_int("Enter B: ")
        if a > b:
            a, b = b, a
        range_ = range(a, b)
    elif option == '3':
        return [], True
    else:
        print("Wrong option!")
        return input_range()
    return range_, False


def row_sort(matrix):
    for i in matrix:
        quick_sort(0, len(i) - 1, i)
    return matrix


def column_sort(matrix):
    matrix = np.transpose(matrix)
    for i in matrix:
        quick_sort(0, len(i) - 1, i)
    matrix = np.transpose(matrix)
    return matrix


def top_down(matrix):
    global sort_iterations
    is_sorted = True
    n = len(matrix)
    m = len(matrix[0])
    for i in range(1, n):
        for j in range(m // 2):
            if matrix[i][j] < matrix[i - 1][m - j - 1]:
                sort_iterations += 1
                matrix[i][j], matrix[i - 1][m - j - 1] = matrix[i - 1][m - j - 1], matrix[i][j]
                is_sorted = False
    return is_sorted


def top_down_sort(matrix):
    for _ in matrix:
        is_sorted = top_down(matrix)
        if is_sorted:
            break
        else:
            matrix = row_sort(matrix)
    return matrix


def sort_matrix(matrix):
    global sort_iterations
    sort_iterations = 0
    matrix = row_sort(matrix)
    matrix = column_sort(matrix)
    matrix = top_down_sort(matrix)
    return matrix.tolist()


def get_menu_option(message):
    print(message)
    return input("-->").strip()


def get_middle(start, end):
    return start + (end - start) // 2


def is_num(x):
    try:
        float(x)
        return True
    except ValueError:
        return False


def compare_num_with_string(a, b, compare):
    if not is_num(a) or not is_num(b):
        return compare(str(a), str(b))
    return compare(float(a), float(b))


def search_in_matrix(matrix, element, end=None, start=None):
    if start is None:
        start = [0, 0]
    if end is None:
        end = [len(matrix)-1, len(matrix[0])-1]
    # find row
    i = start[0]
    while i <= end[0] and i < len(matrix):
        if compare_num_with_string(matrix[i][end[1]], element, lambda a, b: a >= b):
            break
        i += 1
    if i > end[0] or i >= len(matrix):
        return -1, -1
    # find column
    while start[1] <= end[1]:
        j = get_middle(start[1], end[1])
        if compare_num_with_string(matrix[i][j], element, lambda a, b: a == b):
            return i, j
        elif compare_num_with_string(matrix[i][j], element, lambda a, b: a > b):
            end[1] = j-1
        else:
            start[1] = j+1
    return -1, -1


def menu_binary_search(matrix):
    option = get_menu_option("Please choose what to do\n1-search\n2-exit")
    if option == '1':
        element = input("Enter the element: ")
        i, j = search_in_matrix(matrix, element)
        if i == -1 or j == -1:
            print("There is no such element!")
        else:
            print(f"Element in [{i}][{j}]")
        menu_binary_search(matrix)
    elif option == '2':
        exit()
    else:
        print("Wrong option!")
        menu_binary_search(matrix)
        return


def menu_fill(n, m):
    option = get_menu_option("Please choose how to fill matrix: \n1-auto fill\n2-fill by rows\n3-fill by "
                             "elements\n4-exit")
    matrix = []
    if option == '1':
        range_, back = input_range()
        if back or not range_:
            if not back:
                print("Empty range. Try again!")
            menu_fill(n, m)
            return
        matrix = auto_matrix(n, m, range_)
    elif option == '2':
        matrix = fill_matrix_by_rows(n, m)
    elif option == '3':
        matrix = fill_matrix_manual(n, m)
    elif option == '4':
        exit()
    else:
        print("Wrong option!")
        menu_fill(n, m)
        return
    print_matrix(matrix)
    matrix = sort_matrix(matrix)
    print(f"Iterations for sorting: {sort_iterations}")
    print("Sorted matrix: ")
    print_matrix(matrix)
    menu_binary_search(matrix)


n = input_upper_zero_int("Please input N: ")
m = input_upper_zero_int("Please input M: ")
menu_fill(n, m)
