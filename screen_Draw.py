from PIL import Image
import geometry as geom
400
#Create image
res = (800,600)#Resolution
img = Image.new('RGB',res)
pixels = img.load()

def edges(v,e):
    for i in range(len(e)):
        v_a = e[i][0]
        v_b = e[i][1]
        line(v[v_a],v[v_b],(255,255,255))

def line(a, b, color):#Draw a line between a and b with color 

    ab = geom.subt_tuple(b,a)
    
    n_ab = geom.norm(ab,ab)

    r_n_ab = round(n_ab)
    for i in range(r_n_ab):
        p = i/r_n_ab
        v_int = (a[0] + round(ab[0] * p),a[1] + round(ab[1] * p))
        if v_int[0] < res[0] and v_int[1] < res[1]:
            pixels[v_int] = color

    return ab, n_ab
