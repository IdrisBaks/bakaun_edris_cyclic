#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>

class GraphBFS {
private:
    int vertices;
    std::vector<std::vector<int>> adjMatrix;
    std::vector<int> parent;
    std::vector<bool> visited;
    std::vector<int> cyclePath;

    bool bfsUtil(int start) {
        std::queue<int> q;
        std::vector<bool> localVisited(vertices, false);
        std::vector<int> localParent(vertices, -1);
        
        q.push(start);
        localVisited[start] = true;

        while (!q.empty()) {
            int current = q.front();
            q.pop();

            // Check all adjacent vertices
            for (int neighbor = 0; neighbor < vertices; neighbor++) {
                if (adjMatrix[current][neighbor] == 1) { // If there's an edge
                    if (!localVisited[neighbor]) {
                        localVisited[neighbor] = true;
                        localParent[neighbor] = current;
                        q.push(neighbor);
                    }
                    else if (localParent[current] != neighbor) {
                        // Found a cycle - trace back to find the cycle path
                        cyclePath.clear();
                        
                        // Build the cycle path
                        std::vector<int> pathToCurrent;
                        std::vector<int> pathToNeighbor;
                        
                        // Trace path from current to start
                        int temp = current;
                        while (temp != -1) {
                            pathToCurrent.push_back(temp);
                            temp = localParent[temp];
                        }
                        
                        // Trace path from neighbor to start
                        temp = neighbor;
                        while (temp != -1) {
                            pathToNeighbor.push_back(temp);
                            temp = localParent[temp];
                        }
                        
                        // Find common ancestor (LCA)
                        std::reverse(pathToCurrent.begin(), pathToCurrent.end());
                        std::reverse(pathToNeighbor.begin(), pathToNeighbor.end());
                        
                        int lca = -1;
                        int minLen = std::min(pathToCurrent.size(), pathToNeighbor.size());
                        
                        for (int i = 0; i < minLen; i++) {
                            if (pathToCurrent[i] == pathToNeighbor[i]) {
                                lca = pathToCurrent[i];
                            } else {
                                break;
                            }
                        }
                        
                        // Build cycle path
                        if (lca != -1) {
                            // Add path from LCA to current (excluding LCA)
                            auto lcaIt = std::find(pathToCurrent.begin(), pathToCurrent.end(), lca);
                            if (lcaIt != pathToCurrent.end()) {
                                cyclePath.assign(lcaIt, pathToCurrent.end());
                            }
                            
                            // Add path from neighbor back to LCA (excluding neighbor, including LCA)
                            auto neighborLcaIt = std::find(pathToNeighbor.begin(), pathToNeighbor.end(), lca);
                            if (neighborLcaIt != pathToNeighbor.end()) {
                                for (auto it = std::find(pathToNeighbor.begin(), pathToNeighbor.end(), neighbor); 
                                     it != neighborLcaIt; --it) {
                                    cyclePath.push_back(*it);
                                }
                            }
                        } else {
                            // Simple cycle between current and neighbor
                            cyclePath.push_back(current);
                            cyclePath.push_back(neighbor);
                            cyclePath.push_back(current);
                        }
                        
                        return true;
                    }
                }
            }
        }
        return false;
    }

public:
    GraphBFS(int v) : vertices(v) {
        adjMatrix.resize(v, std::vector<int>(v, 0));
        parent.resize(v, -1);
        visited.resize(v, false);
    }

    void addEdge(int u, int v) {
        adjMatrix[u][v] = 1;
        // For undirected graph, uncomment the next line:
        // adjMatrix[v][u] = 1;
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
        std::fill(visited.begin(), visited.end(), false);
        cyclePath.clear();

        // Check each component
        for (int i = 0; i < vertices; i++) {
            if (!visited[i]) {
                if (bfsUtil(i)) {
                    return true;
                }
                // Mark all vertices in this component as visited
                std::queue<int> q;
                q.push(i);
                visited[i] = true;
                
                while (!q.empty()) {
                    int current = q.front();
                    q.pop();
                    
                    for (int neighbor = 0; neighbor < vertices; neighbor++) {
                        if (adjMatrix[current][neighbor] == 1 && !visited[neighbor]) {
                            visited[neighbor] = true;
                            q.push(neighbor);
                        }
                    }
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
    std::cout << "=== Graph Cycle Detection using BFS ===\n";
    
    // Hardcoded graph: D→A, E→A, A→C, C→E, C→F, C→G, C→B, F→B
    // Vertex mapping: A=0, B=1, C=2, D=3, E=4, F=5, G=6
    int vertices = 7;
    GraphBFS graph(vertices);
    
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