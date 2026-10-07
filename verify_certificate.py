"""Check the counterexample to Graffiti conjecture 322 from the edge list alone.

Reads data/edges.txt and verifies, without using any structure of the Golay code:
  1. the graph is simple, connected and triangle-free;
  2. Inverse Even = sum over v of 1/Even(v), where Even(v) counts the vertices at even
     distance from v, including v itself (computed exactly as a fraction);
  3. the distance matrix D has exactly 4 distinct eigenvalues (range = 4):
     the candidate eigenvalues are located numerically, then certified exactly by
       - the integer identity  prod_i (D - r_i I) = 0, and
       - the multiplicities obtained from tr(D^k), k = 0..3, which must be positive integers;
  4. Inverse Even > range, i.e. conjecture 322 fails.

Requires numpy. Integer matrix products are computed with float64 BLAS and certified exact
(see exact_matmul).
"""
from collections import Counter
from fractions import Fraction
from pathlib import Path

import numpy as np

TWO53 = float(2 ** 53)


def exact_matmul(X, Y):
    """Product of two integer matrices via float64, certified exact.

    Every partial sum in entry (i, j) of X @ Y is bounded in absolute value by
    (|X| @ |Y|)[i, j]. If that bound is below 2^53, all partial sums are integers that
    float64 represents exactly, so the floating-point product equals the integer product
    regardless of summation order.
    """
    Xf, Yf = X.astype(np.float64), Y.astype(np.float64)
    bound = np.abs(Xf) @ np.abs(Yf)
    assert bound.max() < TWO53, "entries too large for an exact float64 product"
    return np.rint(Xf @ Yf).astype(np.int64)


def read_edges(path):
    edges = []
    for line in open(path):
        if line.startswith("#") or not line.strip():
            continue
        u, v = map(int, line.split())
        edges.append((u, v))
    return edges


def main():
    edges = read_edges(Path(__file__).with_name("data") / "edges.txt")
    n = 1 + max(max(e) for e in edges)
    A = np.zeros((n, n), dtype=np.int64)
    for u, v in edges:
        assert u != v, "loop"
        assert A[u, v] == 0, "multiple edge"
        A[u, v] = A[v, u] = 1
    m = len(edges)
    print(f"n = {n}, m = {m}")

    # triangle-free: no edge has a common neighbour
    nbr = [set(np.flatnonzero(A[i]).tolist()) for i in range(n)]
    assert all(not (nbr[u] & nbr[v]) for u, v in edges), "triangle found"
    print("triangle-free: yes")

    # all distances by breadth-first search on 0/1 matrices (float products of 0/1 are exact)
    Af = A.astype(np.float64)
    D = np.full((n, n), -1, dtype=np.int64)
    np.fill_diagonal(D, 0)
    frontier = np.eye(n, dtype=bool)
    reached = frontier.copy()
    k = 0
    while frontier.any():
        k += 1
        frontier = ((frontier.astype(np.float64) @ Af) > 0) & ~reached
        D[frontier] = k
        reached |= frontier
    assert reached.all(), "graph is not connected"
    print(f"connected: yes, diameter {D.max()}, distance counts from vertex 0: "
          f"{np.bincount(D[0]).tolist()}")

    # Even vector (distance 0 counts as even) and Inverse Even
    even = (D % 2 == 0).sum(axis=1)
    inv_even = sum(Fraction(1, int(e)) for e in even)
    print(f"Even vector values: {dict(Counter(even.tolist()))}")
    print(f"Inverse Even = {inv_even} = {float(inv_even):.6f}")

    # eigenvalues of D: locate numerically, then certify exactly
    approx = np.linalg.eigvalsh(D.astype(np.float64))
    roots = sorted(set(int(round(x)) for x in approx))
    assert np.max(np.abs(approx - np.round(approx))) < 1e-6, "eigenvalues are not near integers"
    print(f"candidate eigenvalues (numerical): {roots}")

    I = np.eye(n, dtype=np.int64)
    P = I.copy()
    for r in sorted(roots, key=abs, reverse=True):  # largest factor first keeps entries small
        P = exact_matmul(P, D - r * I)
    assert not P.any(), "the product of (D - r I) is not zero"
    print(f"exact check: prod (D - r I) = 0 over the {len(roots)} candidates")

    D2 = exact_matmul(D, D)
    traces = [n, int(np.trace(D)), int(np.trace(D2)), int((D2 * D.T).sum())]
    k_ = len(roots)
    V = [[Fraction(r) ** p for r in roots] for p in range(k_)]
    b = [Fraction(t) for t in traces[:k_]]
    # solve the Vandermonde system V mult = b exactly (Gaussian elimination over Q)
    M = [row[:] + [b[i]] for i, row in enumerate(V)]
    for c in range(k_):
        piv = next(r for r in range(c, k_) if M[r][c] != 0)
        M[c], M[piv] = M[piv], M[c]
        for r in range(k_):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    mult = [M[i][k_] / M[i][i] for i in range(k_)]
    assert all(x.denominator == 1 and x > 0 for x in mult), mult
    spectrum = {r: int(x) for r, x in zip(roots, mult)}
    assert sum(spectrum.values()) == n
    print(f"distance spectrum (exact): {spectrum}")

    rng = len(spectrum)
    print(f"range of eigenvalues of Distance = {rng} (number of distinct eigenvalues)")
    print(f"conjecture 322 requires {inv_even} <= {rng}")
    assert inv_even > rng
    print(f"VIOLATED: Inverse Even = {float(inv_even):.6f} > {rng} = range")


if __name__ == "__main__":
    main()
