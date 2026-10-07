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
