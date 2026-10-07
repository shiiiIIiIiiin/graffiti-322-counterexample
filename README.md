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

## Notes on the definitions and on earlier work

**Why "range" is the number of distinct values.**

- The glossary of Brewster, Dinneen and Faber (p. 54) defines the range of a vector as "the number of distinct components",
  and separately the scope as "the difference between the largest and the smallest components".
  These authors tested Graffiti's conjectures by computer in 1990–91, and *Written on the Wall* (comment to conjecture 107)
  lists 322 among the conjectures that passed their test on all graphs with at most 10 vertices.
- *Written on the Wall* uses both words: conjecture 323, the next one, is about "the scope of positive eigenvalues".
- The survey of Aouchiche and Hansen (2010) also takes the range to be the number of distinct values
  (as reported in Section 5.2 of Roucairol and Cazenave, cited below).
- If "range" is read as the largest eigenvalue minus the smallest, the inequality is trivial. For a connected graph with
  n ≥ 2 vertices, the largest eigenvalue of the distance matrix is at least n − 1 (Rayleigh quotient of the all-ones vector)
  and the smallest is at most −1 (Rayleigh quotient of e_i − e_j), so their difference is at least n,
  while Inverse Even ≤ n because Even(v) ≥ 1.

So conjecture 322 is settled under either reading: it is false with the glossary's definition (the graph above),
and trivially true with the other one.

**The 4-cycle is not a counterexample.**
M. Roucairol and T. Cazenave, *Refutation of Spectral Graph Theory Conjectures with Search Algorithms*
([arXiv:2409.18626](https://arxiv.org/abs/2409.18626), ECAI 2025), Section 5.2, report that with the "number of distinct values"
reading their programs refute 322 with the cycle of length 4 ("the cycle of size 4 has 3 distinct distance eigenvalues and
an Inverse Even of 4"). They suspected an error in the definitions ("An error with the definitions seems more likely than
this conjecture being left open after dozens of articles with such a simple counter-example") and ran their search
with the largest eigenvalue minus the smallest instead, finding no counterexample among triangle-free graphs with up to
50 vertices (their Table 1, where 322 is listed as open).
Their computation counts the vertices at even distance without the vertex itself; this is where Inverse Even = 4
comes from ([code](https://github.com/RoucairolMilo/refutationGBR/blob/main/src/models/conjectures/invariants.rs)).
With the definition above (distance zero included), every vertex of the 4-cycle has Even = 2, so Inverse Even = 2,
and the distance matrix has eigenvalues 4, 0, −2, −2, so the range is 3. The inequality 2 ≤ 3 holds.
This agrees with the 1990–91 test, which covered all graphs with at most 10 vertices.

**Why Even counts the vertex itself.**
The glossary says "at even distance (including zero)". *Written on the Wall* agrees: the remark of Shearer quoted below
gives Even = 254 = 1 + 253 for the graph of this repository, not 253.

**Summary of the readings.**

| range | Even(v) counts v itself | conjecture 322 |
|---|---|---|
| number of distinct values (glossary) | yes (glossary) | false: the graph above. True for all graphs with at most 10 vertices (1990–91 test) |
| number of distinct values | no | false already for the 4-cycle (Roucairol and Cazenave). The graph above also violates it (2048/253 > 4) |
| largest minus smallest | yes or no | trivially true for n ≥ 2 |

**Novelty.**
To our knowledge, the graph above is the first counterexample to conjecture 322 under the glossary's definitions
(first row of the table).
The conjecture was listed as open by Roucairol and Cazenave (2024), following the survey of Aouchiche and Hansen (2010).
On 2026-10-07 we found no earlier counterexample in the literature or in the public records of current computer-assisted
work on these conjectures that we know of; we cannot exclude unpublished work.
By the 1990–91 test, any counterexample has more than 10 vertices; the smallest one is not known.

The graph itself is not new: *Written on the Wall* already mentions it, in a remark of J. B. Shearer (July 1988) on how small
the mean of Even can be ("the mean of Even/n = 254/2048").

References for this section:
M. Aouchiche, P. Hansen, *A survey of automated conjectures in spectral graph theory*, Linear Algebra Appl. 432 (2010) 2293–2322;
M. Roucairol, T. Cazenave, arXiv:2409.18626.

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
