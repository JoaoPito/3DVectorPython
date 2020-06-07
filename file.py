import numpy as np

lineSize = 128#max size of lines in obj files

def OpenFile(fileName):
    print("Opening {}...".format(fileName))
    file = open(fileName)
    return ParseFile(file)


#Returns an array of vertices and an array of triangles
def ParseFile(file):
    vertBuffer = np.array(())#Vertices buffer(1xN)
    triBuffer = np.array(())#Triangles buffer(1xN)

    for line in file:
        vi = 0 #vertex index

        if line[0] == 'v':#Vertices
            vecBuffer = np.fromstring(line[2:],sep = ' ')#Vector buffer independent of the content(vert or tri)
            vecBuffer = np.append(vecBuffer,np.ones(1))
            vertBuffer = np.append(vertBuffer,vecBuffer)

        if line[0] == 'f':#Triangles
            vecBuffer = np.fromstring(line[2:],dtype = int,sep = ' ')#Numpy has a builtin function for converting str into nparrays
            triBuffer = np.append(triBuffer,vecBuffer)
    
    vertBuffer = vertBuffer.reshape(int(len(vertBuffer)/4),4)
    triBuffer = triBuffer.reshape(int(len(triBuffer)/3),3).astype(int)#it is converted to int because its used as index 

    print(str(vertBuffer.shape[0]) + " vertices")
    print(str(triBuffer.shape[0])  + " triangles")
                    
    return vertBuffer, triBuffer


