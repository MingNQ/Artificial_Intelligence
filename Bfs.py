import queue
from queue import Queue

start = ''
end = ''
lst = {}
lines = [
    "Curr       |Next                  |Queue\n"
]

# Read file
def input(filename):
    global start, end
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        start, end = lines[0].strip().split(' ')
        for d in lines[1].strip().split(' '):
            lst[d] = []

        for i in range(2, len(lines)):
            tmp = lines[i].strip().split(' ')
            lst[tmp[0]] = tmp[1:]

# Bfs to find path
def bfs(start, end):
    global lines
    q = queue.Queue()
    q.put(start)
    parent = {start : None}
    lines.append(f"{' '.ljust(10)} | {' '.ljust(20)} | {' '.join(q.queue)}\n")

    while q.qsize() > 0:
        curr = q.get()
        out = curr
        if curr == end:
            lines.append(f"{curr.ljust(10)} | {'End'.ljust(20)} | {' '.join(q.queue)}\n")
            break

        next = lst[curr]
        for i in range(len(next)):
            if next[i] not in parent:
                parent[next[i]] = curr
            q.put(next[i])

        # Format output
        lines.append(f"{curr.ljust(10)} | {' '.join(next).ljust(20)} | {' '.join(q.queue)}\n")

    # Path
    path = []
    current = end
    print(parent)
    while current is not None:
        path.append(current)
        current = parent.get(current)

    path.reverse()
    lines.append('->'.join(path) + '\n')

def output(filename, lines):
    with open('output.txt', 'w', encoding='utf-8') as file:
        file.writelines(lines)

if __name__ == '__main__':
    input("input.txt")
    bfs(start, end)
    output('output.txt', lines)