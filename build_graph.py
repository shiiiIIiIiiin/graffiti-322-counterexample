"""Build the coset graph of the binary Golay code [23,12,7] and write it to data/.

Vertices are the 2048 cosets of the code in F_2^23. Each coset is represented by its
unique leader, a vector of weight <= 3 (the code is perfect). Two cosets are adjacent
when they differ by a single unit vector e_i.

Output:
  data/vertices.txt  one line per vertex: "<index> <support of the coset leader>"
  data/edges.txt     one line per edge:   "<u> <v>" with u < v

Pure Python 3, no dependencies.
"""
from itertools import combinations
from pathlib import Path

N = 23
# generator polynomial of the cyclic binary Golay code: x^11+x^10+x^6+x^5+x^4+x^2+1
G_POLY = 0b110001110101


def clmul(a, b):
    """Carry-less (GF(2)[x]) product of two bit vectors."""
    r = 0
    while b:
        if b & 1:
            r ^= a
        a <<= 1
        b >>= 1
    return r


def weight(v):
    return bin(v).count("1")


def support(v):
    return [i for i in range(N) if v >> i & 1]


def build():
    # the code: all multiples m(x) g(x) with deg m <= 11 (degree <= 22, so no reduction)
    code = {clmul(m, G_POLY) for m in range(1 << 12)}
    assert len(code) == 4096
    wd = {}
    for c in code:
        wd[weight(c)] = wd.get(weight(c), 0) + 1
    assert min(w for w in wd if w > 0) == 7, wd
    assert wd == {0: 1, 7: 253, 8: 506, 11: 1288, 12: 1288, 15: 506, 16: 253, 23: 1}, wd

    # coset leaders: all vectors of weight <= 3 (1 + 23 + 253 + 1771 = 2048 = 2^23 / 4096)
    leaders = [0]
    for w in (1, 2, 3):
        for s in combinations(range(N), w):
            leaders.append(sum(1 << i for i in s))
    assert len(leaders) == 2048
    index = {v: k for k, v in enumerate(leaders)}

    # every 4-subset of the coordinates lies in exactly one weight-7 codeword (Steiner S(4,7,23))
    block_of = {}
    for c in code:
        if weight(c) == 7:
            for s in combinations(support(c), 4):
                key = sum(1 << i for i in s)
                assert key not in block_of
                block_of[key] = c
    assert len(block_of) == 8855  # = C(23,4)

    def leader_of(v):
        """Coset leader of a vector of weight <= 4."""
        if weight(v) <= 3:
            return v
        assert weight(v) == 4
        return v ^ block_of[v]  # v + c has weight 3 when v is inside the weight-7 codeword c

    edges = set()
    for a in leaders:
        for i in range(N):
            b = leader_of(a ^ (1 << i))
            assert b != a
            edges.add((min(index[a], index[b]), max(index[a], index[b])))
    degree = [0] * 2048
    for u, v in edges:
        degree[u] += 1
        degree[v] += 1
    assert set(degree) == {23}, "every coset has 23 distinct neighbours"
    return leaders, sorted(edges)


def main():
    leaders, edges = build()
    out = Path(__file__).with_name("data")
    out.mkdir(exist_ok=True)
    with open(out / "vertices.txt", "w", newline="\n") as f:
        f.write("# index, then the support (coordinates 0..22) of the coset leader\n")
        for k, v in enumerate(leaders):
            f.write(" ".join(map(str, [k] + support(v))) + "\n")
    with open(out / "edges.txt", "w", newline="\n") as f:
        f.write("# coset graph of the binary Golay code [23,12,7]: 2048 vertices, 23552 edges\n")
        for u, v in edges:
            f.write(f"{u} {v}\n")
    print(f"wrote {len(leaders)} vertices and {len(edges)} edges to {out}")


if __name__ == "__main__":
    main()
