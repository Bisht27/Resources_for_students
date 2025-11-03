# GGSIPU – UNIT III ASSIGNMENT
Marks: 30 | Duration: 30 Minutes

## Instructions
- Answer only what is asked in 20–40 words or a short pseudocode/recurrence. [1]
- Provide core DP/BB formulations, not full code. [1]
- Clarity and correctness over length. [1]

## SECTION A – Short Theory [15 Marks]

1) DP essentials  
- List the three ingredients of DP and one-line purpose of each. [2][1]

2) DP vs D&C  
- State two differences focusing on subproblem overlap and reuse; give one example for each. [2][1]

3) Principle of optimality  
- Define it in one sentence and name any one problem satisfying it. [3][4]

4) Memoization  
- Define memoization and contrast with tabulation in one line each. [1]

5) Branch and Bound idea  
- Define BnB and the role of bounding in pruning in two lines. [5][6]

## SECTION B – Algorithms & Recurrences [15 Marks]

6) Matrix Chain Multiplication (A₁:5×4, A₂:4×6, A₃:6×2, A₄:2×7)  
a) Write m[i,j] recurrence and base case (no derivation). [4][7][8]  
b) State the minimum scalar multiplications (number only). [8][4]

7) Longest Common Subsequence (X="ABCDGH", Y="AEDFHR")  
a) Write the LCS(i,j) recurrence and base. [1]  
b) Give the LCS length (number only). [1]

8) Optimal Binary Search Tree (keys: 10,20,30; p: 0.4,0.3,0.3; assume q=0)  
a) Write w[i,j] and e[i,j] DP formulations with base. [1]  
b) State the minimum expected search cost (number only). [1]

9) 0/1 Knapsack – Branch & Bound (W=5; w={2,3,4,5}, p={3,4,5,6})  
a) Write the fractional upper bound formula used for pruning. [6][9][5]  
b) Show level-0 and level-1 nodes (include/exclude first item) with (v,w,ub) only. [5][6]

10) TSP – Dynamic Programming (Held–Karp; 4 cities, example D given)  
a) Write the C[S,j] recurrence and final answer expression. [1]  
b) Initialize base entries C[{k},k] for k=2..4 (numbers only for the given D). [1]

## Submission
- Submit `Unit3_Assignment_<YourName>.md` to GitHub Classroom; use fenced code blocks for recurrences/pseudocode. [10]

