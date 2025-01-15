import queue

V = []
G = {}
start, end = '', ''

class Node:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return f'{self.name}{self.value}'

    def __lt__(self, other):
        return self.value <= other.value

def read_file(filename, g:{}, v:[]):
    global start, end
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        start, end = lines[0].strip().split(' ')
        for var in lines[1].strip().split(' '):
            v.append(Node(var[0], int(var[1:])))

        for node in v:
            g[node] = []

        for line in lines[2:]:
            tmp = line.strip().split(' ')
            node = find_node(v, tmp[0])
            if node:
                for val in tmp[1:]:
                    g[node].append(val)

def find_node(v, d):
    for node in v:
        if node.name == d:
            return node

def best_first_search(g, v):
    global start, end

    Q = queue.Queue()
    start_node = find_node(v, start)
    Q.put(start_node)
    P = {start_node.name : None}

    print(f'{'Curr'.ljust(5)} {'Next'.ljust(15)} Queue')
    while Q.qsize():
        curr_node = Q.get()
        if curr_node.value == 0:
            break

        next_node = g[curr_node]
        for val in next_node:
            tmp_node = find_node(v, val)
            Q.put(tmp_node)
            P[val] = curr_node.name

        my_sort(Q, v) # Sort after put
        print_screen(curr_node, next_node, Q)
    find_path(P, end)

def climbing_hill(g, v):
    global start, end

    L = queue.LifoQueue()
    start_node = find_node(v, start)
    L.put(start_node)
    P = {start_node.name: None}

    print(f'{'Curr'.ljust(5)} {'Next'.ljust(15)} {'L1 List'.ljust(15)} L List')
    while L.qsize():
        curr_node = L.get()
        if curr_node.value == 0:
            break

        next_node = g[curr_node]
        L1 = []
        for val in next_node:
            tmp_node = find_node(v, val)
            L1.append(tmp_node)
            P[val] = curr_node.name

        for node in sorted(L1, reverse=True):
            L.put(node)

        print_screen_v2(curr_node, next_node, L1, L)
    find_path(P, end)

def find_path(parent, end):
    path = []
    curr_path = end
    while curr_path is not None:
        path.append(curr_path)
        curr_path = parent[curr_path]
    path.reverse()
    print('->'.join(path))

def print_screen_v2(curr, next_node, l1, l):
    global V
    curr_node = f'{curr.name}{curr.value}'
    next_node_val = []
    for node in next_node:
        tmp = find_node(V, node)
        if tmp:
            next_node_val.append(f'{tmp.name}{tmp.value}')

    l1_after = []
    l_after = []
    for node in l1:
        l1_after.append(f'{node.name}{node.value}')
    for node in l.queue:
        l_after.append(f'{node.name}{node.value}')
    l_after.reverse()
    print(f'{curr_node.ljust(5)} {' '.join(next_node_val).ljust(15)} {' '.join(l1_after).ljust(15)} {' '.join(l_after)}')

def print_screen(curr, next_node, q):
    global V
    curr_node = f'{curr.name}{curr.value}'
    next_node_val = []
    for node in next_node:
        tmp = find_node(V, node)
        if tmp:
            next_node_val.append(f'{tmp.name}{tmp.value}')

    print(f'{curr_node.ljust(5)} {' '.join(next_node_val).ljust(15)}', *q.queue)

def my_sort(q, v):
    nodes = []
    # Get
    while q.qsize():
        nodes.append(q.get())
    nodes = sorted(nodes)
    # Put again
    for node in nodes:
        q.put(node)

if __name__ == '__main__':
    read_file('input_2.txt', G, V)

    ok = False
    while not ok:
        print("Choose algorithm")
        print("1. Best-First Search")
        print("2. Climbing Hill")
        print("3. End")
        choose = int(input())

        if choose == 1:
            best_first_search(G, V)
        elif choose == 2:
            climbing_hill(G, V)
        elif choose == 3:
            ok = True
        else:
            print("Invalid input")

        input()