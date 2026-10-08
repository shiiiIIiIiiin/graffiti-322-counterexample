"""Conjecture 322 on the coset graphs of the punctured binary Golay codes (pure Python 3, exact).

Deleting the coordinates P from the Golay code [23,12,7] gives a code [23 - |P|, 12] whose coset graph is
the Cayley graph on F_2[x]/(g(x)) / W with the generators x^i mod g(x), i not in P, where W is spanned by
x^j mod g(x), j in P. Each vertex is stored as the smallest element of its class.

  P = {}       2048 vertices, code [23,12,7]   (the counterexample of verify_cayley.py)
  P = {22}     1024 vertices, code [22,12,6]   (a smaller counterexample)
  P = {21, 22}  512 vertices, code [21,12,5]   (the inequality holds)

As in verify_cayley.py, the distance matrix of such a Cayley graph is diagonalised by the characters u
with <u, w> = 0 for all w in W, with eigenvalues sum_x d(x) * (-1)^{<u, x>}.

With --write-data, also writes data/edges-1024.txt and data/vertices-1024.txt
(checked from the edge list alone by `python verify_certificate.py data/edges-1024.txt`).
"""
import sys
from collections import Counter, deque
from fractions import Fraction
from pathlib import Path

G_POLY = 0b110001110101  # x^11+x^10+x^6+x^5+x^4+x^2+1

EXPECTED = {  # deleted coordinates -> (intersection array, conjecture 322 fails)
    (): (([23, 22, 21], [1, 2, 3]), True),
    (22,): (([22, 21, 20], [1, 2, 6]), True),
    (21, 22): (([21, 20, 16], [1, 2, 12]), False),
}


def mod_g(a):
    for b in range(a.bit_length() - 1, 10, -1):
        if a >> b & 1:
            a ^= G_POLY << (b - 11)
    return a


def parity(x):
    return bin(x).count("1") & 1


def coset_graph(punct):
    s = [mod_g(1 << i) for i in range(23)]
    W = {0}
    for j in punct:
        W |= {w ^ s[j] for w in W}

    def rep(x):
        return min(x ^ w for w in W)

    classes = sorted({rep(x) for x in range(1 << 11)})
    gens = [rep(s[i]) for i in range(23) if i not in punct]
    assert len(set(gens)) == len(gens) and 0 not in gens, "loops or multiple edges"
    return W, rep, classes, gens


def check(punct):
    W, rep, classes, gens = coset_graph(punct)
    n = len(classes)
    gset = set(gens)
    # a triangle would need g_i + g_j = g_k in the quotient
    assert not any(rep(a ^ b) in gset for a in gens for b in gens if a != b), "triangle found"

    dist = {0: 0}
    queue = deque([0])
    while queue:
        x = queue.popleft()
        for g in gens:
            y = rep(x ^ g)
            if y not in dist:
                dist[y] = dist[x] + 1
                queue.append(y)
    assert len(dist) == n, "not connected"

    counts = {}
    for x in classes:
        c = Counter(dist[rep(x ^ g)] - dist[x] for g in gens)
        assert counts.setdefault(dist[x], c) == c, "not distance-regular"
    diam = max(dist.values())
    b = [counts[i][1] for i in range(diam)]
    c = [counts[i][-1] for i in range(1, diam + 1)]

    # vertex-transitive, so every vertex has the same Even value
    even = sum(1 for d in dist.values() if d % 2 == 0)  # includes distance 0
    inv_even = Fraction(n, even)

    chars = [u for u in range(1 << 11) if all(parity(u & w) == 0 for w in W)]
    assert len(chars) == n
    spectrum = Counter(sum(-d if parity(u & x) else d for x, d in dist.items()) for u in chars)
    rng = len(spectrum)
    fails = inv_even > rng

    print(f"code [{23 - len(punct)},12], deleted coordinates {sorted(punct)}: {n} vertices, "
          f"{len(gens)}-regular, triangle-free")
    print(f"  distance counts from a vertex: {sorted(Counter(dist.values()).items())}")
    print(f"  distance-regular with intersection array {{{', '.join(map(str, b))}; {', '.join(map(str, c))}}}")
    print(f"  Even(v) = {even} for every v; Inverse Even = {inv_even} = {float(inv_even):.6f}")
    print(f"  distance spectrum: {dict(sorted(spectrum.items()))}; range = {rng}")
    print(f"  {'VIOLATED' if fails else 'holds'}: Inverse Even = {float(inv_even):.6f} "
          f"{'>' if fails else '<='} {rng} = range")
    assert ((b, c), fails) == EXPECTED[tuple(sorted(punct))]


def write_data(punct, n_expected):
    W, rep, classes, gens = coset_graph(punct)
    assert len(classes) == n_expected
    index = {x: k for k, x in enumerate(classes)}
    edges = sorted({(min(index[x], index[rep(x ^ g)]), max(index[x], index[rep(x ^ g)]))
                    for x in classes for g in gens})
    out = Path(__file__).with_name("data")
    out.mkdir(exist_ok=True)
    with open(out / f"vertices-{n_expected}.txt", "w", newline="\n") as f:
        f.write("# index, then the exponents of the smallest element of the class in F_2[x]/(g(x));\n"
                f"# the class is that element plus the span of x^j mod g(x), j in {sorted(punct)}\n")
        for x in classes:
            f.write(" ".join(map(str, [index[x]] + [i for i in range(11) if x >> i & 1])) + "\n")
    with open(out / f"edges-{n_expected}.txt", "w", newline="\n") as f:
        f.write(f"# coset graph of the punctured binary Golay code [{23 - len(punct)},12]: "
                f"{n_expected} vertices, {len(edges)} edges\n")
        for u, v in edges:
            f.write(f"{u} {v}\n")
    print(f"wrote {n_expected} vertices and {len(edges)} edges to {out}")


def main():
    for punct in EXPECTED:
        check(set(punct))
    if "--write-data" in sys.argv:
        write_data({22}, 1024)


if __name__ == "__main__":
    main()
