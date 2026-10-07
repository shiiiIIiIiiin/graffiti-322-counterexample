# A counterexample to Graffiti conjecture 322

[日本語](README.ja.md)

Shin Kimura (木村心), 2026-10-07

Found with the help of AI (Claude by Anthropic).

Numbers in square brackets refer to the [references](#references) at the end; page numbers of [1] refer to the copy listed there.

## Conjecture

S. Fajtlowicz, *Written on the Wall* (July 2004 version), conjecture 322 [1, p. 82]:

> If G is a triangle-free graph then the Inverse Even ≤ range of eigenvalues of Distance.

Terms, as defined in the glossary of T. L. Brewster, M. J. Dinneen and V. Faber [2]:

- **Even vector** [2, p. 52]: "The vector whose ith component is the number of vertices an even distance (including zero) from vertex i."
- **Inverse** of a vector [2, p. 53]: "The sum of the reciprocals of the nonzero components."
- **Range** of a vector [2, p. 54]: "The number of distinct components."
  (The **scope** [2, p. 54] is "The difference between the largest and the smallest components.")

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

Every property stated in this section is checked by the scripts below: `build_graph.py` checks that g(x) generates
a code with minimum distance 7 and the weight distribution of the Golay code, and `verify_cayley.py` checks
triangle-freeness, the distances, the intersection array, Even and the spectrum.

## Notes on the definitions and on earlier work

This section makes three points.

1. Conjecture 322 was not open simply because nobody had looked at it.
2. The 4-cycle, reported in 2024 as a counterexample under one reading, is not a counterexample under the glossary [2].
3. With the definitions of the glossary [2], the graph above is, to our knowledge, the first reported counterexample,
   and there are good reasons to read the conjecture with these definitions.

### 1. The conjecture was not neglected

It was tested by computer, listed as open, and taken up again by a search in 2024.
Each of these had a limit that explains why the counterexample was not found.

| year | who | what they did | why it did not find the counterexample |
|---|---|---|---|
| 1990–91 | Brewster, Dinneen, Faber [2] | Tested "approximately 200 of the Graffiti conjectures" on "all the nonisomorphic graphs with 10 or fewer vertices" and found "counterexamples for over 40 of them" [2, p. 35]. *Written on the Wall* lists 322 among "the conjectures which passed their test" (comment to conjecture 107, dated "August, '90 - August '91. [BDF]") [1, p. 46]. | The test covered only graphs with at most 10 vertices, and there is no counterexample among them (`check_small.py`). |
| 2010 | Aouchiche, Hansen [3] | Survey of computer-generated conjectures in spectral graph theory. Its Table 6 lists 322 as open ("O") [3, p. 2318]. | It is a survey, not a search: Table 6 gives the status of the conjectures "according to the Written on the Wall file" [3, p. 2312]. |
| 2024 | Roucairol, Cazenave [4] | Searched for counterexamples to the conjectures of the survey [3] with eight search algorithms, on triangle-free graphs with up to 50 vertices for 322. 322 is still marked open in their Table 1. | They searched with the range read as the largest eigenvalue minus the smallest, under which 322 is trivially true. They had tried the glossary's range first, but with Even not counting the vertex itself the 4-cycle looked like a counterexample, and they took this as a sign that the definitions were wrong (Section 2). Whether their search would have found a counterexample under the glossary's definitions is not known. |
| 2026 | this repository | Repeated the test on all connected triangle-free graphs with at most 10 vertices (11569 graphs, exact arithmetic, `check_small.py`): no counterexample. The graph above, with 2048 vertices, is a counterexample. | — |

The smallest counterexample is not known: it has more than 10 vertices and at most 2048.

### 2. Why the 4-cycle is not a counterexample

Roucairol and Cazenave [4, Section 5.2] report that with the range read as the number of distinct values,
their programs refuted 322 with the cycle of length 4:
"the cycle of size 4 has 3 distinct distance eigenvalues and an Inverse Even of 4".

The value 4 does not agree with the glossary. Their code counts the vertices at even distance without the vertex
itself (the function `even_vec` skips it [5]), whereas the glossary counts "an even distance (including zero)" [2, p. 52].
With the glossary's definition:

- every vertex of the 4-cycle is at distance 0 from itself and at distance 2 from the opposite vertex, so Even = 2
  and Inverse Even = 4 · 1/2 = 2;
- the distance matrix has eigenvalues 4, 0, −2, −2, so the range is 3;
- 2 ≤ 3, so the inequality holds.

This agrees with the 1990–91 test, which passed 322 on all graphs with at most 10 vertices [1, p. 46],
and with `check_small.py`, which reports the 4-cycle as a violation only when Even(v) does not count v.

The authors themselves did not accept the 4-cycle as a refutation: "An error with the definitions seems more likely than
this conjecture being left open after dozens of articles with such a simple counter-example" [4, Section 5.2].
They took the range to be the largest eigenvalue minus the smallest instead ("The results featured in table 1
for Graffiti 322 use the usual definition of range" [4, Section 5.2]; in the code, the scope of the
distance eigenvalues [5]), and searched triangle-free graphs with up to 50 vertices [4, Table 1].
With that reading the inequality is trivially true (see Section 3), so no search could have found a counterexample.
So the search of 2024 was not a test of the conjecture as defined in the glossary.

### 3. The reading under which this is the first counterexample

The graph above is a counterexample when

- the **range** of a vector is the number of its distinct values, and
- **Even(v)** counts v itself (distance zero).

**Reasons for the range.**

- **The glossary** [2, p. 54] defines Range as "The number of distinct components"
  and Scope as "The difference between the largest and the smallest components".
- **The survey** [3, p. 2312], in the notation for its table of Graffiti's conjectures:
  "The range Rg(Vec) of the vector Vec is the number of its distinct entries. The scope Sp(Vec) is the difference
  between its maximum and minimum values". Its Table 6 writes conjecture 322 with Rg and conjecture 323 with Sp
  [3, p. 2318].
- ***Written on the Wall* uses "range" and "scope" for different quantities.**
  Conjectures 82 and 83 are the same statement with the two words exchanged:
  "range of coordinates of a maximal clique ≤ maximum of Even" and
  "scope of coordinates of a maximal clique ≤ maximum of Even" [1, p. 43].
  The comments say that 82 "is valid for all maximal cliques", while for 83 W. Staton "found a counterexample
  to the strongest version" [1, p. 43].
  Conjecture 323, next to 322, is about "the scope of positive eigenvalues" [1, p. 82].
- **Conjecture 578 separates the two meanings.**
  It reads "If G is a tree then the radius ≤ range of positive eigenvalues" [1, p. 99],
  and the survey lists it as proved ("P") [3, p. 2318].
  With the number of distinct values it is true. A tree of diameter d has at least d + 1 distinct eigenvalues
  (I, A, …, A^d are linearly independent, so the minimal polynomial of A has degree at least d + 1),
  the spectrum is symmetric about 0 because a tree is bipartite, so at least ⌈d/2⌉ of them are positive,
  and ⌈d/2⌉ is the radius of the tree.
  With the largest minus the smallest it is false for every star: the only positive eigenvalue is √k,
  so the difference is 0, while the radius is 1.
- **The other reading makes conjecture 322 trivial.**
  Suppose the range is the largest eigenvalue minus the smallest. For a connected graph with n ≥ 2 vertices,
  the largest eigenvalue of the distance matrix is at least n − 1 (Rayleigh quotient of the all-ones vector)
  and the smallest is at most −1 (Rayleigh quotient of e_i − e_j), so the range is at least n,
  while Inverse Even ≤ n. The inequality would hold for every connected graph,
  and the hypothesis "triangle-free" would play no role.

**Reasons for counting the vertex itself in Even.**

- **The glossary** [2, p. 52] says "(including zero)".
- **Conjecture 111 of *Written on the Wall*** [1, p. 47] reads "If G is triangle-free then [n/2] ≤ mean of Even",
  with the comments "Graffiti's original conjecture was that n/2 ≤ mean of Even. The modification is due to William
  Staton who observed that if n = 3 mod 4 then the cycles C_n are counterexamples" and
  "Since the conjecture is true for trees …".
  Counting v, an odd cycle C_n has mean of Even 1 + 2⌊(n − 1)/4⌋, which is less than n/2 exactly when n ≡ 3 (mod 4),
  and in a connected bipartite graph with parts of sizes a and b the mean of Even is (a² + b²)/n ≥ n/2,
  so the conjecture holds for trees. Not counting v, the original conjecture would also fail for the cycles with
  n ≡ 1 (mod 4), and the modified one would fail for a single edge (mean 0 < 1) and for the 4-cycle (mean 1 < 2).
- **The remark of J. B. Shearer** (July 1988) [1, p. 47] about the graph of this repository:
  "If G is a graph obtained from B₂₃ by identifying all points in cosets of the perfect Golay code then the mean of
  Even/n = 254/2048". Here 254 = 1 + 253 includes the vertex itself.
- *Written on the Wall* (conjecture 110: "Even(v) is the number of vertices at even distance from v" [1, p. 47])
  and the survey [3, p. 2319] do not say explicitly whether v is counted.

**Summary of the readings.**

| range | Even(v) counts v itself | conjecture 322 |
|---|---|---|
| number of distinct values (glossary) | yes (glossary) | false: the graph above. No counterexample with at most 10 vertices |
| number of distinct values | no | false already for the 4-cycle [4]. The graph above also violates it (2048/253 > 4) |
| largest minus smallest | yes or no | trivially true for n ≥ 2 |

**The claim.**
Under the glossary's definitions (first row of the table), the graph above is, to our knowledge,
the first reported counterexample to conjecture 322.
On 2026-10-07 we found no earlier counterexample in the literature or in the public records of current computer-assisted
work on these conjectures that we know of (for example, the ledger of AI Village [6] has no entry for this conjecture);
we cannot exclude unpublished work.
The claim depends on the reading: if Even(v) does not count v (second row), the 4-cycle came first.

**What is new.**
The graph itself is not new: *Written on the Wall* already mentions it, in the remark of Shearer quoted above,
which is about how small the mean of Even can be.
What is new is the observation that its distance matrix has only four distinct eigenvalues,
so that it violates conjecture 322.

## Verification

| script | method | requires |
|---|---|---|
| `verify_certificate.py` | reads only `data/edges.txt`; computes distances, the Even vector and Inverse Even exactly, and certifies the distance spectrum exactly (∏(D − rI) = 0 in integer arithmetic, multiplicities from tr(Dᵏ)) | Python 3, numpy |
| `verify_cayley.py` | builds the graph as a Cayley graph on F₂¹¹; checks triangle-freeness, the distances and the intersection array; computes the distance spectrum exactly with characters | Python 3 |
| `build_graph.py` | checks that g(x) generates a [23,12,7] code with the weight distribution of the Golay code, and regenerates `data/` from it (coset leaders of weight ≤ 3) | Python 3 |
| `check_small.py` | generates all connected triangle-free graphs with at most 10 vertices (11569 graphs up to isomorphism; the counts agree with OEIS A024607 [7]) and checks the inequality in exact arithmetic: no counterexample. Also shows that the 4-cycle is the first violation when Even(v) does not count v | Python 3 |

```
python verify_certificate.py
python verify_cayley.py
python check_small.py
```

## References

All quotations above were checked against the documents below on 2026-10-08.

- **[1]** S. Fajtlowicz, *Written on the Wall*, version of July 2004 (conjectures of the computer program Graffiti).
  The survey [3] gives its address as http://www.math.uh.edu/~clarson/.
  Copy used here (page numbers refer to it):
  [wow-july2004.pdf](https://github.com/RoucairolMilo/refutation-COCOON2022/blob/795ff6797ee3875cd36d715515099a48568a451a/wow-july2004.pdf),
  provided by the authors of [4].
- **[2]** T. L. Brewster, M. J. Dinneen, V. Faber, A computational attack on the conjectures of Graffiti:
  New counterexamples and proofs, *Discrete Mathematics* 147 (1995) 35–55.
  [doi:10.1016/0012-365X(94)00227-A](https://doi.org/10.1016/0012-365X(94)00227-A)
- **[3]** M. Aouchiche, P. Hansen, A survey of automated conjectures in spectral graph theory,
  *Linear Algebra and its Applications* 432 (2010) 2293–2322.
  [doi:10.1016/j.laa.2009.06.015](https://doi.org/10.1016/j.laa.2009.06.015)
- **[4]** M. Roucairol, T. Cazenave, Refutation of Spectral Graph Theory Conjectures with Search Algorithms,
  [arXiv:2409.18626](https://arxiv.org/abs/2409.18626) (2024). Quotations are from Section 5.2 of this version.
  A 2025 version (IASE 2025, [PDF on the second author's page](https://www.lamsade.dauphine.fr/~cazenave/papers/ConjectureRefutationECAI2025.pdf))
  has the same Section 5.2.
- **[5]** Source code of [4], linked from its 2025 version: [RoucairolMilo/refutationGBR](https://github.com/RoucairolMilo/refutationGBR), commit 66b9180.
  [`even_vec`](https://github.com/RoucairolMilo/refutationGBR/blob/66b9180cdb2e39f8cb988f09f94270f2b7f49fe5/src/models/conjectures/invariants.rs#L187-L203)
  (the vertex itself is skipped by `if vert != vert2`);
  [conjecture 322](https://github.com/RoucairolMilo/refutationGBR/blob/66b9180cdb2e39f8cb988f09f94270f2b7f49fe5/src/models/conjectures/GenerateGraph.rs#L1565-L1605)
  (`let rank_dist = scope;`, the count of distinct values is commented out).
- **[6]** AI Village, [graffiti-verification](https://gitlab.com/ai-village-agents/village/graffiti-verification),
  file `verify/ledger.tsv` at commit f2a1f1d (retrieved 2026-10-07).
- **[7]** OEIS, [A024607](https://oeis.org/A024607): Number of connected triangle-free graphs on n unlabeled nodes.

## License

Code: MIT (see `LICENSE`). Text and data: CC BY 4.0.
