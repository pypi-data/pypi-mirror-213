from libcythonconst.lsum cimport lsum

def plus_1(a):
    return lsum(a, 1)
