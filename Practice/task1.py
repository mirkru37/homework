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


def gen_comb(arr, max_size, it, elements):
    new_arr = []
    if len(arr) != 0:
        for i in range(0, len(arr)):
            for j in elements:
                new_arr.append(arr[i] * 10 + j)
    else:
        new_arr = elements
    if it < max_size - 1:
        new_arr += gen_comb(new_arr, max_size, it + 1, elements)
    return new_arr


n = input_upper_zero_num("Enter N>0: ")
correct_nums = [x for x in gen_comb([], len(str(n)), 0, [4, 7]) if x <= n]
print(correct_nums)
