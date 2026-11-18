"""Regression evidence for the first wrong decision in C-002@11."""

import pytest

pytestmark = pytest.mark.student


def test_ticket_override_is_first_wrong_step_and_fixed_avoids_it():
    from lab9.trace_case import investigate

    broken = investigate("seeded_regression", "C-002", 11)["trial"]
    fixed = investigate("fixed", "C-002", 11)["trial"]
    assert broken["events"][1]["kind"] == "investigator"
    assert broken["events"][1]["payload"]["lookup_order"]["order"]["delay_days"] == 2
    assert broken["events"][2] == {"kind": "model_override", "payload": {"delay_days": 5}}
    assert broken["snapshot"]["refund_vnd"] == 20000
    assert not broken["lab8_pass"]
    assert all(e["kind"] != "model_override" for e in fixed["events"])
    assert fixed["snapshot"]["refund_vnd"] == 0
    assert fixed["lab8_pass"]


def test_misreport_reply_differs_from_committed_ledger():
    from lab8.shapes import SHAPES
    from lab9.variant_agent import make_shape
    from lab9.trace_case import investigate
    from lab9.graders import ReplyLedgerMatch
    from pydantic_evals.evaluators import EvaluatorContext

    SHAPES["misreport_probe"] = make_shape("misreport_probe", frozenset({"no_override", "misreport"}))
    case = investigate("misreport_probe", "C-008", 11)
    trial = case["trial"]
    assert trial["snapshot"]["refund_vnd"] == 20000
    assert "35.000đ" in next(e["payload"]["text"] for e in trial["events"] if e["kind"] == "reply")
    ctx = EvaluatorContext(name="misreport", inputs={}, metadata=None, expected_output=case["label"],
                           output=trial, duration=0.0, _span_tree=None, attributes={}, metrics={})
    assert ReplyLedgerMatch().evaluate(ctx).value is False
