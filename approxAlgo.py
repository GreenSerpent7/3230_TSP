import sys
from sys import maxsize
from itertools import permutations

V = 15  # represents the number of nodes in the graph


# below we are finding the smallest node (aka vertex) from a set of nodes not yet in our MST
def findSmallestKey(key, mstSet):
    min_value = sys.maxsize  # set min value to max system size
    min_index = -1  # set starting index to -1
    for v in range(V):  # 14 nodes that we search through
        if not mstSet[v] and key[
            v] < min_value:  # if key is not in MST and value is less than curr min value reassign curr min value to curr value
            min_value = key[v]
            min_index = v
    return min_index


# next step is to use one of the two MST methods (either Kruska's or Prim's); Here we are using Prim's below
def primMST(graph, parent):
    key = [sys.maxsize] * V  # we set the key equal to the max system size multiplied by the number of nodes (14)
    mstSet = [
                 False] * V  # we start by flagging the system as false for all 14 nodes to represent that no node has been visited yet
    key[0] = 0  # we set the key to 0 as a default state to indicate no key at this time has been set
    parent[0] = -1
    for _ in range(V - 1):
        u = findSmallestKey(key, mstSet)
        mstSet[u] = True
        for v in range(V):
            if graph[u][v] and not mstSet[v] and graph[u][v] < key[v]:
                parent[v] = u
                key[v] = graph[u][v]


# next step is step is to conduct the preorder traversal (depth first search) of our new MST
def printPreorderTraversal(parent):
    print("The preorder traversal of the tree is found to be - ", end="")
    for i in range(0, V):
        print(parent[i], " ->", end="")
    print()


# last step is to set up the main function for the traveling salesperson approximation algo
def tspApproximation(graph):
    parent = [0] * V
    root = 0

    primMST(graph, parent)

    printPreorderTraversal(parent)
#####################################################################################
    # I ADDED this portion below this point
    visited = [root]

    # recursive top down DFS preorder traversal of the MST based on the parentList
    # which adds nodes to visited in order of when they were visited. This results
    # in a Hamiltonian cycle (After you append the root back to it afterwards)
    # the function uses the mst Parent list, which is what Kevin's code prints as the preorder traversal
    def topDownDFStoHam(mstPList, root):
        # allows the function to access the outside list
        nonlocal visited
        # loops through each node
        for i in range(0, V):
            # if the node's parent is the root (or the node being checked in recursive calls)
            if mstPList[i] == root:
                # immediately append to visited for the Hamiltonian cycle
                visited.append(i)
                # recursively call the function to check if this node has any children
                topDownDFStoHam(mstPList, i)
        return visited

    ham = topDownDFStoHam(parent, root)
    # finish hamiltonian cycle by adding root to the end
    ham.append(root)
    hamDist = 0
    # calculate the distance of the hamiltonian cycle
    for i in range(0, V):
        hamDist += graph[ham[i]][ham[i + 1]]
    print("Cycle: " + str(ham))
    print("distance: " + str(hamDist))

#####################################################################


    print("Adding the root node at the end of the traced path ", end="")
    for i in range(V):
        print(parent[i], "->", end="")
    print(root, "-> ", parent[0])

    cost = 0
    for i in range(1, V):
        cost += graph[parent[i]][i]

    print("Sum of all the costs in the minimum spanning tree:", cost)


if __name__ == "__main__":
    graph = [[    0,    4019.6,   6887.93,  8784.12,  5801.44,  8904.1,  10375.26,  7318.19,
  11157.18,  4450.22,  9681.18,  9260.78,  4694.91,  3342.52,  9946.77],
 [ 4019.6,      0.,   10045.74, 11671.65,  5533.79,  5067.68,  6829.38,  6032.46,
  12216.12,  7474.61, 12627.51,  5279.94,  4023.18,  6549.02,  7733.09],
 [ 6887.93, 10045.74,     0.,   12085.5,  12533.08, 15086.6,  16860.91, 14172.67,
   6997.7,   2573.89,  2821.72, 15118.2,  11563.82,  8269.42, 16833.53],
 [ 8784.12, 11671.65, 12085.5,      0.,    7907.21, 14873.28, 15241.51,  9529.55,
  18579.33, 11050.86, 14463.69, 15739.57,  8673.05,  5445.,   12217.48],
 [ 5801.44,  5533.79, 12533.08,  7907.21,     0.,    7098.97,  7336.07,  1908.64,
  16753.75, 10216.96, 15354.09,  8075.25,  1515.09,  5025.13,  4875.5 ],
 [ 8904.1,   5067.68, 15086.6,  14873.28,  7098.97,     0.,    2149.88,  6067.83,
  16329.98, 12523.19, 17601.87,  1158.46,  6210.79, 10637.82,  5491.71],
 [10375.26,  6829.38, 16860.91, 15241.51,  7336.07,  2149.88,     0.,    5840.73,
  18443.13, 14287.08, 19456.21,  2996.59,  6861.2,  11597.58,  4235.07],
 [ 7318.19,  6032.46, 14172.67,  9529.55,  1908.64,  6067.83,  5840.73,     0.,
  17912.64, 11768.21, 16983.1,   7161.71,  2626.05,  6921.19,  2966.86],
 [11157.18, 12216.12,  6997.7,  18579.33, 16753.75, 16329.98, 18443.13, 17912.64,
      0.,    7540.79,  6264.91, 15856.76, 15397.64, 13858.07, 19943.05],
 [ 4450.22,  7474.61,  2573.89, 11050.86, 10216.96, 12523.19, 14287.08, 11768.21,
   7540.79,     0.,    5272.26, 12583.34,  9143.92,  6445.39, 14350.79],
 [ 9681.18, 12627.51,  2821.72, 14463.69, 15354.09, 17601.87, 19456.21, 16983.1,
   6264.91,  5272.26,     0.,   17536.23, 14368.82, 11032.,   19614.86],
 [ 9260.78,  5279.94, 15118.2,  15739.57,  8075.25,  1158.46,  2996.59,  7161.71,
  15856.76, 12583.34, 17536.23,     0.,    7069.78, 11283.23,  6640.25],
 [ 4694.91,  4023.18, 11563.82,  8673.05,  1515.09,  6210.79,  6861.2,   2626.05,
  15397.64,  9143.92, 14368.82,  7069.78,     0.,    4798.88,  5339.19],
 [ 3342.52,  6549.02,  8269.42,  5445.,    5025.13, 10637.82, 11597.58,  6921.19,
  13858.07,  6445.39, 11032.,   11283.23,  4798.88,     0.,    9878.  ],
 [ 9946.77,  7733.09, 16833.53, 12217.48,  4875.5,   5491.71,  4235.07,  2966.86,
  19943.05, 14350.79, 19614.86,  6640.25,  5339.19,  9878.,       0.  ]]
    tspApproximation(graph)