#3D Rendering Engine 
#2020, Joao Pito

import math 
import numpy as np 

import screen_Draw as screen
import geometry as geom
import file

import time #Mark elapsed time
import sys #Get arguments (main.py fileName nImages resolutionX resolutionY) 

#Rendering
nImages = int(sys.argv[2])
wireframe = False #Render wireframe

fNear = 0.1#Near clip plane
fFar = 1000.0#Far clip plane
fFov = 90.0#FOV angle
fAspRatio = screen.res[1]/screen.res[0]
fFovRad = 1.0 / math.tan(fFov * 0.5 / 180.0 * math.pi)

#Obj Properties
fileName = "Objects\cube.obj"

objColor = (255,255,255)#The color of the object

objRot = (0.0, 0.0, math.pi)#current rotation
objPos = (0.0, 0.0, 3.0, 0.0)#current postion

#Camera
#If the object comes to close to the camera weird things will happen
camPos = np.array((0.0,0.0,0.0))#Position
camDir = np.array((0.,0.,-1.0))#Direction the camera is looking at

#Illumination
lightDir = (1.0,0.0,-1.0)

#Algebra Functions(Goes to geometry.py)
#Projection Matrix
projMat = np.array(((fAspRatio * fFovRad, 0.0,     0.0,                              0.0),
                   (0.0,                  fFovRad, 0.0,                              0.0),
                   (0.0,                  0.0,      fFar / (fFar - fNear),           1.0),
                   (0.0,                  0.0,      (-fFar * fNear) / (fFar - fNear),0.0)))

def ProjectTri(tri):
    nTri = np.array((tri[0],tri[1],tri[2]))
    projTri = np.zeros(nTri.shape)
    for i in range(tri.shape[0]):
        #Project the triangle into 2D
        projTri[i] = MatrixVectorMult(nTri[i],projMat)

        #Scale so it fits into view (last step)
        projTri[i][0] = (projTri[i][0] + 1.0) * 0.5 * screen.res[0]#clamped and multiplied x with screen width
        projTri[i][1] = (projTri[i][1] + 1.0) * 0.5 * screen.res[1]#clamped and multiplied y with screen height
    
    return projTri

def MatrixVectorMult(v,m):#vector * matrix(divides x1,x2,x3 by x4)
    outVector = np.matmul(v,m)
    w = outVector[3]

    if(w > 0.1):
        outVector[0] = outVector[0]/w
        outVector[1] = outVector[1]/w
        outVector[2] = outVector[2]/w
    
    return outVector

#Translate vector i in the vector v(3D vectors)
def TranslateVector(i,v):
    translMatrix = np.array(((1.0,0.0,0.0,v[0]),
                             (0.0,1.0,0.0,v[1]),
                             (0.0,0.0,1.0,v[2]),
                             (0.0,0.0,0.0,1.0),))

    outVector = np.matmul(translMatrix,i)
    return outVector

#Rotates vector v around angle rot vector r
def RotateVector(v,r):

    XRotMat = np.array(((1.0,0.0,               0.0,           0.0),
                        (0.0,math.cos(r[0]),    -math.sin(r[0]),0.0),
                        (0.0,math.sin(r[0]),    math.cos(r[0]),0.0),
                        (0.0,0.0,               0.0,           1.0)))

    YRotMat = np.array(((math.cos(r[1]), 0.0,math.sin(r[1]),0.0),
                        (0.0,            1.0,0.0,           0.0),
                        (-math.sin(r[1]),0.0,math.cos(r[1]),0.0),
                        (0.0,0.0,        0.0,               1.0)))

    ZRotMat = np.array(((math.cos(r[2]), -math.sin(r[2]), 0.0,0.0),
                        (math.sin(r[2]),  math.cos(r[2]), 0.0,0.0),
                        (0.0,                       0.0,  1.0,0.0),
                        (0.0,                       0.0,  0.0,1.0)))

    vector = MatrixVectorMult(v,XRotMat)#Rotate in the X axis
    vector = MatrixVectorMult(vector,YRotMat)#Rotate in the Y axis
    vector = MatrixVectorMult(vector,ZRotMat)#Rotate in the Z axis
    
    
    return vector

fileName = sys.argv[1]
loadedVerts, loadedTris = file.OpenFile(fileName)

#Main render routine (Goes to screen_draw.py)
def RenderUpdate():

    #Painters algorithm, doesnt work very well the way its implemented here
    sortedTris = loadedTris[np.argsort(-loadedTris[:, 2])]

    for triInd in range(sortedTris.shape[0]):
        a = sortedTris[triInd][0] - 1 #Tri vertices index
        b = sortedTris[triInd][1] - 1 
        c = sortedTris[triInd][2] - 1 
        Tri = np.array((loadedVerts[a],loadedVerts[b],loadedVerts[c]))
        
        #Apply Transformations to the mesh
        nTri = np.zeros((3,4))
        #projTri = np.zeros((3,4))

        for i in range(Tri.shape[0]):
            #Apply Rotations
            nTri[i] = RotateVector(Tri[i],objRot)

            #Translates the cube's triangles so its a bit farther away from the camera(DEBUG)
            nTri[i] = TranslateVector(nTri[i],objPos)

        #Calculates the normal vector
        AB = nTri[1][:3] - nTri[0][:3]#3D vector
        AC = nTri[2][:3] - nTri[0][:3]        
        normal = np.cross(AB,AC)
        norm = geom.norm(normal,normal)
        normal /= norm        

        #Calculates dot product for the normal and the camera pointing at the obj
        #This is used to know if its supposed to draw a tri or not
        CamNormalDot = np.dot(normal,(nTri[0][:3] - camPos)) #Line between the camera and the object        

        if(CamNormalDot < 0.0):
            #Calculates illumination on the triangle
            LightNormalDot = np.dot(normal,lightDir)
            color = ((int)(objColor[0]*(LightNormalDot)),(int)(objColor[1]*(LightNormalDot)),(int)(objColor[2]*(LightNormalDot)))

            #Apply Projection
            nTri = ProjectTri(nTri)            
            screen.fillTriangle(nTri,color)

        #Draws Wireframe
        if(wireframe):
            #Calculates illumination on the triangle
            LightNormalDot = np.dot(normal,lightDir)
            color = ((int)(objColor[0]*(LightNormalDot)),(int)(objColor[1]*(LightNormalDot)),(int)(objColor[2]*(LightNormalDot)))

            #Apply Projection
            nTri = ProjectTri(nTri)
            screen.triangle(nTri,(255,255,255))#Wireframe

#Start Routine
def Start():
    print("Generating " + str(nImages) + " images")
            
#Execute
Start()

#Parameters being updated after each image
for u in range(nImages):
    screen.clearImg()
    RenderUpdate()

    #Rotates and Translates the object
    objRot = (objRot[0] , objRot[1] + 0.03, objRot[2] )
    #objPos = (objPos[0], objPos[1] + 0.03, objPos[2]) 

    #Changes the light direction
    lightDir = (lightDir[0] - 0.01,lightDir[1] ,lightDir[2])

    imgName = "ImgBuffer\img_{}.png"
    screen.img.save(imgName.format(u))    

print("Elapsed time (sec): {}".format(time.thread_time()))
print("Done!")
