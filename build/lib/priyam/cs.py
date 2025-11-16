from typing import Dict, List, Tuple, Any
import heapq
from collections import deque


class GraphAlgorithms:
    """
    Classic graph algorithms: BFS, DFS, Dijkstra, topological sort, etc.
    Graph representation:
        - adjacency list: dict[node] -> list[(neighbor, weight)] for weighted graphs
        - dict[node] -> list[neighbor] for unweighted
    """

    @staticmethod
    def bfs(adj: Dict[Any, List[Any]], start: Any) -> List[Any]:
        """Breadth-first traversal from start (unweighted graph)."""
        visited = set()
        order = []
        q = deque([start])
        visited.add(start)
        while q:
            u = q.popleft()
            order.append(u)
            for v in adj.get(u, []):
                if v not in visited:
                    visited.add(v)
                    q.append(v)
        return order

    @staticmethod
    def dfs(adj: Dict[Any, List[Any]], start: Any) -> List[Any]:
        """Depth-first traversal from start (unweighted graph)."""
        visited = set()
        order = []

        def _dfs(u):
            visited.add(u)
            order.append(u)
            for v in adj.get(u, []):
                if v not in visited:
                    _dfs(v)

        _dfs(start)
        return order

    @staticmethod
    def dijkstra(
        adj: Dict[Any, List[Tuple[Any, float]]],
        source: Any
    ) -> Dict[Any, float]:
        """
        Dijkstra's shortest paths from source in a graph with non-negative weights.
        Returns dict of distances.
        """
        dist = {node: float("inf") for node in adj}
        dist[source] = 0.0
        pq = [(0.0, source)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for v, w in adj.get(u, []):
                nd = d + w
                if nd < dist.get(v, float("inf")):
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))
        return dist

    @staticmethod
    def topological_sort(adj: Dict[Any, List[Any]]) -> List[Any]:
        """
        Kahn's algorithm for DAG topological ordering.
        Raises ValueError if graph has a cycle.
        """
        in_deg = {u: 0 for u in adj}
        for u, neighbors in adj.items():
            for v in neighbors:
                in_deg[v] = in_deg.get(v, 0) + 1

        q = deque([u for u, d in in_deg.items() if d == 0])
        order = []

        while q:
            u = q.popleft()
            order.append(u)
            for v in adj.get(u, []):
                in_deg[v] -= 1
                if in_deg[v] == 0:
                    q.append(v)

        if len(order) != len(in_deg):
            raise ValueError("Graph has at least one cycle; topological sort impossible.")
        return order


class SearchingSorting:
    """
    Fundamental algorithms: binary search, quicksort, mergesort.
    """

    @staticmethod
    def binary_search(arr: List[Any], target: Any) -> int:
        """
        Return index of target in sorted arr, or -1 if not found.
        """
        lo, hi = 0, len(arr) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1

    @staticmethod
    def quicksort(arr: List[Any]) -> List[Any]:
        """In-place quicksort wrapper (returns the same list)."""
        def _qs(a, lo, hi):
            if lo >= hi:
                return
            pivot = a[(lo + hi) // 2]
            i, j = lo, hi
            while i <= j:
                while a[i] < pivot:
                    i += 1
                while a[j] > pivot:
                    j -= 1
                if i <= j:
                    a[i], a[j] = a[j], a[i]
                    i += 1
                    j -= 1
            _qs(a, lo, j)
            _qs(a, i, hi)

        _qs(arr, 0, len(arr) - 1)
        return arr

    @staticmethod
    def mergesort(arr: List[Any]) -> List[Any]:
        """Return a new list containing a sorted copy using mergesort."""
        if len(arr) <= 1:
            return arr[:]
        mid = len(arr) // 2
        left = SearchingSorting.mergesort(arr[:mid])
        right = SearchingSorting.mergesort(arr[mid:])
        return SearchingSorting._merge(left, right)

    @staticmethod
    def _merge(left: List[Any], right: List[Any]) -> List[Any]:
        i = j = 0
        out = []
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                out.append(left[i])
                i += 1
            else:
                out.append(right[j])
                j += 1
        out.extend(left[i:])
        out.extend(right[j:])
        return out


class Complexity:
    """
    Very simple helpers for reasoning about algorithmic complexity.
    Not a formal analyzer – more of a structured documentation helper.
    """

    @staticmethod
    def big_o_notation(operation: str) -> str:
        """
        Return typical time complexity for a named operation.
        This is illustrative and can be extended.

        Examples:
            'binary_search' -> 'O(log n)'
            'quicksort_avg' -> 'O(n log n)'
            'quicksort_worst' -> 'O(n^2)'
        """
        mapping = {
            "binary_search": "O(log n)",
            "linear_search": "O(n)",
            "quicksort_avg": "O(n log n)",
            "quicksort_worst": "O(n^2)",
            "mergesort": "O(n log n)",
            "bfs": "O(V + E)",
            "dfs": "O(V + E)",
            "dijkstra": "O((V + E) log V)",
        }
        return mapping.get(operation, "Unknown / not defined")

class DynamicProgramming:
    """
    Classic DP patterns, both as utilities and as reference implementations.
    """

    @staticmethod
    def knapSack_01(weights: List[int], values: List[int], capacity: int) -> int:
        """
        0/1 Knapsack: maximize sum(values) with sum(weights) <= capacity.
        Returns maximum achievable value.
        Time: O(n * capacity).
        """
        n = len(weights)
        dp = [0] * (capacity + 1)
        for i in range(n):
            w = weights[i]
            v = values[i]
            # iterate backwards for 0/1
            for c in range(capacity, w - 1, -1):
                dp[c] = max(dp[c], dp[c - w] + v)
        return dp[capacity]

    @staticmethod
    def longest_increasing_subsequence(arr: List[int]) -> int:
        """
        LIS in O(n log n).
        Returns length of LIS.
        """
        import bisect
        tails: List[int] = []
        for x in arr:
            idx = bisect.bisect_left(tails, x)
            if idx == len(tails):
                tails.append(x)
            else:
                tails[idx] = x
        return len(tails)

    @staticmethod
    def edit_distance(s1: str, s2: str) -> int:
        """
        Levenshtein edit distance DP.
        """
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                cost = 0 if s1[i - 1] == s2[j - 1] else 1
                dp[i][j] = min(
                    dp[i - 1][j] + 1,      # deletion
                    dp[i][j - 1] + 1,      # insertion
                    dp[i - 1][j - 1] + cost  # substitution
                )
        return dp[m][n]


class GreedyPatterns:
    """
    Simple greedy algorithm patterns.
    """

    @staticmethod
    def activity_selection(intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Select maximum number of non-overlapping intervals (start, finish)
        using earliest-finish-time greedy algorithm.
        """
        intervals_sorted = sorted(intervals, key=lambda x: x[1])
        res = []
        last_finish = -float("inf")
        for s, f in intervals_sorted:
            if s >= last_finish:
                res.append((s, f))
                last_finish = f
        return res
