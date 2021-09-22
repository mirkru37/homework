import numpy as np


def generate_random_int_arr(a, b, size):
    return np.random.randint(a, b, size)


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
        # raise ValueError("Invalid array size")
        print("You've entered wrong value. Try again!!")
        return input_upper_zero_int(message)
    return res


def print_matrix(matrix):
    for row in matrix:
        print(row)


def is_palindrome(row):
    n = len(row)
    for i in range(int(n / 2)):
        if row[i] != row[n - 1 - i]:
            return False
    return True


def palindrome_rows_index(rows):
    rows_index = []
    for i, row in enumerate(rows):
        if is_palindrome(row):
            rows_index.append(i)
    return rows_index


def auto_matrix(a, b, n):
    matrix = []
    for i in range(n):
        matrix.append(generate_random_int_arr(a, b, n))
    return matrix


def is_int(num):
    try:
        int(num)
        return True
    except ValueError:
        return False


def fill_matrix_by_rows(n):
    matrix = []
    print("Please enter numbers separating by ' '.\n "
          "All wrong or extra value will be removed.\n "
          "If your row will be shorter than N or empty, it will be automatically filled with duplicate of first element")
    for i in range(n):
        row = [num for num in input(f"Enter row {i + 1}: ").split() if is_int(num)]
        row = np.resize(row, n)
        matrix.append(row)
    return matrix


def fill_matrix_manual(n):
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(input_int(f"Enter [{i + 1}][{j + 1}] element: "))
        matrix.append(row)
    return matrix


def menu(n):
    print("Please choose how to fill matrix: ", "1-auto fill", "2-fill by rows", "3-fill by elements", "4-exit",
          sep="\n")
    option = input("-->").strip()
    matrix = []
    if option == '1':
        a = input_int("Please input a: ")
        b = input_int("Please input b: ")
        if a > b:
            a, b = b, a
        matrix = auto_matrix(a, b, n)
    elif option == '2':
        matrix = fill_matrix_by_rows(n)
    elif option == '3':
        matrix = fill_matrix_manual(n)
    elif option == '4':
        exit()
    else:
        print("Wrong option!")
        menu(n)
        return
    print("Your matrix:")
    print_matrix(matrix)
    result = palindrome_rows_index(matrix)
    if not result:
        print("There is no palindrome rows!")
    else:
        print("Palindrome rows index: ", result)


n = input_upper_zero_int("Please input N: ")
menu(n)
