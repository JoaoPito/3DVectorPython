import math

def norm(u,v):#Calculate norm( or length) of vector u and v
    mult = 0

    for i in range(len(u)):
        mult = mult + (u[i]*v[i])

    ret = math.sqrt(mult)
    return ret

def normalise(v):
    n = norm(v,v)

    outVector = v / n

    return outVector


def subt_tuple(x,y):#Subtract vectors
    ret = tuple(map(lambda i, j: i - j, x, y)) 
    return ret

def line(a, b):
    ab = subt_tuple(b,a)
    n_ab = norm(ab,ab)

    return ab,n_ab