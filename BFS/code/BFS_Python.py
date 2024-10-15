from collections import deque

adjList = [
    [1, 4],    # Vertex 0 is connected to vertices 1 and 4
    [0, 2, 4], # Vertex 1 is connected to vertices 0, 2, and 4
    [1, 3],    # Vertex 2 is connected to vertices 1 and 3
    [2, 4],    # Vertex 3 is connected to vertices 2 and 4
    [0, 1, 3]  # Vertex 4 is connected to vertices 0, 1, and 3
]

def BFS(startVer):
    totVer=len(adjList)
    visited=[False]*totVer
    visited[startVer]=True

    q=deque([startVer])
    while q:
        vertex=q.popleft()
        print(vertex, end=" ")
        for av in adjList[vertex]:
            if not visited[av]:
                q.append(av)
                visited[av]=True


BFS(0)
                
