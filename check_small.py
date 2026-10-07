"""Exhaustive check of Graffiti conjecture 322 on small graphs (pure Python 3, exact).

Generates, up to isomorphism, all connected triangle-free graphs with at most N vertices
(default N = 10) and checks for each of them

    Inverse Even <= number of distinct eigenvalues of the distance matrix,

with the definitions of the glossary of Brewster, Dinneen and Faber: Even(v) is the number
of vertices at even distance from v, v itself included.

Graphs are built one vertex at a time. A connected triangle-free graph always has a vertex
whose removal leaves a connected graph, and the neighbours of that vertex form a nonempty
independent set; so every such graph on n + 1 vertices is obtained from one on n vertices
by adding a vertex joined to a nonempty independent set. Isomorphic copies are removed,
and the numbers of graphs are compared with OEIS A024607.

The number of distinct eigenvalues is computed exactly. The distance matrix is symmetric,
so this number is the number of distinct roots of its characteristic polynomial p,
i.e. deg p - deg gcd(p, p').

The script also reports what happens when Even(v) does not count v itself.

Usage: python check_small.py [N]
"""
import sys
import time
from fractions import Fraction

# connected triangle-free graphs on 1, 2, 3, ... vertices
A024607 = [1, 1, 1, 3, 6, 19, 59, 267, 1380, 9832, 90842, 1144061]


def bits(mask):
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask ^= low


def distances(adj):
    """Distance matrix of a connected graph given by adjacency bitmasks."""
    n = len(adj)
    dist = []
    for s in range(n):
        row = [0] * n
        seen = frontier = 1 << s
        d = 0
        while frontier:
            d += 1
            reached = 0
            for v in bits(frontier):
                reached |= adj[v]
            frontier = reached & ~seen
            for v in bits(frontier):
                row[v] = d
            seen |= frontier
        dist.append(row)
    return dist


def vertex_invariants(adj, dist):
    n = len(adj)
    deg = [bin(a).count("1") for a in adj]
    return [(tuple(sorted(dist[v])), tuple(sorted(deg[u] for u in bits(adj[v])))) for v in range(n)]


def isomorphic(a, inv_a, b, inv_b):
    """Backtracking test; a vertex may only be mapped to a vertex with the same invariant."""
    n = len(a)
    image = [0] * n

    def extend(v, used):
        if v == n:
            return True
        for w in range(n):
            if used >> w & 1 or inv_a[v] != inv_b[w]:
                continue
            if all((a[v] >> u & 1) == (b[w] >> image[u] & 1) for u in range(v)):
                image[v] = w
                if extend(v + 1, used | 1 << w):
                    return True
        return False

    return extend(0, 0)


def extensions(adj):
    """All graphs obtained by adding a vertex joined to a nonempty independent set."""
    n = len(adj)
    independent = [True] * (1 << n)
    for s in range(1, 1 << n):
        low = (s & -s).bit_length() - 1
        rest = s & (s - 1)
        independent[s] = independent[rest] and not adj[low] & rest
        if independent[s]:
            yield tuple(a | (s >> v & 1) << n for v, a in enumerate(adj)) + (s,)


def next_level(graphs):
    buckets = {}
    for adj, _ in graphs:
        for ext in extensions(adj):
            dist = distances(ext)
            inv = vertex_invariants(ext, dist)
            bucket = buckets.setdefault(tuple(sorted(inv)), [])
            if not any(isomorphic(ext, inv, other, other_inv) for other, other_inv, _ in bucket):
                bucket.append((ext, inv, dist))
    return [(adj, dist) for bucket in buckets.values() for adj, _, dist in bucket]


def charpoly(m):
    """Characteristic polynomial of an integer matrix (Faddeev-LeVerrier), leading coefficient first."""
    n = len(m)
    coeffs = [1]
    aux = [[int(i == j) for j in range(n)] for i in range(n)]
    for k in range(1, n + 1):
        prod = [[sum(m[i][t] * aux[t][j] for t in range(n)) for j in range(n)] for i in range(n)]
        trace = sum(prod[i][i] for i in range(n))
        assert trace % k == 0
        c = -trace // k
        coeffs.append(c)
        for i in range(n):
            prod[i][i] += c
        aux = prod
    return coeffs


def poly_rem(a, b):
    a = a[:]
    while len(a) >= len(b):
        q = a[0] / b[0]
        for i in range(len(b)):
            a[i] -= q * b[i]
        a.pop(0)
    while a and a[0] == 0:
        a.pop(0)
    return a


def distinct_roots(p):
    """Number of distinct roots of the polynomial p: deg p - deg gcd(p, p')."""
    n = len(p) - 1
    a = [Fraction(c) for c in p]
    b = [c * (n - i) for i, c in enumerate(a[:-1])]
    while b:
        a, b = b, poly_rem(a, b)
    return n - (len(a) - 1)


def invariants(dist):
    """Inverse Even (v counted), Inverse Even (v not counted), number of distinct distance eigenvalues."""
    even = [sum(d % 2 == 0 for d in row) for row in dist]
    inverse_even = sum(Fraction(1, e) for e in even)
    inverse_even_excl = sum(Fraction(1, e - 1) for e in even if e > 1)
    return inverse_even, inverse_even_excl, distinct_roots(charpoly(dist))


def edges(adj):
    return " ".join(f"{u}-{v}" for u in range(len(adj)) for v in bits(adj[u]) if u < v)


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    start = time.time()

    c4 = (0b1010, 0b0101, 0b1010, 0b0101)
    assert invariants(distances(c4)) == (2, 4, 3)

    level = [((0,), [[0]])]
    total = violations = violations_excl = 0
    first_excl = None
    counts_ok = True
    print(" n  graphs  A024607  violations  min(range - Inverse Even)  violations if Even(v) does not count v")
    for n in range(1, nmax + 1):
        if n > 1:
            level = next_level(level)
        bad = bad_excl = 0
        slack = None
        for adj, dist in level:
            inverse_even, inverse_even_excl, rng = invariants(dist)
            if slack is None or rng - inverse_even < slack:
                slack = rng - inverse_even
            if inverse_even > rng:
                bad += 1
                print(f"    VIOLATION: Inverse Even = {inverse_even} > {rng}; edges: {edges(adj)}")
            if inverse_even_excl > rng:
                bad_excl += 1
                if first_excl is None:
                    first_excl = (n, inverse_even_excl, rng, edges(adj))
        expected = A024607[n - 1] if n <= len(A024607) else None
        counts_ok = counts_ok and expected in (None, len(level))
        total += len(level)
        violations += bad
        violations_excl += bad_excl
        print(f"{n:2d} {len(level):7d} {str(expected):>8s} {bad:11d} {str(slack):>26s} {bad_excl:11d}", flush=True)

    print(f"\n{total} connected triangle-free graphs with at most {nmax} vertices; "
          f"counts agree with OEIS A024607: {counts_ok}")
    print(f"violations of conjecture 322 (Even(v) counts v): {violations}")
    print(f"violations when Even(v) does not count v: {violations_excl}")
    if first_excl:
        n, inverse_even_excl, rng, e = first_excl
        print(f"  first one: n = {n}, Inverse Even = {inverse_even_excl} > {rng}, edges: {e}")
    print(f"time: {time.time() - start:.0f} s")
    if violations or not counts_ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
