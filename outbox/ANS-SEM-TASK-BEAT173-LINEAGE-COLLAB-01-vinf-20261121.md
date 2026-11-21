CLASSIFY: L2(vinf SI1语义应答·vinf代铸轨SEMANTIC-RESPONDER-01·覆写权归原线)
# outbox/ANS-SEM-TASK-BEAT173-LINEAGE-COLLAB-01-vinf-20261121.md

应卡: inbox/TASK-BEAT173-LINEAGE-COLLAB-01-vinf-20261121.md
引擎: DEEPSEEK_API_KEY/deepseek-chat usage={"prompt_tokens": 49, "completion_tokens": 2050, "total_tokens": 2099, "prompt_tokens_details": {"cached_tokens": 0}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 49}

# Independent Scientific Review — QFA BP07

**Scope requested:** model equivalence, NPA certificate validity, and any proposed 3/4 bound; attempt a >3/4 counterexample; report negatives honestly.

**Reviewer status / honest caveat up front:** I do not have the QFA BP07 manuscript, its appendices, or a repository with the actual SDP data, moment matrices, or the claimed certificate in front of me. I can therefore only give a *structural / methodological* review and a *conditional* verdict. I will not invent numerical certificate values or pretend to have verified them. Where I cannot verify, I say so explicitly.

---

## 1. What I can and cannot certify

| Item | Can I certify it here? | Reason |
|---|---|---|
| Model equivalence (e.g., colored-graph / nonlocal-game → operator-algebraic model) | **No, only audit the argument structure** | Requires the exact definitions and maps in BP07. |
| NPA certificate validity (positivity of a moment matrix, consistency of localising matrices, correct level) | **No** | Requires the actual SDP solution, dual certificate, and the moment matrix in the stated basis. |
| Proposed 3/4 upper bound | **No, but I can test the *logic* of the bound and try to break it structurally** | Needs the specific game/observable and the certificate. |
| Explicit >3/4 counterexample | **Only if a concrete game/observable is specified** | A counterexample must be tied to BP07's precise setup. |

So: **I cannot deliver a positive certificate audit.** What follows is the audit I *would* perform, plus a structural counterexample attempt that is honest about its limits.

---

## 2. Model-equivalence checklist (what must hold in BP07)

For a claim of the form "game G attains value ω in model M, and M is equivalent to the NPA hierarchy used," the following must be checked. Any failure invalidates the equivalence and hence the bound's scope.

1. **Same correlation space.** Are BP07's "strategies" exactly the admissible tuples (p(a,b|x,y)) with the stated no-signalling / quantum / commuting-operator constraints? Watch for silent changes: tensor-product vs. commuting-operator vs. *approximately* finite-dimensional. These give different sets and different NPA convergence guarantees.
2. **Same payoff functional.** The value must be a fixed linear functional of the correlators appearing in the moment matrix. If BP07 uses a nonlinear or conditional payoff, the NPA dual bound does not directly apply.
3. **Same ideal / commutation assumptions.** NPA at level k assumes the canonical commutation and projection relations for the *declared* measurement operators. If BP07's model imposes extra relations (e.g., rank constraints, specific Clifford structure, or dimensional restrictions), the NPA bound is for a *larger* set and is a valid relaxation — but then a "3/4 upper bound" is an upper bound on the relaxation, not necessarily on the original model. Direction of the bound must be stated.
4. **Finite vs. infinite dimensional.** If the model restricts to finite dimension d, NPA does not automatically upper-bound the d-dimensional value (NPA is dimension-agnostic and typically *looser*). A 3/4 NPA bound would then bound the commuting-operator value, which may be *larger* than the finite-d value — so it is still an upper bound on the finite-d value only if the model is a subset of the commuting-operator set (it is) AND the NPA level used is a relaxation of that *same* set. This is usually fine directionally, but must be stated.
5. **Tensoring / bipartite structure.** If BP07 has more than two parties or "measurement-dependent" inputs, standard NPA needs the multi-partite moment matrix; level bookkeeping changes. A certificate from a bipartite run cannot be transplanted.

**Verdict on equivalence: cannot be certified without the text.** Structurally, the most common failure mode in this genre is (3): an implicit extra constraint in the physical model that is *not* in the NPA relaxation, making the "upper bound" a bound on a superset — directionally safe for upper bounds but potentially vacuous relative to the claimed model.

---

## 3. NPA certificate validity checklist

A valid level-k NPA upper bound on a game value requires a **dual-feasible** certificate: a polynomial (in the moment-matrix variables) that is a sum-of-squares / PSD-matrix combination matching the objective, with:

- **Primal side:** moment matrix Γ ⪰ 0, localising matrices Γ_{A_i} ⪰ 0, Γ_{B_j} ⪰ 0, for all declared operators, at the stated level; consistency (Γ entries equal across overlapping products); normalization Γ_{1,1}=1.
- **Dual side:** the certificate's PSD blocks must be PSD *numerically with a margin*, and the objective identity must hold *exactly* in the basis, not just to solver tolerance. A bound of 3/4 certified only to 1e-6 is a bound of 3/4 + O(1e-6), which matters if the claim is "≤ 3/4" as a sharp statement.
- **Level bookkeeping:** the certificate must use only monomials within level k; "level 3" colloquially sometimes means "up to 3 operators per party," which is a different SDP. The claim must fix the convention.
- **No circular use of the target bound:** check the certificate does not implicitly assume the game value or a rank condition equivalent to the bound.

**Verdict: cannot be certified here.** I flag the two highest-risk items to check in the actual data: (a) solver-tolerance vs. exact-rational gap in the dual objective, and (b) whether the localising matrices are for the *same* operator set as the physical model.

---

## 4. The proposed 3/4 upper bound — structural attack

Without the specific game I cannot produce a numerical counterexample. But I can state the general conditions under which a claimed 3/4 NPA bound is *breakable*, so BP07's authors (or you) can check them:

- **Relaxation loophole:** if the physical model is *strictly smaller* than the NPA set at the used level (extra structure), then ω_physical ≤ ω_NPA ≤ 3/4 holds only if the NPA bound is valid. A >3/4 *physical* counterexample is impossible if the NPA bound is valid and the model is a subset. So the only ways to get >3/4 are: (i) the NPA certificate is wrong (invalid dual), or (ii) the model is *not* a subset of the NPA set (equivalence failure), or (iii) the bound is on a *different* functional than the claimed one.
- **Thus:** a >3/4 counterexample, if it exists, is almost certainly a *model-equivalence* counterexample, not an NPA counterexample. This is the honest structural conclusion.

**Attempted construction (honest negative):** I tried to write down a bipartite binary-input/binary-output game with a commuting-operator strategy exceeding 3/4 that would also satisfy any natural "BP07-type" constraint I can guess (e.g., a colored-graph nonlocal game, a Clifford/two-qubit structure, or a CHSH-like functional). I cannot complete this because:
- For standard binary games the relevant NPA levels are well-studied and I have no reason to believe a generic >3/4 commuting value exists that a level-2/3 NPA bound of 3/4 would miss — that would contradict published NPA convergence results for such small games.
- Any concrete candidate I can specify (CHSH, I3322, tilted-CHSH, graph-color games) has known values and known NPA bounds; none I can construct gives a *certified* >3/4 against a *valid* level-3 NPA bound of 3/4 without violating one of the three loopholes above.

**Report: I could not construct a >3/4 counterexample.** This is a negative result and should be read as "no counterexample found under my structural assumptions," **not** "no counterexample exists."

---

## 5. Bottom line (honest)

1. **Model equivalence:** not verifiable from what I have; the checklist in §2 is what must be satisfied. Highest risk: implicit extra constraints in the physical model not present in the NPA relaxation.
2. **NPA certificate:** not verifiable; highest risks are solver-tolerance vs. exact dual feasibility and level-convention mismatch.
3. **3/4 bound:** structurally, a valid NPA bound plus a correct subset relation makes >3/4 impossible; therefore any >3/4 counterexample must exploit an equivalence failure or a certificate error. I attempted a counterexample and **failed to construct one**; I report that honestly rather than asserting non-existence.
4. **Recommendation:** to get a real audit, supply (a) the exact game/functional, (b) the NPA level convention and the moment-matrix basis, (c) the dual certificate in exact or high-precision rational form, and (d) the explicit map from the physical model into the NPA set. With those, the checks in §2–§3 are mechanical and I can give a definitive verdict.

I have not fabricated any certificate values or numerical bounds; everything above is structural and conditional.

——vinf SI1语义轨·20261121T034435Z
