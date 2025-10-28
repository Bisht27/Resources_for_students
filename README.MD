# UNIT III & IV – Theory + Algorithm Practice  
**Total: 60 Marks | Duration: 2 Hours**  
**Instructions:** Write only concise, clear answers (20–50 words). Keep code brief with essential logic.

---

## Theory (Short Answers)

### 1. Polynomial Time Reducibility
A problem A is polynomial-time reducible to B if any instance of A can be transformed into an instance of B in polynomial time.  
**Example:** 3-SAT ≤p Clique problem.

---

### 2. NP Packet Graph vs NP Scheduling Problem
**NP Packet Graph:** Verifying if a graph property (e.g., Hamiltonian path) can be checked in polynomial time.  
**NP Scheduling Problem:** Assigning jobs to machines to minimize time; verification feasible in polynomial time.

---

### 3. Non-Deterministic Algorithm
A non-deterministic algorithm can choose among many possible paths simultaneously and accepts if any path leads to a solution.  
**Example:** Guessing a path in Hamiltonian Cycle and verifying it.

---

### 4. State Space Tree
It represents the search space of a problem as a tree of states.  
**Searching Methods:** Depth-First Search (DFS), Breadth-First Search (BFS).

---

### 5. Boolean Satisfiability (SAT) Problem
It asks whether a Boolean formula can be made true by some assignment of variables.  
**Example:** (x ∨ y') ∧ (x' ∨ y) is satisfiable with x = true, y = true.

---

### 6. Cook’s Theorem
It states that SAT is NP-complete.  
**Application:** It proves the existence of NP-complete problems forming the basis for NP-completeness proofs.

---

### 7. P, NP, NP-Complete, NP-Hard

| Class | Meaning | Examples |
|--------|----------|-----------|
| P | Solvable in polynomial time | Sorting, BFS |
| NP | Verifiable in polynomial time | SAT, Hamiltonian Cycle |
| NP-Complete | NP problems reducible to each other | 3-SAT, Clique |
| NP-Hard | As hard as NP-Complete, not necessarily in NP | TSP (optimization), Halting Problem |

---

### 8. Hamiltonian Cycle in NP
A Hamiltonian Cycle exists if a path visits all vertices once and returns to the start. It’s in NP since a proposed cycle can be verified in polynomial time.

---

## Algorithms & Coding Logic

### 9. Dijkstra’s Algorithm
**Core Logic:** Repeatedly select the node with minimum distance and update its adjacent distances.

