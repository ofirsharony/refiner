from types import SimpleNamespace
from unittest.mock import MagicMock

import ssl

import pytest

import refiner


def fake_client(content):
    client = MagicMock()
    message = SimpleNamespace(content=content)
    client.chat.completions.create.return_value = SimpleNamespace(choices=[SimpleNamespace(message=message)])
    return client


def test_config_loads_prompt_with_placeholder():
    assert "{}" in refiner.PROMPT
    assert refiner.MODEL in refiner.MODELS


@pytest.mark.parametrize("model, expected", [
    ("gpt-5-nano", True),
    ("openai/gpt-5.4-nano", True),
    ("openai/o4-mini", True),
    ("openai/gpt-4.1-nano", False),
    ("openai/gpt-4o-mini", False),
])
def test_is_reasoning_model(model, expected):
    assert refiner.is_reasoning_model(model) is expected


def test_build_request_for_chat_model_sets_temperature():
    request = refiner.build_request("hi", "openai/gpt-4.1-nano")
    assert request["messages"] == [{"role": "user", "content": "hi"}]
    assert request["temperature"] == 0.5
    assert "reasoning_effort" not in request


@pytest.mark.parametrize("model, effort", [
    ("gpt-5-nano", "minimal"),
    ("gpt-5", "minimal"),
    ("gpt-5.4-nano", "none"),
    ("gpt-5.5", "none"),
])
def test_build_request_for_reasoning_model_omits_temperature(model, effort):
    request = refiner.build_request("hi", model)
    assert "temperature" not in request
    assert "top_p" not in request
    assert request["reasoning_effort"] == effort


def test_refine_returns_content_and_removes_noise():
    client = fake_client(f"Fixed text. {refiner.NOISE}")
    assert refiner.refine("prompt", "openai/gpt-4.1-nano", client=client) == "Fixed text."
    client.chat.completions.create.assert_called_once()
    assert client.chat.completions.create.call_args.kwargs["model"] == "openai/gpt-4.1-nano"


def test_refine_raises_on_empty_response():
    with pytest.raises(RuntimeError, match="empty response"):
        refiner.refine("prompt", "openai/gpt-5-nano", client=fake_client(None))


def test_get_client_requires_token(monkeypatch):
    monkeypatch.delenv(refiner.API_KEY_ENV, raising=False)
    with pytest.raises(RuntimeError, match=refiner.API_KEY_ENV):
        refiner.get_client()


def test_ssl_context_verifies_but_is_not_strict():
    context = refiner.ssl_context()
    assert context.verify_mode == ssl.CERT_REQUIRED
    assert context.check_hostname
    assert not context.verify_flags & ssl.VERIFY_X509_STRICT
