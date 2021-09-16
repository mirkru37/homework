import numpy as np


def generate_random_int_arr(size):
    return np.random.randint(0, 100, size)


def input_int_array_manually(size):
    array = []
    print(f"Enter {size} elements of array:")
    i = 0
    while i < size:
        ele = input_int(f"{i + 1}: ")
        i += 1
        array.append(ele)
    return array


def input_int(message):
    try:
        val = int(input(message))
    except ValueError:
        print("Invalid value. Try again!!")
        return input_int(message)
    return val


def input_upper_zero_num(message):
    res = input_int(message)
    if res <= 0:
        # raise ValueError("Invalid array size")
        print("You've entered wrong value. Try again!!")
        return input_upper_zero_num(message)
    return res


def swap_half_arr(array):
    array = np.array_split(array, 2)
    array[0], array[1] = array[1], array[0]
    array = np.concatenate(array, axis=0)
    return array


n = input_upper_zero_num("Enter array size: ")
arr = generate_random_int_arr(n * 2)
# arr = input_int_array_manually(n * 2)
print("Before: ", arr)
arr = swap_half_arr(arr)
print("After: ", arr)
