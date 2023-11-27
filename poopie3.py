from collections import defaultdict

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)

    def add_edge(self, u, v):
        self.graph[u].append(v)

    def fleury(self, u):
        # Алгоритм Флёри для поиска Эйлерова цикла
        cycle = []
        stack = [u]

        while stack:
            current_vertex = stack[-1]

            if self.graph[current_vertex]:
                next_vertex = self.graph[current_vertex].pop()
                edge = (current_vertex, next_vertex)
                if edge not in cycle and edge[::-1] not in cycle:
                    cycle.append(edge)
                    stack.append(next_vertex)
            else:
                stack.pop()

        return cycle

    def eulerian_cycle_union_find(self):
        # Алгоритм поиска Эйлерова цикла на основе объединения простых циклов
        class UnionFind:
            def __init__(self, n):
                self.parent = list(range(n))
                self.rank = [0] * n

            def find(self, x):
                if self.parent[x] != x:
                    self.parent[x] = self.find(self.parent[x])
                return self.parent[x]

            def union(self, x, y):
                root_x, root_y = map(self.find, (x, y))
                if root_x != root_y:
                    self.parent[root_y] = root_x
                    self.rank[root_x] += self.rank[root_x] == self.rank[root_y]

        uf = UnionFind(self.V)
        cycle = [(u, v) for u in self.graph for v in self.graph[u] if uf.union(u, v)]

        return cycle

    def kosaraju(self):
        # Алгоритм Косарайю для нахождения сильно связанных компонент
        visited = set()
        stack = []

        def dfs(v, component):
            visited.add(v)
            component.append(v)
            stack.extend(neigh for neigh in self.graph[v] if neigh not in visited)

        for i in range(self.V):
            if i not in visited:
                dfs(i, [])

        reversed_graph = self.get_transpose()

        scc_components = []

        while stack:
            current_vertex = stack.pop()
            if current_vertex not in visited:
                current_component = []
                dfs(current_vertex, current_component)
                scc_components.append(current_component)

        return scc_components

    def get_transpose(self):
        # Получение транспонированного графа
        reversed_graph = Graph(self.V)
        for i in self.graph:
            for j in self.graph[i]:
                reversed_graph.add_edge(j, i)
        return reversed_graph

# Пример использования
g = Graph(4)
g.add_edge(1, 2)
g.add_edge(2, 3)
g.add_edge(3, 4)
g.add_edge(4, 1)
g.add_edge(1, 3)

result_fleury = g.fleury(1)
print("Флери:", result_fleury)

result_union_find = g.eulerian_cycle_union_find()
print("Эйлиров цикл с объединением:", result_union_find)

result_kosaraju = g.kosaraju()
print("Косарайю):", result_kosaraju)
