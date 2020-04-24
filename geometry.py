import math

def norm(u,v):#Calculate norm of vector v
    mult = (u[0]*v[0])+(u[1]*v[1])
    ret = math.sqrt(mult)
    return ret

def subt_tuple(x,y):#Subtract vectors
    ret = tuple(map(lambda i, j: i - j, x, y)) 
    return ret