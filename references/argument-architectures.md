# Argument Architectures

Section-level shapes by discipline family and by rhetorical pattern. Never impose
IMRaD (Introduction, Methods, Results, Discussion) universally — it is one
architecture among several, native to experimental/empirical sciences, and often
wrong for mathematics, law, or humanities.

## Family architectures

### Empirical social science
```text
problem → literature → theoretical mechanism → hypotheses/questions →
data → methods → results → interpretation → limitations → contribution
```

### Experimental science
```text
problem → known mechanism → specific uncertainty → experimental strategy →
results → mechanistic interpretation → boundary conditions
```

### Mathematics
```text
problem → notation → definitions → main theorem → supporting results →
proof → discussion / corollaries
```

### Humanities (interpretive)
```text
interpretive problem → existing reading → text/source evidence →
conceptual intervention → close analysis → implication
```

### Law (doctrinal)
```text
legal problem → doctrine/authority → conflict or ambiguity → interpretation →
comparative or normative analysis → consequence
```

### Sociology / institutional social science
```text
concept → mechanism → social structure → empirical pattern → scope condition
```

### Engineering / systems
```text
motivation → design goals/constraints → design choice → implementation →
evaluation/benchmark → ablation → interpretation → limitations
```

### Clinical / health sciences
```text
clinical problem → prior evidence → design → population/sample →
outcome measures → results → clinical interpretation → limitations →
implications for practice (kept separate from causal claims)
```

### Historical study
```text
question → sources → chronological reconstruction → interpretation →
historiographical positioning → implication
```

### Philosophical essay
```text
thesis → key distinction → argument for thesis → strongest objection →
response/qualification → refined thesis
```

## Paragraph- and section-level rhythm patterns

Use these as building blocks inside any of the above architectures — they are
where "the argument moves" rather than merely summarizes:

```text
setup → complication → evidence → interpretation → qualification →
narrowed conclusion
```
```text
claim → counterexample → conceptual distinction → revised claim
```
```text
observation → anomaly → mechanism → implication
```

Vary which pattern governs which paragraph; do not apply the same one
mechanically throughout a document (see `human-scholarly-prose.md` §Controlled
Asymmetry).

## Claim calibration by architecture

Match the architecture's evidentiary apparatus to the claim type it is entitled to
produce:

```text
descriptive | associational | causal | mechanistic | interpretive |
normative | predictive | formal
```

An experimental-science architecture with only correlational data supports
`associational`, not `causal`, claims — no amount of confident prose narrows that
gap (see `disciplines/*.md` for field-specific guardrails, e.g. clinical
association/causal/utility separation).

## Contribution types

Match the stated contribution to what the architecture actually establishes:

```text
new mechanism | new theory | new distinction | boundary condition |
measurement | method | dataset | empirical anomaly | comparative evidence |
historical reinterpretation | doctrinal reinterpretation | conceptual synthesis
```

Avoid generic "gap spotting" ("few studies have examined X") as a stand-in for a
substantive contribution — prefer naming the actual gap type (mechanism gap,
measurement gap, boundary-condition gap, institutional gap, theoretical
contradiction, empirical anomaly, methodological limitation, historical
omission).
