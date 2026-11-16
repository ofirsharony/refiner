"""Tests for the Automator scripts. Stub `curl` and `open` on PATH, so no server or network is needed."""
import json
import os
import stat
import subprocess
import urllib.parse
from pathlib import Path

import pytest

AUTOMATIONS = Path(__file__).resolve().parent.parent / "Automations"
REPLACE = AUTOMATIONS / "replace_in_place.sh"
REVIEW = AUTOMATIONS / "review_diff.sh"

TRICKY_TEXTS = [
    "normal text, it's fine",
    "ends with a quote 'like this'",
    "has '''triple''' quotes",
    r"path C:\Users\ofir",
    r"literal \n here",
    "''' + str(__import__('os').getcwd()) + '''",
    "a & b = c? 100% #tag",
    'he said "ok" `ls` $HOME *',
    "שלום ’curly’",
    "two\nlines  with   spaces",
]


def write_stub(directory, name, body):
    path = directory / name
    path.write_text("#!/bin/bash\n" + body)
    path.chmod(path.stat().st_mode | stat.S_IEXEC)


def run(script, text, stub_dir):
    env = {**os.environ, "PATH": f"{stub_dir}:{os.environ['PATH']}"}
    return subprocess.run(["bash", str(script), text], env=env, capture_output=True, text=True, check=True)


@pytest.fixture
def stubs(tmp_path):
    """Fake `curl` records its args and prints $CURL_RESPONSE (exit $CURL_EXIT); fake `open` records the URL."""
    write_stub(tmp_path, "curl", f'printf "%s\\n" "$@" > {tmp_path}/curl_args\nprintf "%s" "$CURL_RESPONSE"\nexit ${{CURL_EXIT:-0}}\n')
    write_stub(tmp_path, "open", f'printf "%s" "$1" > {tmp_path}/open_url\n')
    return tmp_path


def run_replace(text, stubs, response=None, exit_code=0, monkeypatch=None):
    monkeypatch.setenv("CURL_RESPONSE", "" if response is None else json.dumps(response, ensure_ascii=False))
    monkeypatch.setenv("CURL_EXIT", str(exit_code))
    return run(REPLACE, text, stubs).stdout


@pytest.mark.parametrize("text", TRICKY_TEXTS)
def test_replace_sends_text_unchanged_to_api(text, stubs, monkeypatch):
    run_replace(text, stubs, response="ok", monkeypatch=monkeypatch)
    args = (stubs / "curl_args").read_text().splitlines()
    # curl gets "text=<raw text>" and URL-encodes it itself. A newline in the text splits it over lines here.
    sent = "\n".join(args[args.index("--data-urlencode") + 1:])
    assert sent == f"text={text}"
    assert "http://localhost:8005/generate_get" in args


@pytest.mark.parametrize("refined", TRICKY_TEXTS)
def test_replace_prints_decoded_api_response(refined, stubs, monkeypatch):
    assert run_replace("input", stubs, response=refined, monkeypatch=monkeypatch) == refined


def test_replace_keeps_original_when_api_fails(stubs, monkeypatch):
    assert run_replace("keep me", stubs, exit_code=7, monkeypatch=monkeypatch) == "keep me"


def test_replace_keeps_original_when_response_is_not_json(stubs, monkeypatch):
    monkeypatch.setenv("CURL_RESPONSE", "OK")
    assert run(REPLACE, "keep me", stubs).stdout == "keep me"


def test_replace_keeps_original_when_response_is_empty_string(stubs, monkeypatch):
    assert run_replace("keep me", stubs, response="", monkeypatch=monkeypatch) == "keep me"


@pytest.mark.parametrize("text", TRICKY_TEXTS)
def test_review_opens_ui_with_text_unchanged(text, stubs):
    result = run(REVIEW, text, stubs)
    url = urllib.parse.urlsplit((stubs / "open_url").read_text())
    query = urllib.parse.parse_qs(url.query)
    assert url.netloc == "localhost:8504"
    assert query["auto_generate"] == ["true"]
    assert query["text"] == [text]
    assert result.stdout == ""  # Automator must not replace the selection
