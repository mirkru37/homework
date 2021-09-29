import numpy as np
import random

sort_iterations = 0


def print_matrix(matrix, message=''):
    print(message)
    for row in matrix:
        print(row)


def get_menu_option(message=""):
    print(message)
    return input("-->").strip()


def get_middle_in_matrix(start, end, columns):
    if start == end or \
            (start[0] == end[0] and end[1] - start[1] == 1) or \
            (start[1] == columns and end[1] == 0 and end[0] - start[0] == 1):
        return end
    add = ((end[0] * columns + end[1] + 1) - (start[0] * columns + start[1] + 1)) // 2
    # mid = start[0] * columns + start[1] \
    #       + (end[0] * columns + end[1] - start[0] * columns + start[1]) // 2
    return move_matrix_index(start, add, columns)


def move_matrix_index(ij, index, columns):
    ij = ij.copy()
    ij[1] += index
    ij[0] += ij[1] // columns
    ij[1] = ij[1] % columns
    return ij


def is_num(x):
    try:
        float(x)
        return True
    except ValueError:
        return False


def close(*_):
    exit()


def invalid_option(*_):
    print("Invalid choice!!")
    raise ValueError("Invalid menu option")


def compare_num_with_string(a, b, compare=lambda a, b: a == b):
    if not is_num(a) or not is_num(b):
        return compare(str(a), str(b))
    return compare(float(a), float(b))


def partition(start, end, array):
    global sort_iterations
    pivot_index = start
    pivot = array[pivot_index]
    while start < end:
        while start < len(array) and compare_num_with_string(array[start], pivot, lambda a, b: a <= b):
            start += 1
        while compare_num_with_string(array[end], pivot, lambda a, b: a > b):
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


def auto_matrix(n, m, range_):
    matrix = []
    for i in range(n):
        matrix.append(generate_random_arr(m, range_))
    return matrix


def fill_matrix_by_rows(data):
    n, m = data[0], data[1]
    matrix = []
    print("Please enter numbers separating by ' '.\n "
          f"If your row will be shorter than {m} or empty,"
          " it will be automatically filled with duplicate of first element")
    for i in range(n):
        row = [num for num in input(f"Enter row {i + 1}: ").split()]
        row = np.resize(row, m)
        matrix.append(row)
    return matrix


def fill_matrix_manual(data):
    n, m = data[0], data[1]
    matrix = []
    for i in range(n):
        row = []
        for j in range(m):
            row.append(input(f"Enter [{i + 1}][{j + 1}] element: "))
        matrix.append(row)
    return matrix


def search_in_matrix(matrix, element, end=None, start=None):
    rows = len(matrix)
    columns = len(matrix[0])
    if start is None or start < [0, 0]:
        start = [0, 0]
    if end is None or end > [rows - 1, columns - 1]:
        end = [rows - 1, columns - 1]

    ij = start
    iterations = 0
    while start <= end:
        ij = get_middle_in_matrix(start, end, columns)
        iterations += 1
        if compare_num_with_string(matrix[ij[0]][ij[1]], element):
            break
        elif compare_num_with_string(matrix[ij[0]][ij[1]], element, lambda a, b: a > b):
            end = move_matrix_index(ij, -1, columns)
        else:
            start = move_matrix_index(ij, 1, columns)
    if start > end:
        ij = [-1, -1]
    return ij[0], ij[1], iterations


def search(matrix):
    element = input("Enter the element: ")
    i, j, it = search_in_matrix(matrix, element)
    if i == -1 or j == -1:
        print("There is no such element!")
    else:
        print(f"Element in [{i}][{j}]")
    print(f"Search iterations: {it}")
    menu(menu_search, matrix, "Please choose what to do:")


def fill_matrix_auto(data):
    n, m = data[0], data[1]
    range_, back = input_range()
    if back or not range_:
        if not back:
            print("Empty range. Try again!")
        return menu(menu_fill, [n, m], "Please choose how to fill matrix:")
    return auto_matrix(n, m, range_)


def menu(template, data, greet_message='', message_for_get=''):
    print(greet_message)
    for key in template:
        print(f"{key}: {template[key][0]}")
    option = get_menu_option(message_for_get)
    try:
        return template.get(option, [None, invalid_option])[1](data)
    except ValueError:
        return menu(template, data, greet_message, message_for_get)


menu_fill = {
    "1": ("Auto fill", fill_matrix_auto),
    "2": ("Fill by rows", fill_matrix_by_rows),
    "3": ("Fill manually", fill_matrix_manual),
    "4": ("Exit", close)
}

menu_search = {
    "1": ("Search", search),
    "2": ("Exit", close)
}

n = input_upper_zero_int("Please input N: ")
m = input_upper_zero_int("Please input M: ")
matrix = menu(menu_fill, [n, m], "Please choose how to fill matrix:")
print_matrix(matrix, "Your matrix: ")
matrix = sort_matrix(matrix)
print(f"Iterations for sorting: {sort_iterations}")
print_matrix(matrix, "Sorted matrix: ")
menu(menu_search, matrix, "Please choose what to do:")
