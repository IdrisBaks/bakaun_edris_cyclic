# Graph Cycle Detection: DFS vs BFS Implementation

## Overview

This project implements and compares two fundamental graph algorithms for cycle detection: **Depth-First Search (DFS)** and **Breadth-First Search (BFS)**. The program demonstrates how both algorithms can identify cycles in directed graphs, showcasing their different approaches and characteristics.

## Sample Graph Structure

The program uses a predefined directed graph with the following vertices and connections:

### Vertices
- **A** (index 0) - Central hub vertex
- **B** (index 1) - Terminal vertex  
- **C** (index 2) - Distribution vertex
- **D** (index 3) - Source vertex
- **E** (index 4) - Loop participant
- **F** (index 5) - Intermediate vertex
- **G** (index 6) - Terminal vertex

### Edges (Directed)
```
D → A    (D feeds into A)
E → A    (E feeds into A)  
A → C    (A distributes to C)
C → E    (C connects back to E, creating a cycle)
C → F    (C branches to F)
C → G    (C branches to G)
C → B    (C connects to B)
F → B    (F also connects to B)
```

### Graph Visualization
```
D ──┐
    ├──→ A ──→ C ──┬──→ E
E ──┘           │    ↑  
                │    │  
                │    └──┘ (CYCLE: A→C→E→A)
                │
                ├──→ F ──→ B
                ├──→ G
                └──→ B
```

## Algorithm Implementations

### 1. Depth-First Search (DFS) - `cyclic_dfs.cpp`

**Approach**: Uses recursion and a recursion stack to detect back edges.

**Key Features**:
- Maintains a `visited` array to track explored vertices
- Uses `recStack` to identify vertices in the current recursion path
- Detects cycles when encountering a back edge (edge to a vertex in recursion stack)
- Tracks the complete cycle path for visualization

**Time Complexity**: O(V + E) where V = vertices, E = edges
**Space Complexity**: O(V) for recursion stack and auxiliary arrays

### 2. Breadth-First Search (BFS) - `cyclic_bfs.cpp`

**Approach**: Uses iterative exploration with queue-based traversal.

**Key Features**:
- Explores graph level by level using a queue
- Detects cycles by finding cross edges between visited vertices
- Implements Lowest Common Ancestor (LCA) logic to construct cycle paths
- Handles disconnected components systematically

**Time Complexity**: O(V + E) where V = vertices, E = edges  
**Space Complexity**: O(V) for queue and auxiliary arrays

## Files Structure

```
AC CYCLIC DFS, BFS/
├── cyclic_dfs.cpp     # DFS-based cycle detection
├── cyclic_bfs.cpp     # BFS-based cycle detection
└── README.md          # This documentation
```

## Compilation & Execution

### Prerequisites
- C++ compiler supporting C++11 or later (g++, clang++, etc.)

### Compile and Run DFS Implementation
```bash
g++ -o cyclic_dfs cyclic_dfs.cpp
./cyclic_dfs
```

### Compile and Run BFS Implementation
```bash
g++ -o cyclic_bfs cyclic_bfs.cpp
./cyclic_bfs
```

## Expected Output

Both programs will:
1. Display the adjacency matrix representation of the graph
2. Detect and report if a cycle exists
3. Show the specific cycle path found

### Sample Output (DFS):
```
=== Graph Cycle Detection using DFS ===
Using predefined graph:
Vertices: A=0, B=1, C=2, D=3, E=4, F=5, G=6
Edges: D->A, E->A, A->C, C->E, C->F, C->G, C->B, F->B

Adjacency Matrix:
   0 1 2 3 4 5 6 
0: 0 0 1 0 0 0 0 
1: 0 0 0 0 0 0 0 
2: 0 1 0 0 1 1 1 
3: 1 0 0 0 0 0 0 
4: 1 0 0 0 0 0 0 
5: 0 1 0 0 0 0 0 
6: 0 0 0 0 0 0 0 

Graph contains a cycle!
Cycle found: 0 -> 2 -> 4 -> 0
```

## Algorithm Comparison

| Aspect | DFS | BFS |
|--------|-----|-----|
| **Memory Usage** | Lower (recursion stack) | Higher (queue storage) |
| **Cycle Detection** | Direct via back edges | Complex via cross edges |
| **Implementation** | Recursive, elegant | Iterative, more complex |
| **Path Tracking** | Natural through recursion | Requires LCA computation |
| **Performance** | Generally faster | Slightly more overhead |

## Learning Objectives

This project demonstrates:
- **Graph Representation**: Adjacency matrix implementation
- **Traversal Algorithms**: DFS vs BFS comparison
- **Cycle Detection**: Different approaches to the same problem
- **Data Structures**: Usage of stacks, queues, and arrays
- **Algorithm Analysis**: Time and space complexity considerations

## Technical Details

### Graph Properties
- **Type**: Directed graph
- **Vertices**: 7 (labeled A through G)
- **Edges**: 8 directed connections
- **Cycles**: Contains at least one cycle (A→C→E→A)

### Implementation Features
- Object-oriented design with separate classes
- Adjacency matrix representation for fast edge lookups
- Comprehensive cycle path reconstruction
- Clear output formatting and debugging information

## Extensions & Modifications

The code can be easily modified to:
- Accept user input for custom graphs
- Handle undirected graphs
- Implement different graph representations (adjacency list)
- Add timing comparisons between algorithms
- Visualize the graph structure graphically

---

*This implementation serves as an educational tool for understanding fundamental graph algorithms and their practical applications in cycle detection.* 
