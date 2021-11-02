import pandas as pd
import psycopg2
from psycopg2 import Error
import anytree
from anytree import NodeMixin, RenderTree
import re
from psycopg2 import Error






class QepNode(NodeMixin): # Add node feature
    def __init__(self, list_of_tuple, parent=None, children=None):
        self.list_tup = list_of_tuple
        self.explanation = self.get_info()
        self.name = self.get_node_type()
        self.parent = parent

        if children:
            self.children = children

    def get_node_type(self):
        # r1 = re.compile("(.*?)\s*\(")  # get text before paranthesis
        # m1 = r1.match(self.list_tup[0][0])
        # return m1
        text = self.list_tup[0][0].split('(')[0]
        if '->  ' in text:
            text = text.split('->  ')[1]
        return text

    def get_info(self):
        _text = ""
        for i in self.list_tup[1:]:
            print(i)
            _text += i[0].lstrip()
        print(f"{_text} - final string")
        return _text

# get index of first '->'
def get_index_first_arrow(qep):
    for idx, value in enumerate(qep, start=0):
        if '->' in value[0]:
            return idx


def group_nodes_to_list(qep):
    # takes in qep output from cursor.fetchall()
    # return a list of tuple
    lst = []
    if get_index_first_arrow(qep) == 1:
        lst.append([qep[0]])
    else:
        lst.append(qep[:get_index_first_arrow(qep) - 1])

    qep = qep[get_index_first_arrow(qep):]

    # get index of tuple with '->'
    idx_arrow = []
    for idx, value in enumerate(qep, start=0):
        if '->' in value[0]:
            idx_arrow.append(idx)

    for idx, value in enumerate(idx_arrow[:], start=0):
        if idx == len(idx_arrow) - 1:
            lst.append(qep[value:])
        else:
            lst.append(qep[value:idx_arrow[idx+1]])

    # for i in lst:
    #     print(i)

    return lst



def store_qep_in_tree(qep):
    # return list of objects of qep
    lst_obj = []
    lst = group_nodes_to_list(qep)

    for idx, value in enumerate(lst, start=0):

        # check indent of node
        node = value[0]
        indent = re.search('\S', node[0]).start()

        # for root node
        if indent == 0:
            obj = QepNode(value)
            lst_obj.append(obj)
            continue

        # if indent of current node larger than previous node, set previous node as parent
        if indent > (re.search('\S', lst[idx-1][0][0]).start()):
            obj = QepNode(value, parent=lst_obj[idx-1])
            lst_obj.append(obj)

        # else look for parent
        else:
            for j, k in enumerate(reversed(lst[:idx]), start=1):
                prev_indent = re.search('\S', k[0][0]).start()
                if prev_indent < indent:
                    obj = QepNode(value, parent=lst_obj[len(lst[:idx])-j])
                    lst_obj.append(obj)

    return lst_obj


def print_steps(lst_obj):
    # Take the list of objects as parameter and print out the steps for execution from bottom up
    root = lst_obj[0]
    query_string = ""

    # check out PostOrderIter anytree for traversal
    x = [node for node in anytree.PostOrderIter(root)]
    for idx, val in enumerate(x, start=1):
        print(f'Step {idx}: Perform {val.name}')
        query_string += f'Step {idx}: Perform {val.name}'

        if val.explanation != "":
            print(f'{val.explanation}')
            query_string += f'{val.explanation}'
        query_string += '\n'

    for pre, _, node in RenderTree(lst_obj[0]):
        print("%s%s" % (pre, node.name))

    return query_string

def get_tree(lst_obj):

    for pre, _, node in RenderTree(lst_obj[0]):
        print("%s%s" % (pre, node.name))


