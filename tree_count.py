__author__ = 'BlackPanther'
import itertools
import copy
import math

filename = "test.txt"

#defining empty dictionary which will keep all consistent sub graphs sorted as per at which level they were created
levels_subgraphs = {}
tree_with_supernodes = {}

#defination of the graph class and properties modified as required for the algorithm
class Graph(object):
    def __init__(self):
        self.parent_child = {}
        self.child_parent = {}
        self.level_created = None
        self.depth_with_nodes = {}
        self.root = None
        self.depth = None

    def check_childs(self, node):
        self.node = node
        if self.node in self.child_parent.keys():
            return True
        else:
            return False

    def assign_level(self, n):
        self.level_created = n

    def assign_depth(self, n):
        self.depth = n

    def check_level(self):
        return self.level_created

class SuperNode():
    def __init__(self, data, parent = None):
        self.data = data
        self.parent = parent

#processing the input data
def Dataprocessing(filename):
    #DataProcessing

    main_graph = Graph()

    with open(filename) as f:
        for line in f:
            test = []
            test.append([n for n in line.strip().split(' ')])
            if test[0][0] == 'child':
                test.remove(['child','parent'])
            else:
                if test[0][0] not in main_graph.child_parent.keys():
                    main_graph.child_parent[test[0][0]] = [test[0][1]]
                else:
                    main_graph.child_parent[test[0][0]].append(test[0][1])

                if test[0][1] not in main_graph.parent_child:
                    main_graph.parent_child[test[0][1]] = [test[0][0]]
                else:
                    main_graph.parent_child[test[0][1]].append(test[0][0])

    #DecidingRoot
    temp_list = []
    for each in main_graph.parent_child.keys():
        if each not in main_graph.child_parent.keys():
            temp_list.append(each)
            main_graph.root = temp_list

    main_graph.depth_with_nodes[1] = main_graph.root

    i,j =2, 3
    #Getting Levels Dictionary for Level1
    for each in main_graph.depth_with_nodes[1]:
        for eachagain in main_graph.parent_child[each]:
            if 2 in main_graph.depth_with_nodes.keys():
                main_graph.depth_with_nodes[2].append(eachagain)
            else:
                main_graph.depth_with_nodes[2] = [eachagain]

    #Getting Levels Dictionary for all other levels
    while i != j:
        flag = False
        for each in main_graph.depth_with_nodes[i]:
            if each in main_graph.parent_child.keys():
                flag = True
                for eachagain in main_graph.parent_child[each]:
                    for temp in (main_graph.depth_with_nodes.keys()):
                        if eachagain in main_graph.depth_with_nodes[temp]:
                            main_graph.depth_with_nodes[temp].remove(eachagain)
                    if j in main_graph.depth_with_nodes.keys():
                        main_graph.depth_with_nodes[j].append(eachagain)
                    else:
                        main_graph.depth_with_nodes[j] = [eachagain]
        if flag:
            i += 1
            j += 1
        else:
            i += 1
    main_graph.level_created = 1
    main_graph.depth = len(main_graph.depth_with_nodes)
    return main_graph

# #method to generate all combinations
# def powerset(iterable):
#     s = list(iterable)
#     return list(itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(1, len(s)+1)))


#defining object for main graph
main_graph = Graph()

#generation of main graph with the data given
main_graph = Dataprocessing(filename)

#initialising the first graph
root_graph = Graph()
root_graph.child_parent[main_graph.root[0]] = None
root_graph.assign_level(1)

tree_update_with_super_node = {}

level = len(main_graph.depth_with_nodes)
#
def get_data_nonsupernode(NSlist):
    return int((math.pow(2, len(NSlist))-1))

def check_parent(parent, level):
    non_super_nodes = []
    children = copy.deepcopy(main_graph.parent_child[parent])
    for each in children:
        if not isinstance(each, SuperNode):
            non_super_nodes.append(each)
            main_graph.depth_with_nodes[level+1].remove(each)
            main_graph.parent_child[parent].remove(each)
    if len(non_super_nodes) > 0 :
        super_node_data = get_data_nonsupernode (non_super_nodes)
        new_super_node = SuperNode(super_node_data)
        new_super_node.parent = parent
        main_graph.depth_with_nodes[level+1].append(new_super_node)
        main_graph.parent_child[parent].append(new_super_node)

def resolve_small_tree(parent, level):
    summation = 0
    product = 1
    if len(main_graph.parent_child[parent]) == 1:
        for each in main_graph.parent_child[parent]:
            new_data = each.data + 1
    else:
        for each in main_graph.parent_child[parent]:
            product = product * (each.data + 1)
        new_data =  product
    new_super_node = SuperNode(new_data)
    #get Grandparent
    grandparent = main_graph.child_parent[parent]
    for each in grandparent:
        main_graph.parent_child[each].remove(parent)
        if each in main_graph.parent_child.keys():
            main_graph.parent_child[each].append(new_super_node)
        else:
            main_graph.parent_child[each] = [new_super_node]
    main_graph.depth_with_nodes[level].remove(parent)
    main_graph.depth_with_nodes[level].append(new_super_node)


def main():
    current_level = len(main_graph.depth_with_nodes.keys())-1

    while current_level != 1:
       nodes_at_current_level = copy.deepcopy(main_graph.depth_with_nodes[current_level])
       for each_parent in nodes_at_current_level :
           if each_parent in main_graph.parent_child.keys():
               check_parent(each_parent, current_level)
               resolve_small_tree(each_parent, current_level)
       current_level =current_level - 1

    if current_level == 1:
        for root in main_graph.depth_with_nodes[current_level]:
            check_parent(root, current_level)
            summation = 0
            product = 1
            if len(main_graph.parent_child[root]) == 1:
                for each in main_graph.parent_child[root]:
                    new_data = each.data + 1
                final_super_node = SuperNode(new_data)
            else:
                for each in main_graph.parent_child[root]:
                    product = product * (each.data + 1)
                new_data =  product
                final_super_node = SuperNode(new_data)

    print final_super_node.data

main()