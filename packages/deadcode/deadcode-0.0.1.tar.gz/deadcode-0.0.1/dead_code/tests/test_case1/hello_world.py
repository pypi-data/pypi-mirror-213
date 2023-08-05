import sys

unused_global_variable = True
ANOTHER_GLOBAL_VARIABLE = "This variable is unused"
third_global_varialbe = 12 * 25

THIS_ONE_IS_USED = "World"


def unused_function():
    print(f"Unused function {THIS_ONE_IS_USED}")
    print(third_global_varialbe)


class UnusedClass(object):
    pass


class AnotherUnusedClass:
    def __init__(self):
        pass

