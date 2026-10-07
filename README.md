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

This section makes two points.

1. Conjecture 322 was not open simply because nobody had looked at it.
2. With the definitions of the Graffiti glossary, the graph above is, to our knowledge, the first counterexample,
   and there are good reasons to read the conjecture with these definitions.

### 1. The conjecture had been examined before

| year | who | what |
|---|---|---|
| 1990–91 | Brewster, Dinneen, Faber | Tested about 200 of Graffiti's conjectures on all graphs with at most 10 vertices and refuted over 40 of them. *Written on the Wall* (comment to conjecture 107) lists 322 among the conjectures that passed. |
| 2024 | Roucairol, Cazenave | Searched for counterexamples to Graffiti's spectral conjectures with eight search algorithms, working from the survey of Aouchiche and Hansen (2010). 322 is one of the conjectures they report as still open (their Table 1). |
| 2026 | this repository | Repeated the test on all connected triangle-free graphs with at most 10 vertices (11569 graphs, exact arithmetic, `check_small.py`): no counterexample. The graph above, with 2048 vertices, is a counterexample. |

So the conjecture was known, it was listed as open, and it had been tested by computer.
No counterexample has at most 10 vertices, which is why an exhaustive test did not settle it.
The smallest counterexample is not known.

The search of 2024 used other definitions (Section 5.2 of the paper), so it was not a test of the conjecture
as defined in the glossary:

- With the range as the number of distinct values, their programs returned the cycle of length 4:
  "the cycle of size 4 has 3 distinct distance eigenvalues and an Inverse Even of 4".
  The value 4 comes from counting the vertices at even distance without the vertex itself ([code](https://github.com/RoucairolMilo/refutationGBR/blob/main/src/models/conjectures/invariants.rs)).
  With the glossary's definition, every vertex of the 4-cycle has Even = 2, so Inverse Even = 2;
  the distance matrix has eigenvalues 4, 0, −2, −2, so the range is 3; and 2 ≤ 3.
  The 4-cycle is not a counterexample.
- The authors did not accept the 4-cycle as a refutation ("An error with the definitions seems more likely than
  this conjecture being left open after dozens of articles with such a simple counter-example").
  They took the range to be the largest eigenvalue minus the smallest instead, and found no counterexample among
  triangle-free graphs with up to 50 vertices. With that reading the inequality is trivially true (see below),
  so no search could have found one.

### 2. The reading under which this is the first counterexample

The graph above is a counterexample when

- the **range** of a vector is the number of its distinct values, and
- **Even(v)** counts v itself (distance zero).

Reasons for reading the conjecture this way:

- **The glossary.** Brewster, Dinneen and Faber, who tested the conjectures with Graffiti's vocabulary, define
  Range as "The number of distinct components" (p. 54),
  Scope as "The difference between the largest and the smallest components" (p. 54),
  and the Even vector by "the number of vertices an even distance (including zero) from vertex i" (p. 52).
- ***Written on the Wall* uses "range" and "scope" for different quantities.**
  Conjectures 82 and 83 are the same statement with the two words exchanged
  ("range [scope] of coordinates of a maximal clique ≤ maximum of Even").
  According to the comments, 82 "is valid for all maximal cliques", while for 83 a counterexample
  "to the strongest version" was found (W. Staton, March 1988).
  Conjecture 323, next to 322, is about "the scope of positive eigenvalues".
- **Conjecture 578 separates the two meanings.**
  It reads: "If G is a tree then the radius ≤ range of positive eigenvalues. Siemion Fajtlowicz. February 89."
  With the number of distinct values this is true: a tree of diameter d has at least d + 1 distinct eigenvalues,
  placed symmetrically about 0, hence at least ⌈d/2⌉ distinct positive ones, and ⌈d/2⌉ is the radius of the tree.
  With the largest minus the smallest it fails for a single edge: the only positive eigenvalue is 1,
  so the difference is 0, while the radius is 1.
- ***Written on the Wall* counts the vertex itself in Even.**
  For the graph of this repository it records "the mean of Even/n = 254/2048"
  (remark of J. B. Shearer, July 1988), and 254 = 1 + 253.
- **The survey.** Aouchiche and Hansen (2010) also take the range to be the number of distinct values
  (as reported in Section 5.2 of Roucairol and Cazenave).
- **The other reading makes the conjecture trivial.**
  Suppose the range is the largest eigenvalue minus the smallest. For a connected graph with n ≥ 2 vertices,
  the largest eigenvalue of the distance matrix is at least n − 1 (Rayleigh quotient of the all-ones vector)
  and the smallest is at most −1 (Rayleigh quotient of e_i − e_j), so the range is at least n,
  while Inverse Even ≤ n. The inequality would hold for every connected graph,
  and the hypothesis "triangle-free" would play no role.

Summary of the readings:

| range | Even(v) counts v itself | conjecture 322 |
|---|---|---|
| number of distinct values (glossary) | yes (glossary) | false: the graph above. No counterexample with at most 10 vertices |
| number of distinct values | no | false already for the 4-cycle (Roucairol and Cazenave). The graph above also violates it (2048/253 > 4) |
| largest minus smallest | yes or no | trivially true for n ≥ 2 |

**The claim.**
Under the glossary's definitions (first row of the table), the graph above is, to our knowledge,
the first counterexample to conjecture 322.
On 2026-10-07 we found no earlier counterexample in the literature or in the public records of current computer-assisted
work on these conjectures that we know of; we cannot exclude unpublished work.
The claim depends on the reading: if Even(v) does not count v (second row), the 4-cycle came first.

**What is new.**
The graph itself is not new: *Written on the Wall* already mentions it, in the remark of Shearer quoted above,
which is about how small the mean of Even can be.
What is new is the observation that its distance matrix has only four distinct eigenvalues,
so that it violates conjecture 322.

References for this section:
M. Aouchiche, P. Hansen, *A survey of automated conjectures in spectral graph theory*, Linear Algebra Appl. 432 (2010) 2293–2322;
M. Roucairol, T. Cazenave, *Refutation of Spectral Graph Theory Conjectures with Search Algorithms*,
[arXiv:2409.18626](https://arxiv.org/abs/2409.18626) (ECAI 2025).

## Verification

| script | method | requires |
|---|---|---|
| `verify_certificate.py` | reads only `data/edges.txt`; computes distances, the Even vector and Inverse Even exactly, and certifies the distance spectrum exactly (∏(D − rI) = 0 in integer arithmetic, multiplicities from tr(Dᵏ)) | Python 3, numpy |
| `verify_cayley.py` | builds the graph as a Cayley graph on F₂¹¹ and computes the distance spectrum exactly with characters | Python 3 |
| `build_graph.py` | regenerates `data/` from the Golay code (coset leaders of weight ≤ 3) | Python 3 |
| `check_small.py` | generates all connected triangle-free graphs with at most 10 vertices (11569 graphs up to isomorphism; the counts agree with OEIS A024607) and checks the inequality in exact arithmetic: no counterexample. Also shows that the 4-cycle is the first violation when Even(v) does not count v | Python 3 |

```
python verify_certificate.py
python verify_cayley.py
python check_small.py
```

## License

Code: MIT (see `LICENSE`). Text and data: CC BY 4.0.
