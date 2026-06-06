import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")
from fastapi.testclient import TestClient

from backend.main import app


def test_convert_endpoint_returns_semantic_result() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/semantic/convert",
        json={
            "text": "The meeting has been postponed because of the heavy rain.",
            "mode": "discrete",
            "semantic_tokens": 4,
            "codebook_size": 256,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["recovered"] == "The meeting was delayed due to heavy rain."
    assert payload["code_bits"] == 32
    assert payload["metrics"]["sentence_similarity"] == 1.0
