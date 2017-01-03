
adjLists_dict_tree = {}
adjLists_dict_tree_CP ={}

#to be edited to where you keep the input file
filepath = "E:/IU/ADA/Mini Project/trees/tree_100.txt"

f = open(filepath, 'r+')

def generate_tree():
    k=1 #optimized increment, keeps track of column number
    j=0 #track row number
    for line in f:
        cells = line.split()
        adjLists_dict_tree[j] = []
        for field in range(k,len(cells)):
            if cells[field] == "1":
                adjLists_dict_tree[j].append(k)
                if k in adjLists_dict_tree_CP.keys():
                    adjLists_dict_tree_CP[k].append(j)
                else:
                    adjLists_dict_tree_CP[k] = j
                k = k + 1
        j = j + 1


def print_tree():
    n = len(adjLists_dict_tree)
    for key in adjLists_dict_tree:
        print(key, ":", adjLists_dict_tree[key])


def print_tree_CP():
    print("--------------------------------------")
    n = len(adjLists_dict_tree_CP)
    for key in adjLists_dict_tree_CP:
        print(key, adjLists_dict_tree_CP[key])

#generated output can be used as input. 

generate_tree()
print_tree()
print_tree_CP()
f.close()
