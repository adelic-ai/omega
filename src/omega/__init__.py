"""omega — FCA/SKOS rule-sameness across detection rulesets (Sigma, CAR), mapped onto ATT&CK and ATLAS.
Structure first, behavior later.

Layered around a ruleset-agnostic IR (the waist):

  ingest/       per-ruleset adapters — parse + lower to the IR
    sigma.py      Sigma via pySigma: Stage 0 ingest + Stage 1 map to the IR
    car.py        MITRE CAR (structured axes only; query logic counted, not parsed)
    atlas.py      MITRE ATLAS spine -> AtlasTechnique (a taxonomy, not a ruleset)
  ir.py         the agnostic IR: the atoms the analysis reads            (Stage 1's target)
  axes.py       the attribute knob: field / clause / polarity / fieldref / logsource / attack / atlas   (Stage 2)
  fca.py        concepts + subsumption order                             (Stage 3)
  skos.py       graded relations (exact/close/broad/narrow/related) + Turtle       (Stage 4)
  report.py     the over-collapse + generalization figures, cross-corpus bridge   (Stage 5)
  coverage.py   the ATLAS transitive bridge + five-way coverage classifier
  cli.py        `run` / `bridge` / `atlas`                                (Stage 6)

Below the IR is ruleset-specific; at the IR the languages converge; above it omega is written once.
Parsing is delegated to the official parsers (pySigma for Sigma); omega owns the analysis.
"""
