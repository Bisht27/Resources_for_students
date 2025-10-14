import time
import random
import sys
import matplotlib.pyplot as plt

# Increase recursion limit if needed
sys.setrecursionlimit(10000)

def knapsack_recursive(weights, values, capacity, n):
    """
    Brute-force recursive solution (no memoization).
    Returns the maximum value using first n items with given capacity.
    Time complexity: O(2^n) in worst-case.
    """
    if n == 0 or capacity == 0:
        return 0
    if weights[n-1] > capacity:
        return knapsack_recursive(weights, values, capacity, n-1)
    else:
        without = knapsack_recursive(weights, values, capacity, n-1)
        with_item = values[n-1] + knapsack_recursive(weights, values, capacity - weights[n-1], n-1)
        return max(without, with_item)

def knapsack_memo(weights, values, capacity, n, memo=None):
    """
    Top-down DP with memoization.
    Uses a dict to cache computed (n, capacity) results.
    Complexity: O(n * capacity) (pseudo-polynomial).
    """
    if memo is None:
        memo = {}
    if n == 0 or capacity == 0:
        return 0
    key = (n, capacity)
    if key in memo:
        return memo[key]
    if weights[n-1] > capacity:
        result = knapsack_memo(weights, values, capacity, n-1, memo)
    else:
        without = knapsack_memo(weights, values, capacity, n-1, memo)
        with_item = values[n-1] + knapsack_memo(weights, values, capacity - weights[n-1], n-1, memo)
        result = max(without, with_item)
    memo[key] = result
    return result

def knapsack_dp(weights, values, capacity):
    """
    Bottom-up DP (tabulation).
    Build dp table where dp[i][w] = max value using first i items, capacity w.
    Complexity: O(n * capacity) time and space.
    """
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        wt = weights[i - 1]
        val = values[i - 1]
        for w in range(0, capacity + 1):
            # skip
            dp[i][w] = dp[i-1][w]
            # include if it fits
            if wt <= w:
                dp[i][w] = max(dp[i][w], val + dp[i-1][w - wt])
    return dp[n][capacity]

def measure_runtimes(ns, weight_val_generator, capacity_factor=3):
    """
    For each n in ns, generate random instance of size n,
    run the three methods (as feasible), record runtimes.
    Returns dict: method name -> list of runtimes (in seconds, or None if skipped).
    """
    runtimes = {
        'recursive': [],
        'memo': [],
        'dp': []
    }
    for n in ns:
        weights, values = weight_val_generator(n)
        capacity = capacity_factor * n  # capacity grows linearly in n
        # Recursive
        t0 = time.time()
        res_rec = None
        try:
            res_rec = knapsack_recursive(weights, values, capacity, n)
            t1 = time.time()
            runtimes['recursive'].append(t1 - t0)
        except (RecursionError, OverflowError):
            runtimes['recursive'].append(None)
        # Memo
        t0 = time.time()
        res_memo = knapsack_memo(weights, values, capacity, n, memo={})
        t1 = time.time()
        runtimes['memo'].append(t1 - t0)
        # DP
        t0 = time.time()
        res_dp = knapsack_dp(weights, values, capacity)
        t1 = time.time()
        runtimes['dp'].append(t1 - t0)
        # Sanity check
        if res_rec is not None:
            if not (res_dp == res_memo == res_rec):
                print(f"*** Mismatch at n={n}: rec={res_rec}, memo={res_memo}, dp={res_dp}")
        else:
            if res_dp != res_memo:
                print(f"*** Mismatch at n={n}: memo={res_memo}, dp={res_dp}")
        print(f"n={n}, capacity={capacity}, result={res_dp}")
    return runtimes

def random_weights_values(n, max_w=20, max_v=100):
    """
    Generate random weights and values arrays of length n.
    """
    weights = [random.randint(1, max_w) for _ in range(n)]
    values = [random.randint(1, max_v) for _ in range(n)]
    return weights, values

def plot_runtimes(ns, runtimes):
    """
    Plot the runtime curves for each method over ns.
    """
    plt.figure(figsize=(10, 6))
    # Plot each method, skipping None values
    for method, times in runtimes.items():
        # Prepare x and y filtering out None
        x = [ns[i] for i in range(len(ns)) if times[i] is not None]
        y = [times[i] for i in range(len(ns)) if times[i] is not None]
        plt.plot(x, y, marker='o', label=method)
    plt.xlabel("n (number of items)")
    plt.ylabel("Runtime (seconds)")
    plt.title("Runtime comparison: recursive vs memoization vs bottom-up DP")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    # Test sizes
    ns = [5,7, 10,12, 15,17, 20, 25]  # you can push to 40,50 but recursive will fail early
    runtimes = measure_runtimes(ns, random_weights_values, capacity_factor=4)
    # Print table
    print("\nRuntimes (seconds):")
    print("n\t recursive\t\t memo\t\t dp")
    for i, n in enumerate(ns):
        rr = runtimes['recursive'][i]
        rm = runtimes['memo'][i]
        rd = runtimes['dp'][i]
        print(f"{n}\t{rr}\t{rm}\t{rd}")
    # Plot
    plot_runtimes(ns, runtimes)
    return runtimes

if __name__ == "__main__":
    main()
