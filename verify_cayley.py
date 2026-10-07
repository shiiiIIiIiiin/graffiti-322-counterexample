"""Independent check of the counterexample to Graffiti conjecture 322 (pure Python 3, exact).

The coset graph of the binary Golay code is the Cayley graph on the group F_2[x]/(g(x))
(the syndromes, isomorphic to F_2^11) with the 23 generators x^i mod g, i = 0..22.
For a Cayley graph on an elementary abelian 2-group, the distance matrix D(a, b) = d(a + b)
is diagonalised by the characters, so its eigenvalues are, for each u,

    lambda_u = sum_s d(s) * (-1)^{<u, s>}.

This script uses only that fact and integer arithmetic; it shares no code with
build_graph.py or verify_certificate.py.
"""
from collections import Counter, deque
from fractions import Fraction

G_POLY = 0b110001110101  # x^11+x^10+x^6+x^5+x^4+x^2+1
ORDER = 1 << 11


def mod_g(a):
    for b in range(a.bit_length() - 1, 10, -1):
        if a >> b & 1:
            a ^= G_POLY << (b - 11)
    return a


def main():
    gens = [mod_g(1 << i) for i in range(23)]
    assert len(set(gens)) == 23 and 0 not in gens
    gset = set(gens)
    # a triangle would need g_i + g_j = g_k, i.e. a codeword of weight 3
    assert not any((a ^ b) in gset for a in gens for b in gens if a != b)
    print("23 distinct generators; triangle-free: yes")

    dist = [-1] * ORDER
    dist[0] = 0
    queue = deque([0])
    while queue:
        x = queue.popleft()
        for g in gens:
            y = x ^ g
            if dist[y] < 0:
                dist[y] = dist[x] + 1
                queue.append(y)
    assert min(dist) >= 0, "not connected"
    print(f"connected: yes, distance counts from a vertex: {sorted(Counter(dist).items())}")

    # distance-regular: for x at distance i from 0, the numbers of neighbours of x at distance
    # i - 1, i, i + 1 from 0 depend only on i (translations are automorphisms, so vertex 0 suffices)
    counts = {}
    for x in range(ORDER):
        c = Counter(dist[x ^ g] - dist[x] for g in gens)
        assert counts.setdefault(dist[x], c) == c, "not distance-regular"
    diam = max(dist)
    b = [counts[i][1] for i in range(diam)]
    c = [counts[i][-1] for i in range(1, diam + 1)]
    assert (b, c) == ([23, 22, 21], [1, 2, 3])
    print(f"distance-regular with intersection array {{{', '.join(map(str, b))}; {', '.join(map(str, c))}}}")

    # vertex-transitive, so every vertex has the same Even value
    even = sum(1 for d in dist if d % 2 == 0)  # includes distance 0
    inv_even = Fraction(ORDER, even)
    print(f"Even(v) = {even} for every v; Inverse Even = {inv_even} = {float(inv_even):.6f}")

    spectrum = Counter()
    for u in range(ORDER):
        spectrum[sum(d if bin(u & s).count("1") % 2 == 0 else -d for s, d in enumerate(dist))] += 1
    print(f"distance spectrum: {dict(sorted(spectrum.items()))}")
    rng = len(spectrum)
    print(f"range (number of distinct eigenvalues) = {rng}")
    assert inv_even > rng
    print(f"VIOLATED: Inverse Even = {float(inv_even):.6f} > {rng} = range")


if __name__ == "__main__":
    main()
