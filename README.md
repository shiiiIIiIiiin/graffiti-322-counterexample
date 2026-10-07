# A counterexample to Graffiti conjecture 322

[日本語](README.ja.md)

Shin Kimura (木村心), 2026-10-07

Found with the help of AI (Claude by Anthropic).

## Conjecture

S. Fajtlowicz, *Written on the Wall* (July 2004 version), conjecture 322:

> If G is a triangle-free graph then the Inverse Even ≤ range of eigenvalues of Distance.

Terms, as defined in the glossary of T. L. Brewster, M. J. Dinneen, V. Faber,
*A computational attack on the conjectures of Graffiti: New counterexamples and proofs*,
Discrete Math. 147 (1995) 35–55:

- **Even vector** (p. 52): the i-th component is the number of vertices at even distance (including zero) from vertex i.
- **Inverse** of a vector (p. 53): the sum of the reciprocals of the nonzero components.
- **Range** of a vector (p. 54): the number of distinct components.
  (The difference between the largest and the smallest components is called the **scope**.)

So the conjecture states: for every triangle-free graph,
Σ_v 1/Even(v) ≤ (number of distinct eigenvalues of the distance matrix).

## Counterexample

The coset graph of the binary Golay code [23,12,7]
(2048 vertices, 23-regular, triangle-free, distance-regular with intersection array {23,22,21; 1,2,3}).

- Edge list: [`data/edges.txt`](data/edges.txt) (vertices 0–2047, 23552 edges)
- Vertex labels: [`data/vertices.txt`](data/vertices.txt) (the coset leader of each vertex)

| | value |
|---|---|
| distances from any vertex | 1 vertex at distance 0, 23 at 1, 253 at 2, 1771 at 3 |
| Even(v) | 1 + 253 = 254 for every v |
| Inverse Even | 2048/254 = 1024/127 ≈ 8.063 |
| distance spectrum | 5842¹, 10¹²⁸⁸, −14²⁵³, −30⁵⁰⁶ (exponents are multiplicities) |
| range of eigenvalues of Distance | 4 |

Since 1024/127 > 4, the inequality fails.

Construction: the vertices are the elements of F₂[x]/(g(x)) with
g(x) = x¹¹ + x¹⁰ + x⁶ + x⁵ + x⁴ + x² + 1, and two vertices are adjacent when they differ by x^i mod g(x)
for some i = 0, …, 22.

## Verification

| script | method | requires |
|---|---|---|
| `verify_certificate.py` | reads only `data/edges.txt`; computes distances, the Even vector and Inverse Even exactly, and certifies the distance spectrum exactly (∏(D − rI) = 0 in integer arithmetic, multiplicities from tr(Dᵏ)) | Python 3, numpy |
| `verify_cayley.py` | builds the graph as a Cayley graph on F₂¹¹ and computes the distance spectrum exactly with characters | Python 3 |
| `build_graph.py` | regenerates `data/` from the Golay code (coset leaders of weight ≤ 3) | Python 3 |

```
python verify_certificate.py
python verify_cayley.py
```

## License

Code: MIT (see `LICENSE`). Text and data: CC BY 4.0.
