from __future__ import annotations


def semantic_efficiency(sentence_similarity: float, semantic_code_bits: int) -> float:
    if semantic_code_bits <= 0:
        return 0.0
    return round(sentence_similarity / semantic_code_bits, 6)
