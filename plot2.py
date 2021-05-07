import numpy as np

import random

import copy

def M(eX,eY,eZ):
    a1 =  np.array([eX[0],eY[0],eZ[0]])
    a2 =  np.array([eX[1],eY[1],eZ[1]])
    a3 =  np.array([eX[2],eY[2],eZ[2]]) 
    r1 =  np.vstack( [a1,a2] ) 
    r2 =  np.vstack( [r1,a3] )
    return r2


def norm(arr):
    div = (arr[0]**2+arr[1]**2+arr[2]**2)**(1/2)
    return [arr[0]/div,arr[1]/div,arr[2]/div]


def Rotation( theta,aix):
    R = np.ones([3,3])

    if aix == "x":
        R = np.array([  [ 1, 0,             0            ],
                        [ 0, np.cos(theta),-np.sin(theta)],
                        [ 0, np.sin(theta), np.cos(theta)]])



    if aix == "y":
        R = np.array([  [ np.cos(theta), 0, np.sin(theta)],
                        [ 0,             1,            0 ],       
                        [-np.sin(theta), 0, np.cos(theta)]])
                        


    if aix == "z":
        R = np.array([  [np.cos(theta),-np.sin(theta),0],
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



#------------------------------------


# s_3 = (3**(1/2))
# eX = np.array([   1/2,      s_3/2,   0  ])
# eY = np.array([   -s_3/2,   1/2,     0  ])
# eZ = np.array([   0,        0,       1  ])

# eX = norm(eX)
# eY = norm(eY)
# eZ = norm(eZ)

# s =  np.array([  (1/4) -s_3/4 ,  (1/4) +s_3/4  ,0])

# print("---------------------")
# print(M(eX,eY,eZ))
# print("---------------------")

# e = M(eX,eY,eZ).T.dot(s)
# print( e )
# print("---------------------")

#------------------------------------


def creat_random_points():
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
        M = Rotation(theta,aix).dot(M)
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


aixs_point_list =  creat_random_points ()




aixs_point_list = [
    #  oo      ox          oo      oy          oo      oz
    [[[0,0,0],[1,0,0]],  [[0,0,0],[0,1,0]],  [[0,0,0],[0,0,1]]],
    [[[0,0,1],[1,0,1]],  [[0,0,1],[0,1,1]],  [[0,0,1],[0,0,2]]],

    [[[0,0,2+1],[1,0,2+1]],  [[0,0,2+1],[0,1,2+1]],  [[0,0,2+1],[0,0,3+1]]],
    [[[0,0,3+1],[1,0,3+1]],  [[0,0,3+1],[0,1,3+1]],  [[0,0,3+1],[0,0,4+1]]],

    [[[0,0,4+2],[1,0,4+2]],  [[0,0,4+2],[0,1,4+2]],  [[0,0,4+2],[0,0,5+2]]],
    [[[0,0,5+2],[1,0,5+2]],  [[0,0,5+2],[0,1,5+2]],  [[0,0,5+2],[0,0,6+2]]]

]


#print(aixs_point_list.shape)


#aixs_point_list = list(map(norm,list(aixs_point_list)))
#input(aixs_point_list)






def transform_aixs_point(aixs_point_list,aix,theta):
    aixs_point_list = np.array(aixs_point_list)
    shape = aixs_point_list.shape
    #print(shape)
    aixs_point_list = aixs_point_list.reshape([shape[0]*shape[1]*shape[2],3])

    M = Rotation(theta,aix)  
    #aixs_point_list_t=aixs_point_list.dot(M)
    aixs_point_list_t = M.dot(aixs_point_list.T)
    aixs_point_list_t = aixs_point_list_t.T
    #print(aixs_point_list.shape,M.shape)
    #print(aixs_point_list.T.shape)
    aixs_point_list_t = np.array(aixs_point_list_t).reshape([shape[0],shape[1],shape[2],3])
    return aixs_point_list_t


#aix,theta = "z",0.5
#aixs_point_list = transform_aixs_point(aixs_point_list,aix,theta)











import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as p3


# # Fixing random state for reproducibility

# def plot_point(aixs_point_list):


#     #fig = plt.figure()
#     #ax = fig.add_subplot(111, projection='3d')
#     fig = plt.figure()
#     ax = p3.Axes3D(fig)

#     n = 100

#     # For each set of style and range settings, plot n random points in the box
#     # defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
#     for c,(ox, oy, oz) in enumerate(aixs_point_list):
#         m = random.choice([".","o","^"])

#         oo,oa = ox
#         oo,ob = oy
#         oo,oc = oz





#         xs = [oo[0],oa[0],ob[0],oc[0]]
#         ys = [oo[1],oa[1],ob[1],oc[1]]
#         zs = [oo[2],oa[2],ob[2],oc[2]]
#         #print("--",xs,ys,zs)
#         ax.scatter(xs, ys, zs, marker=m)

#         xs = [oo[0],oa[0],oo[0],ob[0],oo[0],oc[0]]
#         ys = [oo[1],oa[1],oo[1],ob[1],oo[1],oc[1]]
#         zs = [oo[2],oa[2],oo[2],ob[2],oo[2],oc[2]]



def plot_point(aixs_point_list):


    #fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    fig = plt.figure()
    ax = p3.Axes3D(fig)

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


#plot_point(aixs_point_list)

#         ax.plot(xs, ys, zs)

#         label = str(c)
#         zdir = None
#         #print(oo[0],oo[1],oo[2])

#         ax.text(oo[0],oo[1],oo[2], label, zdir)



#     ax.set_xlabel('X Label')
#     ax.set_ylabel('Y Label')
#     ax.set_zlabel('Z Label')

#     plt.show()


# plot_point(aixs_point_list)












def simulation(aixs_point_list,aix):

    #fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    fig = plt.figure()
    ax = p3.Axes3D(fig)
    m = random.choice([".","o","^"])


    def draw_circle(pos,aix,div,r):
        
        dx,dy,dz = pos

        an = np.linspace(0, 2 * np.pi, div)
        if aix=="x":
            ax.plot(r*np.zeros([div])+dx, r* np.cos(an)+dy,      r* np.sin(an)+dz )    
        if aix=="y":
            ax.plot( r* np.cos(an)+dx, r*np.zeros([div])+dy,     r* np.sin(an)+dz )  
        if aix=="z":
            ax.plot(r* np.cos(an)+dx,      r* np.sin(an)+dy ,r*np.zeros([div])+dy) 

    def draw_box(pos,s):
        
        dx,dy,dz = pos

        #an = np.linspace(0, 2 * np.pi, div)
        x = np.array([0,1,1,0])
        y = np.array([0,0,0,0])
        z = np.array([0,0,1,1])
        ax.plot( s*x+dx, s*y+dy, s*z+dz )    
        x = np.array([0,0,0,0])
        y = np.array([0,1,1,0])
        z = np.array([0,0,1,1])
        ax.plot( s*x+dx, s*y+dy, s*z+dz ) 

        x = np.array([0,1,1,0])
        y = np.array([0,0,1,1])
        z = np.array([0,0,0,0])
        ax.plot( s*x+dx, s*y+dy, s*z+dz )    
        x = np.array([0,1,1,0])
        y = np.array([0,0,1,1])
        z = np.array([1,1,1,1])
        ax.plot( s*x+dx, s*y+dy, s*z+dz )    

        x = np.array([0,0])
        y = np.array([0,0])
        z = np.array([0,1])
        ax.plot( s*x+dx, s*y+dy, s*z+dz ) 

        x = np.array([1,1])
        y = np.array([1,1])
        z = np.array([1,0])
        ax.plot( s*x+dx, s*y+dy, s*z+dz ) 


    p = np.linspace(0, 2*np.pi, 128)
    for theta in p:
        
        oos = []  #坐标原点连线
        
        plt.cla()
        

        for index,(ox, oy, oz) in enumerate(transform_aixs_point(aixs_point_list,aix,theta)):
            
            oo,oa = ox
            oo,ob = oy
            oo,oc = oz


            if index == 0:
                draw_circle(oo,"z",50,1)
            if index == 2:
                draw_circle(oo,"x",50,0.4)     

            if index == 4:
                draw_circle(oo,"x",50,0.4)                 

            if index == 5:
                draw_circle(oo,"x",50,0.4)
            draw_box([0,4,0],1)


            xs = [oo[0],oa[0],ob[0],oc[0]]
            ys = [oo[1],oa[1],ob[1],oc[1]]
            zs = [oo[2],oa[2],ob[2],oc[2]]
            ax.scatter(xs, ys, zs, marker=m)

            xs = [oo[0],oa[0],oo[0],ob[0],oo[0],oc[0]]
            ys = [oo[1],oa[1],oo[1],ob[1],oo[1],oc[1]]
            zs = [oo[2],oa[2],oo[2],ob[2],oo[2],oc[2]]
            ax.plot(xs, ys, zs)


            oos.append(oo)
            if index>0:
                xs = [oos[index-1][0],oos[index][0]]
                ys = [oos[index-1][1],oos[index][1]]
                zs = [oos[index-1][2],oos[index][2]]  
            ax.plot(xs, ys, zs)              


            label = str(index)
            zdir = None
            
            
            ax.text(oo[0],oo[1],oo[2], label, zdir)

            ax.text(oa[0],oa[1],oa[2], "x", zdir)
            ax.text(ob[0],ob[1],ob[2], "y", zdir)
            ax.text(oc[0],oc[1],oc[2], "z", zdir)


            ax.set_xlim3d([-6.0, 6.0])
            ax.set_ylim3d([-6.0, 6.0])
            ax.set_zlim3d([  .0,12.0])
            ax.set_xlabel('X Label')
            ax.set_ylabel('Y Label')
            ax.set_zlabel('Z Label')
        plt.pause(0.01)
    plt.show()





#import threading


#simulation(aixs_point_list,"z")

# t = threading.Thread(target=simulation,args=(aixs_point_list,"z"))
# t.start()











#------------------------------------------------

import math

def tran_saixs_point_list(aixs_point_list,index,aix,theta): #math.pi/2


    aixs_point_list_new = [] 

    for c, i in enumerate(aixs_point_list):
        axis = []
        for o,axi in i:
            #print(o,axi ,end = "")
            if c == index:
                m = Rotation( theta,aix)
                o = o.dot(m)
                axi = axi.dot(m)
            axis.append([o,axi])
        aixs_point_list_new.append(axis)
        #print("---------------")
    return aixs_point_list_new




def relatively_aixs_point(aix,eX,eY,eZ):
    #eX = norm (eX)
    #eY = norm (eY)
    #eZ = norm (eZ)

    
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



def get_relative_coordinate(aixs_point_list):
    aixs_point_list_new = copy.deepcopy(aixs_point_list)
    aixs_point_list_result = []
    num  =len(aixs_point_list_new)
    for i in range(num):
        aixs_point_list_result.append(aixs_point_list_new[0])
        aixs_point_list_new = F(aixs_point_list_new)
    return aixs_point_list_result


#-------------------------------------



def absolute_aixs_point(aix,eX,eY,eZ):
    M_r = np.linalg.inv(M(eX,eY,eZ))
    return M_r.T.dot(aix)



def inverse_F(aixs_point_list):
    base = aixs_point_list[0]
    aixs_point_list_new = [base]
    eO = base[0][0]
    eX,eY,eZ =base[0][1]-eO, base[1][1]-eO, base[2][1]-eO
    for count,i in enumerate(aixs_point_list[1:]):
        aixs = []
        for o,axi in i :
            o_rela = absolute_aixs_point(o,eX,eY,eZ)+eO
            axi_rela = absolute_aixs_point(axi,eX,eY,eZ)+eO
            aixs.append([o_rela,axi_rela]) 
        aixs_point_list_new.append(aixs)
    return aixs_point_list_new 



def get_absolute_coordinate(aixs_point_list):

    aixs_point_list_new = copy.deepcopy(aixs_point_list)
    aixs_point_list_result = []
    num  =len(aixs_point_list_new)
    aixs_point_list_temp = []
    for count,i in enumerate(aixs_point_list_new):
        if num-count-2 >= 0:
            aixs_point_list_temp = copy.deepcopy(aixs_point_list_new[num-count-2:])
            aixs_point_list_temp = inverse_F(aixs_point_list_temp)
            aixs_point_list_new[num-count-2:] = aixs_point_list_temp
            aixs_point_list_result = aixs_point_list_temp
    return aixs_point_list_result

#------------------------------------------------



aixs_point_list = get_relative_coordinate(np.array(aixs_point_list))

print(np.array(aixs_point_list).shape)
print(np.array(aixs_point_list).reshape([-1,3]))

index,aix,theta = 3 ,"x",math.pi/2
aixs_point_list = tran_saixs_point_list(aixs_point_list,index,aix,theta)


aixs_point_list = get_absolute_coordinate(np.array(aixs_point_list))



simulation(aixs_point_list,"z")




input("finish")
















# for i in aixs_point_list:
#     print("-",[list([list([k.round(3) for k in j]) for j in  x]) for x in i])

import math

def tran_saixs_point_list(aixs_point_list):


    aixs_point_list_new = [] 

    for i in aixs_point_list:
        axis = []
        for o,axi in i:
            #print(o,axi ,end = "")
            m = Rotation( math.pi/2,"z")
            o = o.dot(m)
            axi = axi.dot(m)
            axis.append([o,axi])
        aixs_point_list_new.append(axis)
        #print("---------------")
    return aixs_point_list_new


aixs_point_list_new = tran_saixs_point_list(aixs_point_list)

plot_point(aixs_point_list_new)
print("--------------------------")
for i in aixs_point_list_new:
    print("-",[list([list([k.round(3) for k in j]) for j in  x]) for x in i])


print("--------------------------")




def relatively_aixs_point(aix,eX,eY,eZ):
    #eX = norm (eX)
    #eY = norm (eY)
    #eZ = norm (eZ)

    
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



def get_relative_coordinate(aixs_point_list):
    aixs_point_list_new = copy.deepcopy(aixs_point_list)
    aixs_point_list_result = []
    num  =len(aixs_point_list_new)
    for i in range(num):
        aixs_point_list_result.append(aixs_point_list_new[0])
        aixs_point_list_new = F(aixs_point_list_new)
    return aixs_point_list_result



print("------------------------------------------------------111")



a = get_relative_coordinate(aixs_point_list)
for i in a:
    print("-",[list([list([k.round(3) for k in j]) for j in  x]) for x in i])

print("#######")

b = get_relative_coordinate(aixs_point_list_new)
for i in b:
    print("-",[list([list([k.round(3) for k in j]) for j in  x]) for x in i])


print("-----------------------------------------------------111")




def absolute_aixs_point(aix,eX,eY,eZ):
    M_r = np.linalg.inv(M(eX,eY,eZ))
    return M_r.T.dot(aix)



def inverse_F(aixs_point_list):
    base = aixs_point_list[0]
    aixs_point_list_new = [base]
    eO = base[0][0]
    eX,eY,eZ =base[0][1]-eO, base[1][1]-eO, base[2][1]-eO
    for count,i in enumerate(aixs_point_list[1:]):
        aixs = []
        for o,axi in i :
            o_rela = absolute_aixs_point(o,eX,eY,eZ)+eO
            axi_rela = absolute_aixs_point(axi,eX,eY,eZ)+eO
            aixs.append([o_rela,axi_rela]) 
        aixs_point_list_new.append(aixs)
    return aixs_point_list_new 



def get_absolute_coordinate(aixs_point_list):

    aixs_point_list_new = copy.deepcopy(aixs_point_list)
    aixs_point_list_result = []
    num  =len(aixs_point_list_new)
    aixs_point_list_temp = []
    for count,i in enumerate(aixs_point_list_new):
        if num-count-2 >= 0:
            aixs_point_list_temp = copy.deepcopy(aixs_point_list_new[num-count-2:])
            aixs_point_list_temp = inverse_F(aixs_point_list_temp)
            aixs_point_list_new[num-count-2:] = aixs_point_list_temp
            aixs_point_list_result = aixs_point_list_temp
    return aixs_point_list_result





print("------------------------------------------------------222")



aixs_point_list = get_absolute_coordinate(a)
for i in aixs_point_list:
    print("-",[list([list([k.round(3) for k in j]) for j in  x]) for x in i])

print("#######")

aixs_point_list_new = get_absolute_coordinate(b)
for i in aixs_point_list_new:
    print("-",[list([list([k.round(3) for k in j]) for j in  x]) for x in i])


print("-----------------------------------------------------222")








