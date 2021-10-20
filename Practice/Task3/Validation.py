def is_num(n):
    try:
        float(n)
        return True
    except ValueError:
        return False


def is_path(path):
    try:
        open(path)
        return True
    except FileNotFoundError:
        return False
