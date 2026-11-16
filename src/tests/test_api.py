import pytest
from fastapi.testclient import TestClient

import api


@pytest.fixture
def calls(monkeypatch):
    recorded = []

    def fake_refine(text, model):
        recorded.append((text, model))
        return "refined"

    monkeypatch.setattr(api, "refine", fake_refine)
    return recorded


client = TestClient(api.app)


def test_get_uses_default_model_and_prompt(calls):
    response = client.get("/generate_get", params={"text": "helo"})
    assert response.status_code == 200
    assert response.json() == "refined"
    assert calls == [(api.PROMPT.format("helo"), api.MODEL)]


def test_post_uses_default_model(calls):
    response = client.post("/generate_post", json={"text": "helo"})
    assert response.status_code == 200
    assert calls[0][1] == api.MODEL


def test_post_accepts_custom_model_and_prompt(calls):
    client.post("/generate_post", json={"text": "helo", "model": "openai/gpt-5-nano", "prompt": "Fix: {}"})
    assert calls == [("Fix: helo", "openai/gpt-5-nano")]
