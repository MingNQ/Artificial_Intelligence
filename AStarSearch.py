import queue

class Node:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return f'{self.name}{self.value}'

    def __lt__(self, other):
        return self.value <= other.value
    
class A_Star:
    def __init__(self):
        self.start = None
        self.end = None
        self.G = {}
        self.E = {}
        self.V = []
        self.lines = []

        self.read_file('input_3.txt')
        self.search()
        self.write_file()

    def read_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            self.start, self.end = lines[0].strip().split(' ')
            for var in lines[1].strip().split(' '):
                self.V.append(Node(var[0], int(var[1:])))

            for node in self.V:
                self.G[node.name] = []

            for line in lines[2:]:
                tmp = line.strip().split(' ')
                self.G[tmp[0]].append(tmp[1])
                self.E[(tmp[0], tmp[1])] = self.E.get((tmp[0], tmp[1]), int(tmp[2]))

    def search(self):
        L = []
        start_node = self.find_node(self.start)
        L.append(start_node)
        g = {self.start:0}
        parent = {self.start:None}
        title = f"{"TT".ljust(5)} | {"TTK".ljust(5)} | {"k(u, v)".ljust(8)} | {"h(v)".ljust(5)} | {"g(u)".ljust(5)} | {"f(v)".ljust(5)} | {"DSL".ljust(20)}"
        print(title)
        self.lines.append(title + '\n')

        while True:
            if len(L) <= 0:
                print("ERROR: No path found")
                return

            current_node = L.pop(0)
            
            if current_node.name == self.end:
                ttkt = f"{current_node.name.ljust(5)} | TTKT -> STOP"
                path = 'Path: ' + ' -> '.join(self.min_path(parent, self.end))
                min_width = f"Min width: {current_node.value}"
                
                self.lines.append(f"{ttkt}\n{path}\n{min_width}\n")
                print(f"{ttkt}\n{path}\n{min_width}\n")
                return

            next_nodes = self.G[current_node.name]
            i = 0
            output = [""] * len(next_nodes)
            output[i] = f"{current_node.name.ljust(5)} | "

            for node in next_nodes:
                k = self.E[(current_node.name, node)]
                h = self.find_node(node).value
                g[node] = g[current_node.name] + k
                f = g[node] + h
                L.append(Node(node, f))
                output[i] += f"{node.ljust(5)} | {str(k).ljust(8)} | {str(h).ljust(5)} | {str(g[node]).ljust(5)} | {str(f).ljust(5)} | "
                i += 1
                
                parent[node] = current_node.name

            L.sort()
            output[0] += f"{' '.join([str(n) for n in L])}"
            self.print_state(output)

    def find_node(self, start):
        for v in self.V:
            if v.name == start:
                return v

    def min_path(self, parent, end):
        path = []
        current_path = end
        while current_path is not None:
            path.append(current_path)
            current_path = parent[current_path]
        path.reverse()
        return path

    def print_state(self, output):
        for j in range(1, len(output)):
            output[j] = ' '.ljust(5) + " | " + output[j]
        print('\n'.join(output))
        self.lines.append('\n'.join(output) + '\n')

    def write_file(self):
        with open('output.txt', 'w', encoding='utf-8') as file:
            file.writelines(self.lines)

if __name__ == '__main__':
    A_Star()