__author__ = 'BlackPanther'
import itertools
import copy

filename = "test.txt"

#defining empty dictionary which will keep all consistent sub graphs sorted as per at which level they were created
levels_subgraphs = {}

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

#method to generate all combinations
def powerset(iterable):
    s = list(iterable)
    return list(itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(1, len(s)+1)))


#defining object for main graph
main_graph = Graph()

#generation of main graph with the data given
main_graph = Dataprocessing(filename)

#initialising the first graph
root_graph = Graph()
root_graph.child_parent[main_graph.root[0]] = None
root_graph.assign_level(1)

levels_subgraphs[1] = [root_graph]

for level in range(2, main_graph.depth+1):
    #previous level
    previous_level = level - 1
    print level
    #getting all nodes present at current level
    nodes_at_current_level = main_graph.depth_with_nodes[level]

    #generating combinations of each node at current level
    # all_possible_combinations= [list(i) for i in powerset(nodes_at_current_level)]

    for each_list in [list(i) for i in powerset(nodes_at_current_level)]:

        new_sub_graphs = copy.deepcopy(levels_subgraphs[previous_level])
        print "Deep copy done"
        print len(new_sub_graphs)

        #getting the consistent graphs for each combinations to append
        for each_element in each_list:
            parent_of_current_element = main_graph.child_parent[each_element]
            for each_parent in parent_of_current_element:
                temp = []
                for each_subgraph_at_previous_level in new_sub_graphs:
                    if each_parent not in each_subgraph_at_previous_level.child_parent.keys():
                        temp.append(each_subgraph_at_previous_level)
                if len(temp) > 0:
                    for k in temp:
                        new_sub_graphs.remove(k)

        #now appending all edges with all parents to resulting graphs and appending to original subgraph list with level update
        if not new_sub_graphs:
            continue
        else:
            for each_element in each_list:
                parent_of_current_element = main_graph.child_parent[each_element]
                for each_parent in parent_of_current_element:
                    for each_consitent_subgraph_at_previous_level in new_sub_graphs:
                        if each_element not in each_consitent_subgraph_at_previous_level.child_parent.keys():
                            each_consitent_subgraph_at_previous_level.child_parent[each_element] = [each_parent]
                        else:
                            each_consitent_subgraph_at_previous_level.child_parent[each_element].append(each_parent)

        for each_new_graph in new_sub_graphs:
            if level in levels_subgraphs.keys():
                levels_subgraphs[level].append(each_new_graph)
            else:
                levels_subgraphs[level] = [each_new_graph]

count = 0

for each in levels_subgraphs.keys():
    count += len(levels_subgraphs[each])

print count
