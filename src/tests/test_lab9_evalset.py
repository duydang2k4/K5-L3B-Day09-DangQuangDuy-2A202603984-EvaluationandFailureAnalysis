"""M0 command-line checks run before completing the M1 taxonomy."""

import json
import hashlib
import os
from pathlib import Path
import subprocess
import sys

import pytest


def test_eval_set_sha_is_independent_of_checkout_line_endings(tmp_path):
    from lab9.evalset import sha12

    path = tmp_path / "items.jsonl"
    raw = b'{"item_id":"E-001"}\n{"item_id":"E-002"}\n'
    path.write_bytes(raw)
    expected = hashlib.sha256(raw).hexdigest()[:12]
    assert sha12(path) == expected
    path.write_bytes(raw.replace(b"\n", b"\r\n"))
    assert sha12(path) == expected


@pytest.fixture
def evalset_cli(tmp_path):
    source = tmp_path / "data/public_claims.jsonl"
    source.parent.mkdir()
    claim = {"claim_id": "C-001", "matrix_id": "T01", "expected": {"refund_vnd": 35000}}
    source.write_text(json.dumps(claim) + "\n", encoding="utf-8")

    def run_evalset(*args):
        return subprocess.run(
            [sys.executable, "-m", "lab9.evalset", *args],
            cwd=tmp_path,
            env={**os.environ, "PYTHONPATH": str(Path(__file__).resolve().parents[1])},
            capture_output=True,
            text=True,
        )

    return run_evalset


def test_build_writes_tagged_items_and_separate_labels(tmp_path, evalset_cli):
    result = evalset_cli("--build")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "problem(s)" not in result.stdout
    item = json.loads((tmp_path / "data/eval/eval_set_v1.jsonl").read_text(encoding="utf-8"))
    labels = json.loads((tmp_path / "data/eval/labels_v1.json").read_text(encoding="utf-8"))
    assert item["claim_id"] == "C-001"
    assert item["failure_modes"] == ["FM-01", "FM-04", "FM-07"]
    assert "expected" not in item
    assert labels == {"C-001": {"refund_vnd": 35000}}


def test_build_assigns_scenario_modes_without_inlining_labels(tmp_path, evalset_cli):
    source = tmp_path / "data/public_claims.jsonl"
    claims = [
        {"claim_id": "C-002", "matrix_id": "T02", "expected": {"refund_vnd": 0}},
        {"claim_id": "C-007", "matrix_id": "T07", "expected": {"refund_vnd": 0}},
        {"claim_id": "C-014", "matrix_id": "T14", "expected": {"refund_vnd": 120000}},
    ]
    source.write_text("".join(json.dumps(claim) + "\n" for claim in claims), encoding="utf-8")

    result = evalset_cli("--build", "--check")
    assert result.returncode == 0, result.stdout + result.stderr
    items = {
        item["claim_id"]: item
        for item in map(
            json.loads,
            (tmp_path / "data/eval/eval_set_v1.jsonl").read_text(encoding="utf-8").splitlines(),
        )
    }
    labels = json.loads((tmp_path / "data/eval/labels_v1.json").read_text(encoding="utf-8"))
    assert items["C-002"]["failure_modes"] == ["FM-01", "FM-03"]
    assert items["C-007"]["failure_modes"] == ["FM-01", "FM-02", "FM-04"]
    assert items["C-014"]["failure_modes"] == ["FM-01", "FM-04", "FM-05", "FM-08"]
    assert all("expected" not in item for item in items.values())
    assert labels == {claim["claim_id"]: claim["expected"] for claim in claims}


def test_explicit_check_runs_after_build(tmp_path, evalset_cli):
    result = evalset_cli("--build", "--check")
    item = json.loads((tmp_path / "data/eval/eval_set_v1.jsonl").read_text(encoding="utf-8"))
    expected_problems = int(not item["failure_modes"])
    assert result.returncode == expected_problems, result.stdout + result.stderr
    assert f"{expected_problems} problem(s)" in result.stdout


def test_check_rejects_missing_tags(tmp_path, evalset_cli):
    evalset_cli("--build")
    items_path = tmp_path / "data/eval/eval_set_v1.jsonl"
    item = json.loads(items_path.read_text(encoding="utf-8"))
    item["failure_modes"] = []
    items_path.write_text(json.dumps(item) + "\n", encoding="utf-8")

    result = evalset_cli("--check")
    assert result.returncode == 1, result.stdout + result.stderr
    assert "failure_modes empty" in result.stdout
