#include <iostream>
#include <vector>
#include <stack>
#include <algorithm>

class GraphDFS {
private:
    int vertices;
    std::vector<std::vector<int>> adjMatrix;
    std::vector<bool> visited;
    std::vector<bool> recStack;
    std::vector<int> parent;
    std::vector<int> cyclePath;

    bool dfsUtil(int v, std::vector<int>& path) {
        visited[v] = true;
        recStack[v] = true;
        path.push_back(v);

        // Check all adjacent vertices
        for (int u = 0; u < vertices; u++) {
            if (adjMatrix[v][u] == 1) { // If there's an edge from v to u
                if (!visited[u]) {
                    parent[u] = v;
                    if (dfsUtil(u, path)) {
                        return true;
                    }
                }
                else if (recStack[u]) {
                    // Found a back edge, indicating a cycle
                    cyclePath.clear();
                    
                    // Find the start of cycle in the path
                    auto it = std::find(path.begin(), path.end(), u);
                    if (it != path.end()) {
                        cyclePath.assign(it, path.end());
                        cyclePath.push_back(u); // Complete the cycle
                    }
                    return true;
                }
            }
        }

        recStack[v] = false;
        path.pop_back();
        return false;
    }

public:
    GraphDFS(int v) : vertices(v) {
        adjMatrix.resize(v, std::vector<int>(v, 0));
        visited.resize(v, false);
        recStack.resize(v, false);
        parent.resize(v, -1);
    }

    void addEdge(int u, int v) {
        adjMatrix[u][v] = 1;
    }

    void printMatrix() {
        std::cout << "\nAdjacency Matrix:\n";
        std::cout << "   ";
        for (int i = 0; i < vertices; i++) {
            std::cout << i << " ";
        }
        std::cout << "\n";
        
        for (int i = 0; i < vertices; i++) {
            std::cout << i << ": ";
            for (int j = 0; j < vertices; j++) {
                std::cout << adjMatrix[i][j] << " ";
            }
            std::cout << "\n";
        }
    }

    bool isCyclic() {
        // Reset arrays for fresh detection
        std::fill(visited.begin(), visited.end(), false);
        std::fill(recStack.begin(), recStack.end(), false);
        std::fill(parent.begin(), parent.end(), -1);
        cyclePath.clear();

        // Call DFS for all vertices
        for (int i = 0; i < vertices; i++) {
            if (!visited[i]) {
                std::vector<int> path;
                if (dfsUtil(i, path)) {
                    return true;
                }
            }
        }
        return false;
    }

    void printCycle() {
        if (!cyclePath.empty()) {
            std::cout << "Cycle found: ";
            for (int i = 0; i < cyclePath.size(); i++) {
                std::cout << cyclePath[i];
                if (i < cyclePath.size() - 1) {
                    std::cout << " -> ";
                }
            }
            std::cout << std::endl;
        }
    }
};

int main() {
    std::cout << "=== Graph Cycle Detection using DFS ===\n";
    
    // Hardcoded graph: D→A, E→A, A→C, C→E, C→F, C→G, C→B, F→B
    // Vertex mapping: A=0, B=1, C=2, D=3, E=4, F=5, G=6
    int vertices = 7;
    GraphDFS graph(vertices);
    
    std::cout << "Using predefined graph:\n";
    std::cout << "Vertices: A=0, B=1, C=2, D=3, E=4, F=5, G=6\n";
    std::cout << "Edges: D->A, E->A, A->C, C->E, C->F, C->G, C->B, F->B\n";
    
    // Add edges: D->A, E->A, A->C, C->E, C->F, C->G, C->B, F->B
    graph.addEdge(3, 0);  // D -> A
    graph.addEdge(4, 0);  // E -> A
    graph.addEdge(0, 2);  // A -> C
    graph.addEdge(2, 4);  // C -> E
    graph.addEdge(2, 5);  // C -> F
    graph.addEdge(2, 6);  // C -> G
    graph.addEdge(2, 1);  // C -> B
    graph.addEdge(5, 1);  // F -> B
    
    graph.printMatrix();
    
    if (graph.isCyclic()) {
        std::cout << "\nGraph contains a cycle!\n";
        graph.printCycle();
    } else {
        std::cout << "\nGraph does not contain a cycle.\n";
    }
    
    return 0;
} 