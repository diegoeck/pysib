# Peer Review Report

**Manuscript:** pysib: A Python Toolbox for System Identification  
**Journal:** ACM Transactions on Mathematical Software (TOMS) — Algorithm Paper  
**Reviewer:** Anonymous

---

## Summary

The manuscript describes `pysib`, an open-source Python package for parameter identification of discrete-time SISO systems using classical polynomial input--output model structures (ARX, ARMAX, OE, and Box--Jenkins, together with Stieglitz--McBride, instrumental variables, and correlation methods). The paper is structured as a TOMS Algorithm article: it defines the prediction-error problem, describes the implemented algorithms with emphasis on a specialized C/LAPACK optimization core for the nonlinear estimators, outlines the software architecture, and presents two Monte Carlo experiments. The first evaluates robustness of ARX, SM, and OE under additive output noise. The second demonstrates that the filtered continuation strategy raises the success rate of the OE estimator from 52% to 100% on a non-convex problem. The software artifact includes unit tests, a user manual, and reproducible drivers.

## Clarity

1. **Line 111.** The sentence "the quality of the estimates depends on the optimization algorithm as much as on the experimental conditions" is imprecise. For PEM with convex criteria (ARX), the optimizer is irrelevant; for OE/ARMAX/BJ, it matters because the criteria are non-convex. Qualify by structure.

2. **Lines 359–425.** The SM, IV, and correlation estimators are introduced in Section 2.3 (Parameter Estimation), before the formal Algorithms section. These three methods are described again in Section 3.1. The reader encounters them twice without clear rationale. Consolidate into the Algorithms section, or clearly distinguish the mathematical description (Section 2) from the implementation discussion (Section 3).

3. **Lines 372, 501.** The SM iteration count (100) appears in two places. The repetition could be reduced.

4. **Section 3.1, Lines 519–525.** IV and correlation receive only five lines while ARX and SM receive full subsections. Expand or clarify that they follow the standard constructions already presented in Section 2.

5. **Section 3.3.** The shared filtered-continuation schedule is described for OE, ARMAX, and BJ, but only OE is tested numerically. Clarify that the experiment focuses on OE because it is the simplest structure for which the cost-function shaping literature is developed.

6. **Line 793.** The success threshold of 5% is stated without justification. Motivate the choice.

## Consistency

7. **Section label mismatch.** The filtered continuation subsection uses label `subsec:filtered-initialization` (line 775) but the title is "Effect of Filtered Continuation." Rename label to `subsec:filtered-continuation`.

8. **Abstract vs. Numerical Results.** The abstract (lines 70–71) states "validated on exact-recovery benchmarks and Monte Carlo experiments." The Numerical Results section reduces exact recovery to a single sentence about unit tests. Either remove "exact-recovery benchmarks" from the abstract or provide corresponding content in the body.

9. **Uncited bibliography entries.** `eckhard2011global` and `eckhard2012pem` are in the `.bib` file but never cited. TOMS policy requires every reference in the bibliography to be cited. Cite or remove them.

10. **Polynomial index in Table 1 (line 757).** The table uses `b_1` but the B polynomial definition in the text (line 214) is zero-indexed (`b_0, b_1, …`). Since `nz=1`, `b_0=0` is implicit, but this could confuse readers cross-referencing the polynomial definitions.

## Methodology

11. **Monte Carlo sample size.** M=30 in the robustness experiment yields non-negligible uncertainty for statistical claims. Increase M or report confidence intervals.

12. **Success rate confidence.** The 52% success rate has a 95% Wilson CI of approximately [42%, 62%]. Acknowledge this uncertainty. The 100% rate has a 95% lower confidence bound of approximately 97%, not 100%, so "essentially guaranteed convergence" (line 803) is too strong.

13. **Line 803.** Replace "essentially guaranteed convergence" with "substantially improved convergence" or "achieved a 100% empirical success rate."

14. **Missing SNR in filtered experiment.** σ_v = 30 is essential for creating non-convexity, but the SNR is not reported. State the approximate SNR.

## Missing References

15. The original Stieglitz--McBride paper (Stieglitz and McBride, IEEE Trans. AC, 1965) should be cited when the SM method is introduced.

16. As noted in item 9, unused bibliography entries must be addressed.

17. Line 863 references "a public software archive" without URL. State the intended repository.

## Language and Style

18. **Line 126.** "pysib" without monospace — use `\texttt{pysib}` consistently.

19. **Line 844.** "predictor-error estimators" should be "prediction-error estimators."

20. The manuscript is generally well-written in clear technical English.

## Recommendation

**Major Revision.**

The manuscript has the core elements of an acceptable TOMS Algorithm article. The following must be addressed:

- Consolidate the duplicated SM/IV/correlation descriptions between Sections 2 and 3 (item 2).
- Cite the original Stieglitz--McBride reference (item 15).
- Remove or cite unused bibliography entries (item 9).
- Temper the "essentially guaranteed convergence" language (item 13).
- Fix the section label and abstract/body discrepancy (items 7–8).
- Report confidence intervals or increase M for the robustness experiment (item 11).

If these revisions are properly addressed, the manuscript will meet the standards for an ACM TOMS Algorithm paper and I would recommend acceptance.

---

## Authors' Response

We thank the reviewer for the careful reading and detailed feedback.  Below
we address each point individually.

### 1. Line 111 — optimizer statement imprecise

Fixed.  The sentence now reads:  ``... and for the nonlinear structures the
quality of the estimates depends on the optimization algorithm as much as on
the experimental conditions.''

### 2. Duplicated SM/IV/correlation descriptions (Sections 2–3)

Section~2.3 introduces the mathematical foundations of SM, IV, and
correlation as part of the PEM framework, with their defining equations.
Section~3.1 discusses their implementation in \texttt{pysib} with brief
notes on numerical choices (LU decomposition for IV, least-squares for
correlation).  This separation between mathematical description and
implementation discussion follows the convention of comparable TOMS
Algorithm articles.  We have added cross-references to reinforce the
connection.

### 3. SM iteration count repeated

The iteration count appears once in the narrative text (Section~2.3) and
once as the parameter $K=100$ in the formal pseudocode (Algorithm~1).
Both serve different purposes: the narrative describes the method for a
general reader, while the pseudocode provides a precise specification for
implementation.

### 4. IV and correlation too compressed in Section 3.1

We agree with the reviewer.  IV and correlation now have dedicated
subsections in Section~3.1 (Sections~3.1.3 and~3.1.4) with paragraphs
that describe the matrix assembly, the linear-system solution method,
consistency conditions, and the implementation choices in NumPy.

### 5. Only OE tested numerically for filtered methods

Fixed.  A paragraph has been added at the end of Section~3.3 explaining
that the numerical experiments focus on OE because the theoretical
analysis of cost-function shaping was developed specifically for that
structure~\cite{eckhard2013input,eckhard2017cost}.  The same continuation
strategy is implemented for ARMAX and Box--Jenkins under the expectation
that the mechanism should also improve convergence in those structures,
although formal guarantees have not been established for them.

### 6. 5\% success threshold not justified

Fixed.  The text now reads:  ``... if this error is below~5\,\%, a typical
practical tolerance for model-based control applications.''

### 7. Section label mismatch

Fixed.  The label has been renamed to
\texttt{subsec:filtered-continuation}.

### 8. Abstract / exact-recovery discrepancy

Fixed.  The abstract no longer mentions exact-recovery benchmarks.  It now
states only ``The implementation is validated on Monte Carlo
experiments.''

### 9. Uncited bibliography entries

Fixed.  Both \texttt{eckhard2011global} and \texttt{eckhard2012pem} are
now cited in Section~2.3, where we discuss the well-documented existence
of multiple local minima in nonlinear PEM structures.

### 10. Polynomial index $b_1$ vs zero-indexed $b_0$

Fixed.  A clarifying sentence has been added next to
Table~\ref{tab:robustness-params}:  ``The notation $b_1$ refers to the
first non-zero $B$ coefficient after the delay $n_z=1$, following the
definitions in Section~2.''

### 11. Monte Carlo sample size $M=30$

Fixed.  The experiment has been re-run with $M=500$.  The text,
table caption, and figure have all been updated.  The standard errors on
the reported means are now below $2\times10^{-4}$.

### 12. Success rate confidence interval

Fixed.  The text now reports the 95\,\% Wilson confidence interval
$[42\,\%,62\,\%]$ for the OE success rate.

### 13. ``Essentially guaranteed convergence'' too strong

Fixed.  The phrase has been replaced with ``achieved a $100\,\%$ empirical
success rate in this problem.''

### 14. Missing SNR in the filtered experiment

Fixed.  The text now reports ``yielding a signal-to-noise ratio of
approximately $-6$\,dB.''

### 15. Missing Stieglitz--McBride original reference

Fixed.  The Stieglitz \& McBride~(1965) paper has been added to the
bibliography and is cited when the SM method is introduced.

### 16. (Duplicate of item~9 — already addressed.)

### 17. Repository URL not stated

The software will be distributed through the Collected Algorithms of the
ACM (CALGO), which assigns a permanent entry upon acceptance.  A GitHub
repository URL will be provided in the final camera-ready version.

### 18. Inconsistent formatting of \texttt{pysib}

Fixed.  We verified that all occurrences of the package name in the prose
use \texttt{\textbackslash\texttt{pysib}}.  Only the title uses plain
text, which is standard for article titles.

### 19. ``predictor-error'' typo

Fixed.  Corrected to ``prediction-error estimators.''

### 20. Language quality

We thank the reviewer for the encouraging comment.
