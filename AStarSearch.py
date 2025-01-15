import queue

G = {} # A12 : B11 C6 D8 E7
E = {} # (A, C) : 7
V = []
start, end = '', ''

class Node:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return f'{self.name}{self.value}'

    def __lt__(self, other):
        return self.value <= other.value

def read_file(filename):
    global start, end, G, E, V
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        start, end = lines[0].strip().split(' ')
        v = []
        for var in lines[1].strip().split(' '):
            v.append(Node(var[0], int(var[1:])))
        V = v
        for node in v:
            G[node.name] = []

        for line in lines[2:]:
            tmp = line.strip().split(' ')
            G[tmp[0]].append(tmp[1])
            E[(tmp[0], tmp[1])] = E.get((tmp[0], tmp[1]), int(tmp[2]))

def find_node(V, start):
    for v in V:
        if v.name == start:
            return v

def sort_list(q):
    nodes = []
    # Get
    while q.qsize():
        nodes.append(q.get())
    nodes = sorted(nodes)
    # Put again
    for node in nodes:
        q.put(node)

def A_star(G, E, V, start, end):
    Q = queue.Queue()
    start_node = find_node(V, start)
    Q.put(start_node)
    g = {start:0}
    parent = {start:None}

    while Q.qsize():
        current_node = Q.get()

        if current_node.name == end:
            print("Min width:", current_node.value)
            print('Way: ' + '->'.join(min_path(parent, end)))
            break

        next_nodes = G[current_node.name]
        for node in next_nodes:
            h = find_node(V, node).value
            k = E[(current_node.name, node)]
            g[node] = g[current_node.name] + k
            f = g[node] + h
            Q.put(Node(node, f))
            if node not in parent:
                parent[node] = current_node.name

        sort_list(Q)
        print(*Q.queue)

def min_path(parent, end):
    path = []
    current_path = end
    while current_path is not None:
        path.append(current_path)
        current_path = parent[current_path]
    path.reverse()
    return path

if __name__ == '__main__':
    read_file('input_3.txt')
    A_star(G, E, V, start, end)