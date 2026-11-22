# Mathar's recurrence in OEIS A174193

Haobo Ma (ChronoAI Pte Ltd, Singapore), followed by Wenlin Zhang (National University of Singapore; ChronoAI Pte Ltd, Singapore). 4 November 2026. CC BY 4.0.

The note extends Brignall, Ekhad, Smith and Vatter (2009) by proving the order-four recurrence in OEIS A174193, FORMULA, 14 June 2016, and evaluating their tableau sum for almost-321-avoiding permutations, identifying the specified algebraic series with their actual counting function. The same method proves the A174195 recurrence for indices at least four, first-order relations, the exact count difference, common asymptotics and relative gap 1/(2n). Nonzero A174195 recurrence residuals at n=2,3 show n >= 4 is the exact range among integers n >= 2. As a consequence of the count inequality, equal lexicographic ranks give a length-preserving injection. Problem 10 is not covered: this cardinality-induced injection does not supply its sought combinatorial explanation. Conjecture 11 is proved for t=1; t=0 is the classical Catalan case, and t >= 2 is not covered.

## Build

Use Tectonic 0.17.0:

```sh
tectonic --untrusted note.tex
```

Alternatively, use a standard LaTeX distribution with the packages listed in `note.tex`:

```sh
pdflatex -no-shell-escape note.tex
pdflatex -no-shell-escape note.tex
```

The bibliography is included in the main source, so BibTeX is unnecessary. No external figures or TeX input files are required.

## Exact arithmetic

Python 3.9 or newer, standard library only:

```sh
python3 verify.py > verification.json
```

Expected status: `all_checks_passed`. Nine exact polynomial identities support the written proofs: two cleared recurrence identities, the sum of recurrence weights, two generating-function decompositions, the coefficient difference, the bivariate weighted-sum expansion, its rational Vandermonde evaluation and the tableau closed-form simplification. Independently generated coefficients test each closed form through index 200, each original recurrence from 4 through 200, the A174193 first-order relation through index 199, the A174195 first-order relation from 2 through 199, the coefficient difference from 2 through 200 and all 30 displayed terms of each OEIS entry. The tableau sum is compared at all 201 indices. Deletion enumeration through length 8 independently counts both permutation classes and checks the rank-injection images. The checker also records the nonzero A174195 recurrence residuals at indices 2 and 3.

## Formal scope

At revision `0b9787cf2582188d0ab3da380adab3fa26bea39c`, the declaration `D5.S1.Recurrence.Algebraic.MatharA174193OrderFourRecurrence.result` in the pinned source below proves existence of the algebraic series and the universal A174193 recurrence for natural indices at least four:

https://github.com/the-omega-institute/trureturing/blob/0b9787cf2582188d0ab3da380adab3fa26bea39c/D5/S1/Recurrence/Algebraic/MatharA174193OrderFourRecurrence.lean

Its Euler-coefficient dependency is:

https://github.com/the-omega-institute/trureturing/blob/0b9787cf2582188d0ab3da380adab3fa26bea39c/D5/S1/Recurrence/A308815DFiniteRecurrence.lean

The imported declaration `D5.S1.Recurrence.A308815DFiniteRecurrence.euler_coeff` states `[x^d](x f') = d[x^d]f` for rational formal series and natural d. The closed forms, first-order relations, tableau-sum evaluation and counting identification, A174195 recurrence, count comparison, asymptotics, rank injection and t=0,1 consequences are written mathematical proofs in the note. They are outside the main Lean declaration's statement. The finite comparisons in `verification.json` have the stated finite bounds.

## Sources and license

The exact posing locators are https://oeis.org/A174193 and https://oeis.org/A174195, FORMULA entries signed R. J. Mathar, 14 June 2016. Context: Brignall, Ekhad, Smith and Vatter, *Almost avoiding permutations*, Discrete Mathematics 309 (2009), 6626–6631, doi:10.1016/j.disc.2009.06.027; https://arxiv.org/abs/2007.15111v1. Their Proposition 3 and Section 2 supply the tableau sum, Theorem 9 proves the A174195 generating function, Problem 10 seeks a combinatorial explanation by an injection, and Conjecture 11 asks about all t. The 2020 arXiv deposit is the 2009 work, not a later independent proof. The bibliography also identifies Stanley's D-finite theorem and Mathar's general recurrence method.

The note, checker and accompanying descriptive material are licensed CC BY 4.0: https://creativecommons.org/licenses/by/4.0/. Referenced third-party sources retain their respective licenses.
