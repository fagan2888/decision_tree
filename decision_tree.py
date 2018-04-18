import math


attributes_value = {}
attributes = []
examples = []
decision_values = []
f = open('examples.txt', 'r')
c = 0
for line in f:
    if line.split(' ')[0] == '%':
        c = c + 1
        continue
    if c == 1:
        atr, vals = line.replace('\n', '').split(': ')
        values = vals.split(', ')
        attributes.append(atr)
        attributes_value[atr] = values
    if c == 2:
        decision_values = line.replace('\n', '').split(', ')
    if c == 4:
        examples.append(line.replace('\n', '').split(', '))


ind_exm_deci = len(attributes)


class tree:
    def __init__(self, name):
        self.name = name
        self.value = []
        self.children = []

    def add_value(self, value):
        self.value.append(value)

    def add_children(self, node):
        self.children.append(node)


def Decision_Tree_Learning(examples, attributes, parent):
    if examples == []:
        return plurality_value(parent)
    # elif all examples have same classification
    elif all(examples[i][ind_exm_deci] == examples[0][ind_exm_deci] for i in range(len(examples))):
        return examples[0][ind_exm_deci]
    elif attributes == []:
        return plurality_value(examples)
    else:
        a_value = []
        for a in attributes:
            imp = Importance(a, examples)
            a_value.append(imp)
        A = attributes[a_value.index(max(a_value))]
        # tree = new tree with root test A
        new_tree = tree(A)
        for v in attributes_value[A]:
            exs = []
            for e in examples:
                index = attributes.index(A)
                if e[index] == v:
                    exs.append(e)
            subtree = Decision_Tree_Learning(exs, attributes, examples)
            new_tree.add_value(v)
            new_tree.add_children(subtree)
    return new_tree


def Importance(a, examp):
    p = 0.0
    n = 0.0
    ind = attributes.index(a)
    val = []
    for e in examp:
        val.append(e[ind])
        if e[ind_exm_deci] == 'Yes':
            p = p+1
        else: n = n+1
    val_list = list(set(val))
    num_val = len(val_list)
    pk = num_val * [0.0]
    nk = num_val * [0.0]
    for i in range(num_val):
        for e in examp:
            if e[ind] == val_list[i]:
                if e[ind_exm_deci] == 'Yes':
                    pk[i] = pk[i] + 1
                else: nk[i] = nk[i] + 1
    remainder = 0
    for j in range(num_val):
        remainder = remainder + (pk[j] + nk[j])/(p+n)*Bi(pk[j]/(pk[j] + nk[j]))
    gain = Bi(p/(p+n)) - remainder

    return gain


def Bi(x):
    if x == 0 or x == 1:
        return 0
    else:
        return - x * math.log(x,2) - (1-x) * math.log((1-x),2)

def plurality_value(example):
    whole = []
    for e in example:
        whole.append(e[ind_exm_deci])
    y = 0
    for i in range(len(whole)):
        if whole[i] == 'Yes':
            y = y+1
    n = len(whole) - y
    if y >= n: return 'Yes'
    else: return 'No'

decision = Decision_Tree_Learning(examples, attributes, examples)

# write the dtree.txt
output = open('dtree.txt', 'w')
output.write('% Format: decision? value, next node (leaf value or next decision?)\n')
output.write('% Use question mark and comma markers as indicated below.\n')


# do it by recursion function
def recur_func(decision):
    for child in decision.children:
        i = decision.children.index(child)
        if child in ['Yes', 'No']:
            output.write(str(decision.name) + '? ' + str(attributes_value[decision.name][i]) + ', ' + str(child) + '\n')
        else:
            output.write(str(decision.name) + '? ' + str(attributes_value[decision.name][i]) + ', ' + str(child.name) + '\n')
            recur_func(child)

recur_func(decision)

output.close()
