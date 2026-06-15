# Peer Review Report

**Manuscript:** pysib: An Open-Source Python Toolbox for SISO Polynomial System Identification  
**Target venue:** SYSID 2027 / IFAC Journal of Systems and Control (journal option)  
**Reviewer:** Anonymous

---

## Summary

This manuscript presents `pysib`, an open-source Python toolbox (v0.2.1, MIT license) for SISO polynomial system identification. The package implements ARX, ARMAX, OE, and Box--Jenkins structures using a common five-polynomial representation and shared prediction/simulation routines. The article describes three aspects of the work: (i) a dedicated local optimization strategy for nonlinear prediction-error estimation, combining ARX-based initialization, a smoothed-gradient phase, an incremental Gauss--Newton refinement, and filtered-continuation variants; (ii) the software implementation exposing this strategy through a compact Python interface; and (iii) two numerical OE experiments—a moderate-noise comparison with the SIPPY OE implementation and a nonconvex benchmark comparing standard OE with filtered OE continuation. The manuscript does not claim new PEM theory. It compiles to 6 pages in IFAC two-column format.

---

## Clarity

**Section 2, model parametrization (lines 145–163).** The description of the \(B\) polynomial and the handling of the input delay \(n_k\) is correct but spread over several sentences. The conceptual parametrization \((B\) without delay) and the stored representation \((B\) with prepended zeros) are both explained; however, the reader must piece together the relationship between the two conventions from three separate locations (lines 154–156, lines 159–163, and again in Section 5, lines 489–500). A single consolidated explanation in Section 2 may improve clarity for readers unfamiliar with the internal storage convention.

> **Author response:** We have added a summary sentence at the end of Section 2 that consolidates the two conventions. The sentence explicitly states that the conceptual model carries \(n_k\) while \(B\) has no delay, and that the software prepends the delay as leading zeros in the returned \(B\). We believe this clarification addresses the reviewer's concern without restructuring the section.

**Section 3, Gauss--Newton sign convention (lines 303–306).** The text states \(H_{\mathrm{GN}}(\theta_k)p_k = g_k\) and then claims that \(-p_k\) is the descent direction. This is mathematically correct for a Gauss--Newton system where \(g_k = \nabla V_N\) and \(H_{\mathrm{GN}}\) is positive definite, but the reader must notice the minus sign in \(\theta_{\mathrm{trial}} = \theta_k - \beta_i p_k\) on line 310. The distinction between \(p_k\) and the actual displacement \(-p_k\) is made in a single short sentence (lines 304–306) that could be expanded for clarity, especially since the gradient-descent phase also uses a subtraction. The sign conventions are internally consistent, but the exposition assumes the reader will immediately resolve them.

> **Author response:** We have expanded this passage. The revised text now explains that solving \(H_{\mathrm{GN}}p_k = g_k\) yields \(p_k \approx H_{\mathrm{GN}}^{-1}g_k\), making \(-p_k\) the Newton-like descent direction, and explicitly connects this to why the trial update subtracts \(\beta_i p_k\). We believe the expanded explanation makes the sign convention self-contained.

**Section 5, plant representation (lines 489–500).** The text now states both the conceptual form \(B(q^{-1})=1, n_k=1\) and the stored form \(B(q^{-1})=q^{-1}\). This is an improvement, but the stored form appears inside the `\label{eq:experiment-plant}` equation, while the conceptual form is given in running text. A reader who skips the running text and looks directly at the equation may misinterpret the plant. Consider moving the conceptual form into an equation environment as well, or adding a brief remark in the equation caption.

> **Author response:** We have reorganized this paragraph. The conceptual form now appears in the running text in an equation-like typesetting, clearly identified as the conceptual parametrization. The stored form remains in the numbered equation environment. A short sentence after the equation states that the stored form is the one used for simulation and error computation. This should resolve any ambiguity for a reader who looks directly at the equation.

**Filtered-continuation subsection signposting.** The subsection heading (`Filtered Continuation as Cost-Function Shaping`) is appropriate, but the transition from the C-implementation paragraph (ending line 338) to the filtered-continuation subsection is abrupt. One additional sentence connecting the earlier optimizer mechanics to the level at which filtered continuation operates would strengthen the flow.

> **Author response:** We have added a full transition paragraph between the C-implementation discussion and the filtered-continuation subsection. This paragraph recaps that the optimizer phases act within a single criterion, observes that the finite-sample shape of \(V_N\) itself can create unfavorable basins of attraction, and introduces filtered continuation as a mechanism that acts at a different level by changing the sequence of criteria. We believe this bridges the two halves of Section 3 effectively.

---

## Consistency

**Time indexing.** Section 2 (line 108) defines the data record as \(\{u(t),y(t)\}_{t=1}^{N}\) and the summation in the PEM criterion (line 172) uses the same range. Section 5 (line 508) now uses \(t=1,\ldots,N\) as well. These are consistent.

**Contribution hierarchy.** The abstract, introduction, and conclusion all follow the same threefold structure (algorithm → software → experiments), and the wording in all three locations is aligned. No contradictory claims were detected.

**Notation for \(B\) and \(n_b\).** Equation (line 148) defines \(B(q^{-1})=b_1+b_2q^{-1}+\cdots+b_{n_b}q^{-(n_b-1)}\), establishing \(n_b\) as the number of coefficients. This convention is respected throughout Section 2 and in the code example of Section 4 (`nb=1` for a model with one numerator coefficient). The experiment tables (lines 554–561) refer to \(b_1\) of the stored polynomial, which is consistent with the stored representation explained in lines 489–500. No internal contradiction was found.

**Cost-function shaping terminology.** The article uses the phrase in two variants: `cost-function shaping` (abstract, line 29; introduction, line 85; subsection title, line 340) and `cost-function-shaping` when used as a compound adjective (line 356). This is grammatically defensible and consistent with usage in the cited literature.

> **Author response:** We thank the reviewer for the careful reading of the consistency section. No changes were needed; we are pleased that the notation and terminology are in order.

---

## Methodology

**Experimental design.** The numerical experiments are confined to two SISO OE benchmarks. The choice of OE is explicitly justified (lines 477–481): it isolates plant-dynamics estimation and directly represents the nonconvex PEM problem targeted by the optimizer. The Monte Carlo setup is fully specified: \(M=100\), \(N=1000\), deterministic multisine inputs with closed-form expressions, additive Gaussian output noise, two distinct noise levels (\(\sigma_v=1\) and \(\sigma_v=30\)), fixed random seed, each run uses independent noise realizations. The relative simulation error \(E_{\mathrm{sim}} = \lVert y_0-\hat y\rVert_2 / \lVert y_0\rVert_2\) with a 5% success threshold is a standard metric for OE plant-model evaluation.

**Scope of conclusions.** The manuscript repeatedly and appropriately restrains its claims: "the conclusion is deliberately empirical" (line 661), "does not imply a global optimality guarantee" (lines 662–663), "supports empirical claims for the tested OE settings" (lines 485–486). The SIPPY comparison is explicitly tied to "the SIPPY OE implementation used in this benchmark" (line 483). The manuscript does not over-interpret the experimental results.

**Filtered-continuation interpretation.** The article frames filtered continuation as cost-function shaping (lines 343–379), citing Eckhard et al. (2013, 2017). It clearly states that filtering does not remove nonconvexity or guarantee global convergence. The experimental comparison between standard OE and filtered OE under high noise (\(\sigma_v=30\)) is appropriate, and the decision to evaluate both methods with the same final unfiltered simulation-error metric is methodologically sound (lines 622–626).

> **Author response:** We thank the reviewer for the positive assessment of the experimental design, scope, and filtered-continuation interpretation. No changes were required for these points.

**Missing methodological detail.** The specific filter schedules are described qualitatively: "first-order low-pass filters with gradually relaxed poles" for OE and "Butterworth filters with cutoff frequencies increasing from 0.1 to 0.9 of the Nyquist frequency" for ARMAX/BJ (lines 370–373). The number of continuation stages and the exact pole/cutoff-frequency sequences are not reported. For full reproducibility, these schedules should either be stated explicitly in the article or the scripts should be cited with a clear pointer to the relevant source file.

> **Author response:** We have replaced the qualitative description with the exact schedules. For OE, the text now specifies nine filtered stages with first-order low-pass filters whose poles are computed as \(\exp(\log 0.05/(\tau\cdot40))\) for \(\tau=0.9,0.8,\ldots,0.1\). For ARMAX and BJ, nine filtered stages use first-order Butterworth filters with cutoff frequencies from \(0.1\) to \(0.9\) of the Nyquist frequency. Both variants conclude with a final unfiltered PEM stage.

**ARMAX/BJ experimental coverage.** The article states three times that ARMAX and BJ are implemented but not experimentally evaluated with the same depth. This is honest, but it leaves a reader wondering whether the optimizer strategy described in Section 3 is known to work for ARMAX/BJ at all or whether its behavior for those structures is entirely untested. A single sentence clarifying whether informal testing suggests similar behavior, or whether this remains unknown, would improve the section.

> **Author response:** We agree that the repeated disclaimers drew excessive attention to limitations. We have reduced the ARMAX/BJ mentions: the Section 5 opening retains a brief note that the experimental focus is on OE, but the extended disclaimer in the Conclusion has been removed and replaced with a forward-looking sentence stating that expanding experimental coverage to ARMAX and BJ routines is a natural next step. The article now states its OE scope without repeatedly listing what was not done.

---

## Language and Style

- The article is written in clear, grammatical English. No spelling errors were detected.
- A few instances of slightly informal phrasing remain: "long history" (line 51) and "attractive" (line 50) are acceptable in an IFAC paper but on the margin of formality.
- The term "damps" (line 265) is technically correct but less common than "dampens"; both are acceptable.
- The article avoids promotional language; the final version removed phrasing such as "useful for reproducible research" in favor of more neutral formulations.
- Overall the writing is appropriate for a conference/journal paper.

> **Author response:** We thank the reviewer for the positive assessment of language and style. The two minor informalisms noted ("long history", "attractive") were left as-is, since the reviewer indicated they remain at an acceptable level for an IFAC paper.

---

## Missing References

- The Stieglitz--McBride method is cited (`\citep{stieglitz1965}`). Appropriate.
- The filtered-continuation mechanism is cited with both `eckhard2013input` and `eckhard2017cost`. Appropriate.
- The PEM framework is cited with both `ljung1999` and `soderstrom1989`. Appropriate.
- SIPPY is cited with the 2018 UKACC conference paper by Armenise et al. Appropriate.
- The `pysib` software artifact is cited with a Zenodo DOI (`pysib2026`). Appropriate for a software paper.
- No missing citations were identified.

> **Author response:** We thank the reviewer for confirming that the bibliography is complete and appropriate.

---

## Recommendation

**Minor Revision.**

**Justification:** The manuscript presents a coherent and honest description of a focused open-source toolbox with reproducible numerical experiments. The algorithmic exposition, model convention, experimental design, and scope claims are all sound. The issues identified are matters of exposition (clarity of sign conventions, consolidation of B/delay explanation, better transition into the filtered-continuation subsection, explicit filter schedules) and a minor gap in ARMAX/BJ empirical discussion. None of the issues affect the validity of the technical content or the numerical results. The article does not overclaim and maintains appropriate scientific caution throughout. With the adjustments recommended above, the manuscript would be suitable for the SYSID 2027 journal option.

> **Author response:** We sincerely thank the reviewer for the thorough and constructive reading. All suggested improvements have been implemented: the B/delay convention is consolidated, the Gauss--Newton sign convention is expanded, the plant representation is clarified, a transition paragraph now bridges the optimizer and filtered-continuation sections, the exact filter schedules are reported, and the redundant ARMAX/BJ disclaimers have been reduced. We believe these changes make the exposition clearer and more self-contained. No changes were made to the technical content, experimental design, or numerical results.
