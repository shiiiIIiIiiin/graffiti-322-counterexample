# Graffiti 予想 322 の反例

[English](README.md)

木村心（Shin Kimura）、2026-10-07

AI（Anthropic の Claude）の助けを借りて見つけた。

## 予想

S. Fajtlowicz『Written on the Wall』（2004 年 7 月版）の予想 322：

> G が三角形を含まないグラフならば、Inverse Even ≤ 距離行列の固有値の range。

用語は、T. L. Brewster, M. J. Dinneen, V. Faber,
"A computational attack on the conjectures of Graffiti: New counterexamples and proofs",
Discrete Math. 147 (1995) 35–55 の用語集の定義に従う。

- **Even ベクトル**（p. 52）：第 i 成分は、頂点 i から偶数の距離（0 を含む）にある頂点の個数。
- ベクトルの **Inverse**（p. 53）：0 でない成分の逆数の和。
- ベクトルの **Range**（p. 54）：異なる成分の個数。
  （最大の成分と最小の成分の差は **scope** と呼ばれる。）

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

## 定義と先行研究についての補足

**「range」を「異なる値の個数」と読む理由.**

- Brewster, Dinneen, Faber の用語集（p. 54）は、ベクトルの range を「異なる成分の個数」と定義し、
  それとは別に scope を「最大の成分と最小の成分の差」と定義している。
  この著者たちは 1990〜91 年に Graffiti の予想を計算機で検証しており、『Written on the Wall』（予想 107 へのコメント）は、
  10 頂点以下のすべてのグラフでの検証を通過した予想の 1 つとして 322 を挙げている。
- 『Written on the Wall』は 2 つの語を使い分けている。すぐ次の予想 323 は「the scope of positive eigenvalues」についての予想である。
- Aouchiche と Hansen のサーベイ（2010）も、range を異なる値の個数としている
  （下に挙げる Roucairol と Cazenave の論文の 5.2 節による）。
- 「range」を「最大固有値 − 最小固有値」と読むと、この不等式は自明になる。頂点数 n ≥ 2 の連結グラフでは、
  距離行列の最大固有値は n − 1 以上（全成分 1 のベクトルのレイリー商）、最小固有値は −1 以下（e_i − e_j のレイリー商）なので、
  その差は n 以上である。一方、Even(v) ≥ 1 なので Inverse Even ≤ n である。

したがって、予想 322 はどちらの読み方でも決着している。用語集の定義では偽（上のグラフ）であり、
もう一方の読み方では自明に真である。

**長さ 4 の閉路は反例ではない.**
M. Roucairol and T. Cazenave, *Refutation of Spectral Graph Theory Conjectures with Search Algorithms*
（[arXiv:2409.18626](https://arxiv.org/abs/2409.18626)、ECAI 2025）の 5.2 節は、「異なる値の個数」という読み方では、
長さ 4 の閉路で 322 が反証されると報告している（「長さ 4 の閉路は、距離行列の異なる固有値が 3 個で、Inverse Even が 4 である」）。
著者たちは定義の誤りを疑い（「これほど単純な反例があるのに、何十本もの論文のあとでこの予想が未解決のまま残っているとは考えにくく、
定義に誤りがある可能性のほうが高い」）、代わりに「最大固有値 − 最小固有値」で探索して、
50 頂点までの三角形を含まないグラフで反例を見つけなかった（同論文の表 1。322 は未解決とされている）。
この計算では、偶数距離にある頂点を数えるときに、その頂点自身を数えていない。Inverse Even = 4 はここから出てくる
（[コード](https://github.com/RoucairolMilo/refutationGBR/blob/main/src/models/conjectures/invariants.rs)）。
上の定義（距離 0 を含む）では、長さ 4 の閉路のどの頂点でも Even = 2 なので Inverse Even = 2、
距離行列の固有値は 4, 0, −2, −2 なので range は 3 である。不等式 2 ≤ 3 は成り立つ。
これは、10 頂点以下のすべてのグラフを調べた 1990〜91 年の検証とも合う。

**Even がその頂点自身を数える理由.**
用語集には「偶数の距離（0 を含む）」と書かれている。『Written on the Wall』もこれと合う。下に引用する Shearer のコメントは、
このリポジトリのグラフの Even を 253 ではなく 254 = 1 + 253 としている。

**読み方ごとのまとめ.**

| range | Even(v) が v 自身を数えるか | 予想 322 |
|---|---|---|
| 異なる値の個数（用語集） | 数える（用語集） | 偽：上のグラフ。10 頂点以下のすべてのグラフでは真（1990〜91 年の検証） |
| 異なる値の個数 | 数えない | 長さ 4 の閉路ですでに偽（Roucairol と Cazenave）。上のグラフでも成り立たない（2048/253 > 4） |
| 最大 − 最小 | どちらでも | n ≥ 2 で自明に真 |

**新規性.**
私たちの知る限り、上のグラフは、用語集の定義（表の 1 行目）のもとでの予想 322 の最初の反例である。
この予想は、Aouchiche と Hansen のサーベイ（2010）に従って、Roucairol と Cazenave の論文（2024）で未解決とされていた。
2026-10-07 の時点で、文献にも、私たちの知る範囲の、計算機を使った現在進行中の検証の公開記録にも、
これより前の反例は見つからなかった。未公表の結果がある可能性は否定できない。
1990〜91 年の検証により、反例の頂点数は 10 より大きい。最小の反例は分かっていない。

このグラフ自体は新しいものではない。『Written on the Wall』には、Even の平均がどこまで小さくなるかについての
J. B. Shearer のコメント（1988 年 7 月）として、すでにこのグラフが登場する（"the mean of Even/n = 254/2048"）。

この節の文献：
M. Aouchiche, P. Hansen, *A survey of automated conjectures in spectral graph theory*, Linear Algebra Appl. 432 (2010) 2293–2322；
M. Roucairol, T. Cazenave, arXiv:2409.18626.

## 検証

| スクリプト | 方法 | 必要なもの |
|---|---|---|
| `verify_certificate.py` | `data/edges.txt` だけを読み、距離、Even ベクトル、Inverse Even を厳密に計算する。距離行列のスペクトルも厳密に確かめる（整数演算で ∏(D − rI) = 0 を確認し、重複度は tr(Dᵏ) から求める） | Python 3、numpy |
| `verify_cayley.py` | グラフを F₂¹¹ 上のケーリーグラフとして作り、指標を使って距離行列のスペクトルを厳密に計算する | Python 3 |
| `build_graph.py` | Golay 符号（重み 3 以下の剰余類代表元）から `data/` を作り直す | Python 3 |

```
python verify_certificate.py
python verify_cayley.py
```

## ライセンス

コード：MIT（`LICENSE` を参照）。文章とデータ：CC BY 4.0。
