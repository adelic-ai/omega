"""Determinism of Sigma -> IR value lowering. A value must render identically for identical tests, across rules
and across runs — in particular, no Python object repr (which embeds a memory address) may leak into an Atom."""

import os
import re
from pathlib import Path

import pytest
from sigma.collection import SigmaCollection

from omega.axes import CONTENT, attributes
from omega.ingest.sigma import NULL_VALUE, load_ir, to_ir

SIGMA = Path(os.environ["OMEGA_SIGMA_CORPUS"]) if os.environ.get("OMEGA_SIGMA_CORPUS") else \
    Path(__file__).resolve().parents[2] / "semantic-cyber/data/sigma-rules"

_ADDRESS = re.compile(r"object at 0x[0-9a-fA-F]+")

_NULL_RULE = """\
title: {t}
id: 00000000-0000-0000-0000-00000000000{n}
logsource:
  product: aws
  service: cloudtrail
detection:
  selection:
    eventName: DeleteBucket
  selection_status_null:
    errorCode: null
  condition: selection and 1 of selection_status_*
"""


def _lower(title: str, n: int):
    (rule,) = SigmaCollection.from_yaml(_NULL_RULE.format(t=title, n=n)).rules
    return to_ir(rule)


def _null_atom(ir):
    return next(a for b in ir.blocks for a in b.atoms if a.field == "errorCode")


def test_null_lowers_to_the_sentinel():
    assert _null_atom(_lower("A", 1)).values == (NULL_VALUE,)


def test_identical_null_tests_in_different_rules_share_a_clause():
    """Before the fix each SigmaNull instance stringified to its own address, so no two rules ever overlapped."""
    a, b = _lower("A", 1), _lower("B", 2)
    assert _null_atom(a) == _null_atom(b)
    shared = set(attributes(a, axes=CONTENT)) & set(attributes(b, axes=CONTENT))
    assert f"+clause:errorCode|={NULL_VALUE}" in shared


@pytest.mark.skipif(not SIGMA.is_dir(), reason="vendored sigma-rules corpus not present")
def test_no_object_repr_leaks_into_the_corpus_ir():
    """Whole-corpus guard: no atom value anywhere contains a memory address, so lowering is run-stable."""
    rules, _ = load_ir(SIGMA)
    leaks = [
        (r.id, a.field, v)
        for r in rules for b in r.blocks for a in b.atoms for v in a.values
        if _ADDRESS.search(v)
    ]
    assert not leaks, leaks[:5]
