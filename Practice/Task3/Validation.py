def is_num(n):
    try:
        float(n)
        return True
    except ValueError:
        return False
