from PIL import Image
import geometry as geom
import numpy as np

#Image
res = (512,512)#Resolution
img = Image.new('RGB',res)
pixels = img.load()

bkgColor = (100,100,255)#Feel free to choose the background color

#Change img resolution, CLEARS THE IMAGE
def changeRes(resolution):
    res = resolution
    img = Image.new('RGB',res)
    pixels = img.load()

    if (bkgColor != (0,0,0)): clearImg()

#set all pixels to a given color
def clearImg():
    for x in range(res[0]):
        for y in range(res[1]):
            pixels[(x,y)] = bkgColor

#Draw a line between a and b with color
def line(a, b, color):
    ab = geom.subt_tuple(b,a)
    
    n_ab = geom.norm(ab,ab)

    r_n_ab = (int)(n_ab*2)
    for i in range(r_n_ab):
        p = i/r_n_ab
        v_int = (a[0] + (int)(ab[0] * p),a[1] + (int)(ab[1] * p))
        if v_int[0] < res[0]-1 and v_int[1] < res[1]-1:
            pixels[v_int] = color

    return ab, n_ab

#Draw atriangle
def triangle(t,color):#Vertices/Triang.
    a = t[0]
    b = t[1]
    c = t[2]

    line(a,b,color)#vector AB
    line(b,c,color)#BC
    line(c,a,color)#CA


def fillTriangle(t, color):
    #It divides the triangle in 2 rectangle triangles, rasters the 1st triangle then goes to the second

    tYSorted = t[np.argsort(t[:, 1])]#Sort by y value(Bottom first)

    a = tYSorted[0]#Now they are sorted lowest Y first
    b = tYSorted[1]
    c = tYSorted[2]

    ab,n_ab = geom.line(a,b)
    bc,n_bc = geom.line(b,c)
    ca,n_ca = geom.line(a,c)    

    ab_step = 0
    bc_step = 0
    ca_step = 0

    if((int)(ca[1])!=0): ca_step = ca[0] / (float)(abs(ca[1]))

    if((int)(ab[1]) != 0):

        ab_step = ab[0] / (float)(abs(ab[1]))       

        for i in range((int)(b[1]-a[1])+1):#Loops across Y between a and b and draws half of the img
            a_ab_step = a[0] + (float)(i) * ab_step
            a_ca_step = a[0] + (float)(i) * ca_step

            #Swap if true so a_ab_step is always smaller
            if (a_ab_step > a_ca_step):
                buf = a_ab_step
                a_ab_step = a_ca_step
                a_ca_step = buf
            
            for j in range((int)(a_ca_step - (a_ab_step - 1)) + 2):
                v_int = (j + a_ab_step, i + a[1])
                
                #print("v_int: "+str(v_int)+" ab_step: " + str(ab_step)+" a_ac_step: " + str(a_ac_step) + " a_ab_step: " + str(a_ab_step))
                pixels[v_int] = color

    #Draws the other half of the triangle
    if((int)(bc[1]) != 0):

        bc_step = bc[0] / (float)(abs(bc[1]))

        for i in range((int)(c[1]-b[1])+1):

            b_bc_step = b[0] + ((float)(i) * bc_step)
            a_ca_step = a[0] + (float)(i + (b[1]-a[1])) * ca_step
        
            #Swap if true
            if (b_bc_step > a_ca_step):
                buf = b_bc_step
                b_bc_step = a_ca_step
                a_ca_step = buf

            for j in range((int)((a_ca_step - (b_bc_step - 1)) + 2)):
                v_int = (j + b_bc_step, i + b[1])
                
                #print("v_int: "+str(v_int)+" ab_step: " + str(ab_step)+" a_ac_step: " + str(a_ac_step) + " b_ab_step: " + str(b_ab_step))
                pixels[v_int] = color
