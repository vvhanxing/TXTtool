import sys
import numpy as np
#input(sys.version)
#import commands #python2
import subprocess as commands #python3

cmd = "pip2.7 list"
output = commands.getoutput(cmd)

paks = []
lines = output.split("\n")
mark = "----------"
pak_name_line_start = 0
for count, line in enumerate(lines):
    if mark in line:
        pak_name_line_start = count+1
    if count >= pak_name_line_start and "DEPRECATION:" not in line and "Package " not in line:
        pak_name = line.split()[0]
        version = line.split()[1]
        paks.append(pak_name)
        print (">", pak_name , version)



import networkx as nx
import matplotlib.pyplot as plt

G=nx.DiGraph()

#item = [1,2]
#G.add_edge(*item) #color = item[-1], weight = 2)

#item = [3,1]
#G.add_edge(*item)





for pak_name in paks[:10]:
    Requires = []
    Required_by = []
    output = commands.getoutput(cmd)
    cmd = "pip2.7 show "+pak_name
    print("-----")
    print(cmd)
    print("-----")
    #print(output)
    lines = output.split("\n")
    for line in lines:
      if "Requires:" in line:
        print(">",line)
        require_paks = line.split()[1:]
        if len(require_paks)>0:
            for require_pak in require_paks:
                item = [require_pak,pak_name]
                G.add_edge(*item) #color = item[-1], weight = 2)
      if "Required-by:" in line:
        print(">",line)
        require_by_paks = line.split()[1:]
        if len(require_by_paks)>0:
            for require_by_pak in require_by_paks:
                item = [require_by_pak,pak_name]
                G.add_edge(*item) #color = item[-1], weight = 2)


#nx.write_dot(G,'test.dot')
print(G)


print("in_degree")
nodes_in_degree = G.in_degree()
print(nodes_in_degree)

print("out_degree")
nodes_out_degree = G.out_degree()
print(nodes_out_degree)

print()



plt.title('python pkg net')
#nodes_pos = nx.spring_layout(G)
nodes_pos = {}

print("------------")
paths = nx.all_simple_paths(G, source="ipython", target="bzr")
for path in list(paths ):
    print(path)
    #input("---")

print(list(paths))
#input()
print("------------")

nodes_in_degree_0    = list(filter(lambda x :x[1]==0 ,nodes_in_degree))
nodes_in_degree_not0 = list(filter(lambda x :x[1]!=0 ,nodes_in_degree))

for count, node_in_degree in enumerate(nodes_in_degree):
    node_name = node_in_degree[0]
    in_degree = node_in_degree[1]
    nodes_pos[node_name] = np.array([count,in_degree])


    print("---------------->",len(nodes_in_degree),len(nodes_in_degree_not0),len(nodes_in_degree_0))
    #input()
    if (node_name,0) in  nodes_in_degree_0:#初始顶点
        nodes_pos[node_name] = np.array([count,in_degree])

    else: #不是初始顶点
        nodes_pos[node_name] = np.array([count,in_degree])
        # node_name #该顶点到初始顶点的路径长度
        # nodes_pos[node_name] = np.array([count,in_degree])
       
        paths_length = []
        for node_in_degree_0 in nodes_in_degree_0:

           
            print("node_in_degree_0,node_name ",node_in_degree_0,node_name)
            paths = list(nx.all_simple_paths(G, source=node_in_degree_0[0], target=node_name))
            print(">>",  paths )
            if paths!=[]:
                max_path_length = max( [len(path) for path in paths] )
                paths_length.append(max_path_length)
            else:
              paths_length.append(0)
               
       
        nodes_pos[node_name] = np.array([count,max(paths_length)])
        print("-")
   

# nodes_in_degree_not0 = list(filter(lambda x :x[1]!=0 ,nodes_in_degree))
# nodes_in_degree_0 = list(filter(lambda x :x[1]==0 ,nodes_in_degree))
# print("---------------->",len(nodes_in_degree),len(nodes_in_degree_not0),len(nodes_in_degree_0))

# for count , node_in_degree_not0 in enumerate(nodes_in_degree_not0):
#     nodes_pos[node_in_degree_not0] = np.array([0,count])
#     print("+",node_in_degree_not0,nodes_pos[node_in_degree_not0] )



# for count , node_in_degree_0 in enumerate(nodes_in_degree_0):
#     nodes_pos[node_in_degree_0] = np.array([5,count])
#     print("-",node_in_degree_0,nodes_pos[node_in_degree_0] )




nx.draw(G,nodes_pos,with_labels = True, edge_color = 'b')  
#print(nodes_pos)
plt.show()

