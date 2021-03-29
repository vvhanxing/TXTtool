import numpy as np

import random

def M(eX,eY,eZ):
    a1 =  np.array([eX[0],eY[0],eZ[0]])
    a2 =  np.array([eX[1],eY[1],eZ[1]])
    a3 =  np.array([eX[2],eY[2],eZ[2]]) 
    #print(a1,a2,a3)
    r1 =  np.vstack( [a1,a2] ) 
    r2 =  np.vstack( [r1,a3] )

    return r2


def norm(arr):
    div = (arr[0]**2+arr[1]**2+arr[2]**2)**(1/2)
    
    return [arr[0]/div,arr[1]/div,arr[2]/div]


def Rotation( theta,aix):
    R = np.ones([3,3])

    if aix == "x":
        R = np.array([[   1, 0,             0            ],
                        [ 0, np.cos(theta),-np.sin(theta)],
                        [ 0, np.sin(theta), np.cos(theta)]])



    if aix == "y":
        R = np.array([[   np.cos(theta), 0, np.sin(theta)],
                        [ 0,             1,            0],       
                        [-np.sin(theta), 0, np.cos(theta)]])
                        


    if aix == "z":
        R = np.array([[  np.cos(theta),-np.sin(theta),0],
                        [np.sin(theta), np.cos(theta),0],
                        [0,             0,            1]])

    return R


def Move( arr, distance,aix):

    if aix == "x":
        return arr[0]+distance




    if aix == "y":
        return arr[1]+distance

                        


    if aix == "z":
        return arr[2]+distance






s_3 = (3**(1/2))
eX = np.array([   1/2,      s_3/2,   0  ])
eY = np.array([   -s_3/2,   1/2,     0  ])
eZ = np.array([   0,        0,       1  ])

eX = norm(eX)
eY = norm(eY)
eZ = norm(eZ)

s =  np.array([  (1/4) -s_3/4 ,  (1/4) +s_3/4  ,0])

print("---------------------")
print(M(eX,eY,eZ))
print("---------------------")

e = M(eX,eY,eZ).T.dot(s)
print( e )
print("---------------------")




def creat_points ():
    points_absolute = []
    aixs_array_list = []#np.array([[1,0,0],[0,1,0],[0,0,1]])
    aixs_point_list = []

    random.seed(0)
    for i in range(12):
    
        oa = np.array([random.randint(1,10),random.randint(1,10),random.randint(1,10)])
        points_absolute.append(oa)
    

        aix = random.choice(["x","y","z"])
        theta = random.random()*3.1
        M = Rotation(theta,aix)
        aixX = np.array([1,0,0]).dot(M)
        aixY = np.array([0,1,0]).dot(M)
        aixZ = np.array([0,0,1]).dot(M)

        aix = random.choice(["x","y","z"])
        theta = random.random()*3.1
        M = Rotation(theta,aix)
        aixX = np.array(aixX).dot(M)
        aixY = np.array(aixY).dot(M)
        aixZ = np.array(aixZ).dot(M)

        aix = random.choice(["x","y","z"])
        theta = random.random()*3.1
        M = Rotation(theta,aix)
        aixX = np.array(aixX).dot(M)
        aixY = np.array(aixY).dot(M)
        aixZ = np.array(aixZ).dot(M)
        
        aixs_array_list.append(np.array([list(aixX),
                                     list(aixY),
                                     list(aixZ)]))


        ox = [oa,oa+aixX]
        oy = [oa,oa+aixY]
        oz = [oa,oa+aixZ]


        aixs_point_list .append( [ox,oy,oz] )
    return  aixs_point_list
    #aixs_info.append([ox,oy,oz])
aixs_point_list =  creat_points ()
#print(len(aixs_point_list))





















import matplotlib.pyplot as plt
#import numpy as np

# Fixing random state for reproducibility

def plot_point(aixs_point_list):


    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    n = 100

    # For each set of style and range settings, plot n random points in the box
    # defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
    for c,(ox, oy, oz) in enumerate(aixs_point_list):
        m = random.choice([".","o","^"])

        oo,oa = ox
        oo,ob = oy
        oo,oc = oz


        xs = [oo[0],oa[0],ob[0],oc[0]]
        ys = [oo[1],oa[1],ob[1],oc[1]]
        zs = [oo[2],oa[2],ob[2],oc[2]]
        #print("--",xs,ys,zs)
        ax.scatter(xs, ys, zs, marker=m)

        xs = [oo[0],oa[0],oo[0],ob[0],oo[0],oc[0]]
        ys = [oo[1],oa[1],oo[1],ob[1],oo[1],oc[1]]
        zs = [oo[2],oa[2],oo[2],ob[2],oo[2],oc[2]]



        ax.plot(xs, ys, zs)

        label = str(c)
        zdir = None
        #print(oo[0],oo[1],oo[2])

        ax.text(oo[0],oo[1],oo[2], label, zdir)



    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    plt.show()


plot_point(aixs_point_list)


import math

def tran_saixs_point_list(aixs_point_list):


    aixs_point_list_new = [] 

    for i in aixs_point_list:
        axis = []
        for o,axi in i:
            print(o,axi ,end = "")
            m = Rotation( math.pi/2,"z")
            o = o.dot(m)
            axi = axi.dot(m)
            axis.append([o,axi])
        aixs_point_list_new.append(axis)
        print("---------------")
    return aixs_point_list_new


aixs_point_list_new = tran_saixs_point_list(aixs_point_list)

plot_point(aixs_point_list_new)


def relatively_aixs_point(aix,eX,eY,eZ):
    eX = norm (eX)
    eY = norm (eY)
    eZ = norm (eZ)

    
    return M(eX,eY,eZ).T.dot(aix)

def F(aixs_point_list):
    base = aixs_point_list[0]

    
            
    aixs_point_list_new = []
    eO = base[0][0]
    eX,eY,eZ =base[0][1]-eO, base[1][1]-eO, base[2][1]-eO
    for  count,i in enumerate( aixs_point_list[1:]):
        axis = []
        for o,axi in i:

            o_rela = relatively_aixs_point(o-eO,eX,eY,eZ)
            axi_rela = relatively_aixs_point(axi-eO,eX,eY,eZ)
            axis.append([o_rela,axi_rela]) 

        aixs_point_list_new.append(axis)
        

        
    return aixs_point_list_new 









a = F(aixs_point_list)
print(len(a))
for i in a:
    print("-",i)

print("#######")

b = F(aixs_point_list_new)
for i in b:
    print("-",i)
print(len(b))




import copy
def get_result(aixs_point_list):
    aixs_point_list_new = copy.deepcopy(aixs_point_list)

    aixs_point_list_result = []
    num  =len(aixs_point_list_new)
    for i in range(num):
        
    
        aixs_point_list_result.append(aixs_point_list_new[0])
    

        aixs_point_list_new = F(aixs_point_list_new)

        print(i,len(aixs_point_list_new))

    return aixs_point_list_result

print("~~~~~~~~~~~~~~~~~~~~~")






a = get_result(aixs_point_list)
for i in a:
    print("-",i)

print("#######")

b = get_result(aixs_point_list_new)
for i in b:
    print("-",i)


input("----------------")



























def relatively_saixs_point_list(aixs_point_list):


    aixs_point_list_new = [] 

    for count,i in enumerate( aixs_point_list):
        axis = []
        
        if count==0:
            
            eO,eX,eY,eZ = [0,0,0],[1,0,0],[0,1,0],[0,0,1]
            for o,axi in i:

                
                
                
                o_rela = relatively_aixs_point(o-eO,eX,eY,eZ)
                
                axi_rela = relatively_aixs_point(axi-eO,eX,eY,eZ)
                #print("1",axi_rela)

                #axi_rela = norm(axi_rela)

                #print("2",axi_rela)
                #input("------")
                

               
                #|----|axi = axi+o-np.array([0,0,0])
                #|    |print(o_rela)
                #|    |print(axi_rela)
                #|    |o = o - np.array([0,0,0])
                #|    |o_rela,axi_rela
                #|    |o_rela,aci_rela
                #|    |o_rela,aci_rela
                #|    |o_rela,aci_rela
                #|----|o_rela,aci_rela

                axis.append([o_rela,axi_rela])
            aixs_point_list_new.append(axis)
            
        if count>0:
            last = aixs_point_list_new[count-1]
            

            eO,eX,eY,eZ =last[0][0], last[0][1]-last[0][0], last[1][1]-last[1][0], last[2][1]-last[2][0]
           
            #z,a,b,c = next[0][0],next[0][1],next[1][1],next[2][1]
            for o,axi in i:

                

                o_rela = relatively_aixs_point(o-eO,eX,eY,eZ)

                axi_rela = relatively_aixs_point(axi-eO,eX,eY,eZ)

                #print("1",axi_rela)

                #axi_rela = norm(axi_rela)

                #print("2",axi_rela)
                #input("------")                
                
                #axi = axi+o-np.array([0,0,0])
                #o = o - np.array([0,0,0])
                #print(o_rela)
                #print(axi_rela)
                
                axis.append([o_rela,axi_rela])

            aixs_point_list_new.append(axis)
        

        print("---------------")
    return aixs_point_list_new

aixs_point_list_new1 = relatively_saixs_point_list(aixs_point_list)
print()
aixs_point_list_new2 = relatively_saixs_point_list(aixs_point_list_new)

print("###############################################################")
#print(aixs_point_list_new1)
for i in aixs_point_list_new1:
    print("->",i)
print("-----")
#print(aixs_point_list_new2)
for i in aixs_point_list_new2:
    print("->",i)
