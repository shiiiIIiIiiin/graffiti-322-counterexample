# Graffiti 予想 322 の反例

[English](README.md)

木村心（Shin Kimura）、2026-10-07（2026-10-08 更新。[更新履歴](#更新履歴)を参照）

AI（Anthropic の Claude）の助けを借りて見つけた。

角括弧の番号は、末尾の[参考文献](#参考文献)を指す。[1] のページ番号は、そこに挙げた写しのページである。
引用は原文（英語）のまま載せ、必要に応じて訳を添える。

## 予想

S. Fajtlowicz『Written on the Wall』（2004 年 7 月版）の予想 322 [1, p. 82]：

> If G is a triangle-free graph then the Inverse Even ≤ range of eigenvalues of Distance.

（G が三角形を含まないグラフならば、Inverse Even ≤ 距離行列の固有値の range。）

用語は、T. L. Brewster, M. J. Dinneen, V. Faber の用語集 [2] の定義に従う。

- **Even ベクトル** [2, p. 52]："The vector whose ith component is the number of vertices an even distance (including zero) from vertex i."
  （第 i 成分は、頂点 i から偶数の距離（0 を含む）にある頂点の個数。）
- ベクトルの **Inverse** [2, p. 53]："The sum of the reciprocals of the nonzero components."（0 でない成分の逆数の和。）
- ベクトルの **Range** [2, p. 54]："The number of distinct components."（異なる成分の個数。）
  （**Scope** [2, p. 54] は "The difference between the largest and the smallest components."（最大の成分と最小の成分の差）。）

したがって、この予想の主張は次のとおり。三角形を含まないすべてのグラフについて、
Σ_v 1/Even(v) ≤（距離行列の異なる固有値の個数）。

## 反例

2 元 Golay 符号 [23,12,7] の剰余類グラフ
（2048 頂点、23-正則、三角形なし、交差配列 {23,22,21; 1,2,3} の距離正則グラフ）。

- 辺のリスト：[`data/edges.txt`](data/edges.txt)（頂点 0〜2047、辺 23552 本）
- 頂点のラベル：[`data/vertices.txt`](data/vertices.txt)（各頂点の剰余類の代表元）

| | 値 |
|---|---|
| 任意の頂点からの距離 | 距離 0 に 1 頂点、距離 1 に 23 頂点、距離 2 に 253 頂点、距離 3 に 1771 頂点 |
| Even(v) | すべての v で 1 + 253 = 254 |
| Inverse Even | 2048/254 = 1024/127 ≈ 8.063 |
| 距離行列のスペクトル | 5842¹, 10¹²⁸⁸, −14²⁵³, −30⁵⁰⁶（右上の数字は重複度） |
| 距離行列の固有値の range | 4 |

1024/127 > 4 なので、不等式は成り立たない。

構成：頂点は F₂[x]/(g(x)) の元とする。ここで
g(x) = x¹¹ + x¹⁰ + x⁶ + x⁵ + x⁴ + x² + 1。
ある i = 0, …, 22 について x^i mod g(x) だけ異なる 2 頂点を、辺で結ぶ。

この節に書いた性質は、すべて下のスクリプトで確かめている。`build_graph.py` は、g(x) が生成する符号の最小距離が 7 で、
重み分布が Golay 符号のものと一致することを確かめる。`verify_cayley.py` は、三角形がないこと、距離、交差配列、Even、
スペクトルを確かめる。

## より小さい反例

上の符号の座標を 1 つ削ると、Golay 符号を puncture した [22,12,6] 符号が得られる。その剰余類グラフ
（1024 頂点、22-正則、三角形なし、交差配列 {22,21,20; 1,2,6} の距離正則グラフ）も反例である。

- 辺のリスト：[`data/edges-1024.txt`](data/edges-1024.txt)（頂点 0〜1023、辺 11264 本）
- 頂点のラベル：[`data/vertices-1024.txt`](data/vertices-1024.txt)（各頂点の F₂[x]/(g(x)) での代表元）

| | 値 |
|---|---|
| 任意の頂点からの距離 | 距離 0 に 1 頂点、距離 1 に 22 頂点、距離 2 に 231 頂点、距離 3 に 770 頂点 |
| Even(v) | すべての v で 1 + 231 = 232 |
| Inverse Even | 1024/232 = 128/29 ≈ 4.414 |
| 距離行列のスペクトル | 2794¹, 10⁶¹⁶, −22⁴⁰⁷ |
| 距離行列の固有値の range | 3 |

128/29 > 3 なので、不等式は成り立たない。直径は 3 だが、距離行列の異なる固有値は 3 個しかない。

構成：上のグラフの各頂点 a を a + (x²² mod g(x)) と同一視する。これで頂点は 1024 個になり、
ある i = 0, …, 21 について x^i mod g(x) だけ異なる 2 頂点を、辺で結ぶ。

さらに座標を 1 つ削っても反例にはならない。[21,12,5] 符号の剰余類グラフ（512 頂点）は
Inverse Even = 512/211 ≈ 2.43 で、距離行列の異なる固有値は 4 個である。

この節に書いた性質は、すべて `check_quotients.py` で確かめている。辺のリストは
`verify_certificate.py data/edges-1024.txt` で確かめている。

## 定義と先行研究についての補足

この節で言いたいことは 3 つある。

1. 予想 322 は、誰も調べていなかったから未解決だったわけではない。
2. 2024 年にある読み方のもとで反例として報告された長さ 4 の閉路は、用語集 [2] の定義では反例ではない。
3. 用語集 [2] の定義のもとでは、2048 頂点のグラフは、私たちの知る限り最初に報告された反例である。
   そして、この予想をその定義で読むべき理由がある。

### 1. この予想は放置されていたわけではない

計算機で検証され、未解決として挙げられ、2024 年には探索の対象にもなった。
ただし、どれにも限界があり、それが反例を見つけられなかった理由になっている。

| 年 | 誰が | 何をしたか | 反例を見つけられなかった理由 |
|---|---|---|---|
| 1990〜91 | Brewster, Dinneen, Faber [2] | "all the nonisomorphic graphs with 10 or fewer vertices"（10 頂点以下の非同型なグラフすべて）で "approximately 200 of the Graffiti conjectures"（約 200 個の予想）を検証し、"counterexamples for over 40 of them"（40 個以上に反例）を見つけた [2, p. 35]。『Written on the Wall』は、"the conjectures which passed their test"（検証を通過した予想）の 1 つとして 322 を挙げている（予想 107 へのコメント。日付は "August, '90 - August '91. [BDF]"）[1, p. 46]。 | 検証したのは 10 頂点以下のグラフだけで、その中に反例はない（`check_small.py`）。 |
| 2010 | Aouchiche, Hansen [3] | 計算機が生成したスペクトルグラフ理論の予想のサーベイ。表 6 で 322 を未解決（"O"）としている [3, p. 2318]。 | 探索ではなくサーベイである。表 6 の状態は "according to the Written on the Wall file"（『Written on the Wall』に従って）書かれている [3, p. 2312]。 |
| 2024 | Roucairol, Cazenave [4] | サーベイ [3] の予想の反例を 8 種類の探索アルゴリズムで探した。322 については、50 頂点までの三角形を含まないグラフを探索した。322 は同論文の表 1 で未解決のまま残っている。 | range を「最大固有値 − 最小固有値」と読んで探索した。この読み方では 322 は自明に成り立つ。最初は用語集どおりの range で計算したが、Even に頂点自身を数えていなかったため長さ 4 の閉路が反例に見え、定義が違うのだろうと判断した（2 を参照）。用語集の定義で探索していたら反例が見つかったかどうかは分からない。 |
| 2026 | このリポジトリ | 10 頂点以下の、三角形を含まない連結グラフすべて（11569 個）で検証をやり直した（厳密な計算、`check_small.py`）。反例はなかった。一方、上の 2048 頂点と 1024 頂点のグラフは反例である。 | — |

最小の反例は分かっていない。頂点数は 10 より大きく、1024 以下である。

### 2. 長さ 4 の閉路が反例ではない理由

Roucairol と Cazenave [4, 5.2 節] は、range を「異なる値の個数」と読むと、プログラムが長さ 4 の閉路で 322 を反証したと報告している：
"the cycle of size 4 has 3 distinct distance eigenvalues and an Inverse Even of 4"
（長さ 4 の閉路は、距離行列の異なる固有値が 3 個で、Inverse Even が 4 である）。

この 4 という値は用語集と合わない。同論文のコードは、偶数距離にある頂点を数えるときに頂点自身を数えていない
（関数 `even_vec` が頂点自身を飛ばしている [5]）。一方、用語集は "an even distance (including zero)"（0 を含む偶数の距離）
で数える [2, p. 52]。用語集の定義では次のとおりである。

- 長さ 4 の閉路のどの頂点も、自分自身から距離 0、向かいの頂点から距離 2 にあるので、Even = 2、
  Inverse Even = 4 · 1/2 = 2。
- 距離行列の固有値は 4, 0, −2, −2 なので、range は 3。
- 2 ≤ 3 なので、不等式は成り立つ。

これは、10 頂点以下のすべてのグラフで 322 が通過した 1990〜91 年の検証 [1, p. 46] とも、
Even(v) が v 自身を数えない場合にだけ長さ 4 の閉路を違反として表示する `check_small.py` とも合う。

著者たち自身も、長さ 4 の閉路を反証とは認めなかった：
"An error with the definitions seems more likely than this conjecture being left open after dozens of articles with
such a simple counter-example"（これほど単純な反例があるのに、何十本もの論文のあとでこの予想が未解決のまま残っているとは
考えにくく、定義に誤りがある可能性のほうが高い）[4, 5.2 節]。
代わりに range を「最大固有値 − 最小固有値」とし（"The results featured in table 1 for Graffiti 322 use the usual
definition of range" [4, 5.2 節]。コードでは距離固有値の最大と最小の差 [5]）、
50 頂点までの三角形を含まないグラフを探索した [4, 表 1]。
この読み方では不等式は自明に成り立つ（3 を参照）ので、どれだけ探索しても反例は見つからない。
したがって、2024 年の探索は、用語集の定義での予想を調べたことにはならない。

### 3. 上のグラフが最初の反例になる読み方

上の 2 つのグラフが反例になるのは、次のように読んだときである。

- ベクトルの **range** は、異なる値の個数である。
- **Even(v)** は、v 自身（距離 0）を数える。

**range をこう読む理由.**

- **用語集** [2, p. 54] は、Range を "The number of distinct components"（異なる成分の個数）、
  Scope を "The difference between the largest and the smallest components"（最大の成分と最小の成分の差）と定義している。
- **サーベイ** [3, p. 2312] は、Graffiti の予想の表のための記法として、
  "The range Rg(Vec) of the vector Vec is the number of its distinct entries. The scope Sp(Vec) is the difference
  between its maximum and minimum values"（range は異なる成分の個数、scope は最大値と最小値の差）と書いている。
  表 6 では、予想 322 を Rg で、予想 323 を Sp で書いている [3, p. 2318]。
- **『Written on the Wall』は range と scope を別の量として使っている.**
  予想 82 と 83 は、この 2 語を入れ替えただけの同じ文である：
  "range of coordinates of a maximal clique ≤ maximum of Even" と
  "scope of coordinates of a maximal clique ≤ maximum of Even" [1, p. 43]。
  コメントによれば、82 は "is valid for all maximal cliques"（すべての極大クリークについて成り立つ）が、
  83 については W. Staton が "found a counterexample to the strongest version"（最も強い形への反例を見つけた）[1, p. 43]。
  322 のすぐ次の予想 323 は "the scope of positive eigenvalues" についての予想である [1, p. 82]。
- **予想 578 で 2 つの意味を区別できる.**
  予想 578 は "If G is a tree then the radius ≤ range of positive eigenvalues"（木ならば、半径 ≤ 正の固有値の range）であり [1, p. 99]、
  サーベイはこれを証明済み（"P"）としている [3, p. 2318]。
  range が異なる値の個数なら、これは正しい。直径 d の木は少なくとも d + 1 個の異なる固有値をもつ
  （I, A, …, A^d は線形独立なので、A の最小多項式の次数は d + 1 以上）。木は 2 部グラフなので固有値は 0 について対称であり、
  異なる正の固有値は少なくとも ⌈d/2⌉ 個ある。そして ⌈d/2⌉ は木の半径である。
  range が最大 − 最小なら、すべての星で成り立たない。星 K₁,ₖ の正の固有値は √k だけなので差は 0 だが、半径は 1 である。
- **もう一方の読み方では、予想 322 が自明になる.**
  range を「最大固有値 − 最小固有値」とする。頂点数 n ≥ 2 の連結グラフでは、
  距離行列の最大固有値は n − 1 以上（全成分 1 のベクトルのレイリー商）、最小固有値は −1 以下（e_i − e_j のレイリー商）なので、
  range は n 以上である。一方、Inverse Even ≤ n である。
  つまり、不等式はすべての連結グラフで成り立ち、「三角形を含まない」という仮定は何の役割も果たさない。

**Even が頂点自身を数えると読む理由.**

- **用語集** [2, p. 52] に "(including zero)"（0 を含む）とある。
- **『Written on the Wall』の予想 111** [1, p. 47] は "If G is triangle-free then [n/2] ≤ mean of Even" であり、
  コメントに "Graffiti's original conjecture was that n/2 ≤ mean of Even. The modification is due to William Staton
  who observed that if n = 3 mod 4 then the cycles C_n are counterexamples"
  （元の予想は n/2 ≤ Even の平均だった。n ≡ 3 (mod 4) の閉路 C_n が反例になることを Staton が指摘し、修正された）と、
  "Since the conjecture is true for trees …"（この予想は木では正しいので…）とある。
  v 自身を数えると、奇数長の閉路 C_n の Even の平均は 1 + 2⌊(n − 1)/4⌋ で、これが n/2 より小さくなるのはちょうど n ≡ 3 (mod 4) のときである。
  また、大きさ a と b の 2 つの部分をもつ連結な 2 部グラフでは Even の平均は (a² + b²)/n ≥ n/2 なので、木では予想が成り立つ。
  v 自身を数えないと、元の予想は n ≡ 1 (mod 4) の閉路でも成り立たず、修正後の予想も辺 1 本のグラフ（平均 0 < 1）や
  長さ 4 の閉路（平均 1 < 2）で成り立たない。コメントと合わない。
- **J. B. Shearer のコメント**（1988 年 7 月）[1, p. 47] は、このリポジトリのグラフについてのものである：
  "If G is a graph obtained from B₂₃ by identifying all points in cosets of the perfect Golay code then the mean of
  Even/n = 254/2048"。この 254 = 1 + 253 は頂点自身を含む。
- なお、『Written on the Wall』（予想 110："Even(v) is the number of vertices at even distance from v" [1, p. 47]）と
  サーベイ [3, p. 2319] は、v 自身を数えるかどうかを明記していない。

**読み方ごとのまとめ.**

| range | Even(v) が v 自身を数えるか | 予想 322 |
|---|---|---|
| 異なる値の個数（用語集） | 数える（用語集） | 偽：上の 2 つのグラフ。10 頂点以下に反例はない |
| 異なる値の個数 | 数えない | 長さ 4 の閉路ですでに偽 [4]。上の 2 つのグラフでも成り立たない（2048/253 > 4、1024/231 > 3） |
| 最大 − 最小 | どちらでも | n ≥ 2 で自明に真 |

**主張.**
用語集の定義（表の 1 行目）のもとで、2048 頂点のグラフは、私たちの知る限り、予想 322 の最初に報告された反例である。
2026-10-07 の時点で、文献にも、私たちの知る範囲の、計算機を使った現在進行中の検証の公開記録
（例えば AI Village の記録 [6] には、この予想の項目がない）にも、これより前の反例は見つからなかった。
未公表の結果がある可能性は否定できない。
この主張は読み方に依存する。Even(v) が v 自身を数えない場合（表の 2 行目）は、長さ 4 の閉路のほうが先である。

**新しい点.**
このグラフ自体は新しいものではない。『Written on the Wall』には、上に引用した Shearer のコメント
（Even の平均がどこまで小さくなるかについてのもの）として、すでにこのグラフが登場する。
新しいのは、このグラフの距離行列の異なる固有値が 4 個しかなく、そのため予想 322 が成り立たない、という観察である。
1024 頂点のグラフ（距離行列の異なる固有値は 3 個）についても同じである。

## 検証

| スクリプト | 方法 | 必要なもの |
|---|---|---|
| `verify_certificate.py` | `data/edges.txt`（または引数で渡した辺のリスト。例えば `data/edges-1024.txt`）だけを読み、距離、Even ベクトル、Inverse Even を厳密に計算する。距離行列のスペクトルも厳密に確かめる（整数演算で ∏(D − rI) = 0 を確認し、重複度は tr(Dᵏ) から求める） | Python 3、numpy |
| `verify_cayley.py` | グラフを F₂¹¹ 上のケーリーグラフとして作り、三角形がないこと、距離、交差配列を確かめ、指標を使って距離行列のスペクトルを厳密に計算する | Python 3 |
| `build_graph.py` | g(x) が Golay 符号の重み分布をもつ [23,12,7] 符号を生成することを確かめ、そこから `data/edges.txt` と `data/vertices.txt` を作り直す（重み 3 以下の剰余類代表元） | Python 3 |
| `check_quotients.py` | 座標を 0・1・2 個削った符号の剰余類グラフ（2048・1024・512 頂点）をケーリーグラフとして作り、三角形がないこと、距離、交差配列を確かめ、指標を使って距離行列のスペクトルを厳密に計算する。`--write-data` を付けると `data/edges-1024.txt` と `data/vertices-1024.txt` を作り直す | Python 3 |
| `check_small.py` | 10 頂点以下の、三角形を含まない連結グラフをすべて生成し（同型を除いて 11569 個。個数は OEIS A024607 [7] と一致）、不等式を厳密な計算で確かめる。反例なし。Even(v) が v 自身を数えない場合に、長さ 4 の閉路が最初の違反になることも表示する | Python 3 |

```
python verify_certificate.py
python verify_certificate.py data/edges-1024.txt
python verify_cayley.py
python check_quotients.py
python check_small.py
```

## 参考文献

上の引用はすべて、2026-10-08 に以下の文献の原文と照合した。

- **[1]** S. Fajtlowicz, *Written on the Wall*, version of July 2004（計算機プログラム Graffiti の予想集）.
  サーベイ [3] は所在を http://www.math.uh.edu/~clarson/ としている。
  ここで使った写し（ページ番号はこれによる）：
  [wow-july2004.pdf](https://github.com/RoucairolMilo/refutation-COCOON2022/blob/795ff6797ee3875cd36d715515099a48568a451a/wow-july2004.pdf)
  （[4] の著者が公開しているもの）。
- **[2]** T. L. Brewster, M. J. Dinneen, V. Faber, A computational attack on the conjectures of Graffiti:
  New counterexamples and proofs, *Discrete Mathematics* 147 (1995) 35–55.
  [doi:10.1016/0012-365X(94)00227-A](https://doi.org/10.1016/0012-365X(94)00227-A)
- **[3]** M. Aouchiche, P. Hansen, A survey of automated conjectures in spectral graph theory,
  *Linear Algebra and its Applications* 432 (2010) 2293–2322.
  [doi:10.1016/j.laa.2009.06.015](https://doi.org/10.1016/j.laa.2009.06.015)
- **[4]** M. Roucairol, T. Cazenave, Refutation of Spectral Graph Theory Conjectures with Search Algorithms,
  [arXiv:2409.18626](https://arxiv.org/abs/2409.18626) (2024). 引用はこの版の 5.2 節から。
  2025 年版（IASE 2025、[第 2 著者のページの PDF](https://www.lamsade.dauphine.fr/~cazenave/papers/ConjectureRefutationECAI2025.pdf)）にも同じ 5.2 節がある。
- **[5]** [4] のソースコード（2025 年版からリンクされている）：[RoucairolMilo/refutationGBR](https://github.com/RoucairolMilo/refutationGBR)、コミット 66b9180。
  [`even_vec`](https://github.com/RoucairolMilo/refutationGBR/blob/66b9180cdb2e39f8cb988f09f94270f2b7f49fe5/src/models/conjectures/invariants.rs#L187-L203)
  （`if vert != vert2` で頂点自身を飛ばしている）、
  [予想 322](https://github.com/RoucairolMilo/refutationGBR/blob/66b9180cdb2e39f8cb988f09f94270f2b7f49fe5/src/models/conjectures/GenerateGraph.rs#L1565-L1605)
  （`let rank_dist = scope;`。異なる値の個数を数える行はコメントアウトされている）。
- **[6]** AI Village, [graffiti-verification](https://gitlab.com/ai-village-agents/village/graffiti-verification)、
  ファイル `verify/ledger.tsv`、コミット f2a1f1d（2026-10-07 取得）。
- **[7]** OEIS, [A024607](https://oeis.org/A024607): Number of connected triangle-free graphs on n unlabeled nodes.

## 更新履歴

- 2026-10-07：2048 頂点の反例（[23,12,7] Golay 符号の剰余類グラフ）を公開した。
  AI（Anthropic の Claude）の助けを借りて見つけた。
- 2026-10-08：定義と先行研究についての補足と、10 頂点以下のすべてのグラフでの検証を追加した。
- 2026-10-08：座標を 1 つ削った [22,12,6] 符号の剰余類グラフ（1024 頂点）も反例であることに著者が気付き、
  Claude で計算して確かめた（`check_quotients.py`、`verify_certificate.py data/edges-1024.txt`）。
  これにより、最小の反例は 1024 頂点以下となる。

## ライセンス

コード：MIT（`LICENSE` を参照）。文章とデータ：CC BY 4.0。
