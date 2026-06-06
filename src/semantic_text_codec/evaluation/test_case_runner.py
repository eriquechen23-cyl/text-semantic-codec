from __future__ import annotations

from semantic_text_codec.metrics.text_metrics import sentence_similarity


def run_semantic_test_cases(cases: list[dict[str, object]], threshold: float = 0.75) -> list[dict[str, object]]:
    results = []
    for case in cases:
        score = sentence_similarity(str(case["original"]), str(case["candidate"]))
        predicted = score >= threshold
        results.append(
            {
                **case,
                "sentence_similarity": score,
                "predicted_semantic_match": predicted,
                "passed": predicted == bool(case["expected_semantic_match"]),
            }
        )
    return results
