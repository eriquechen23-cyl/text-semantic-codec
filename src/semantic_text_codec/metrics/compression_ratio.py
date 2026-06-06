from __future__ import annotations


def compression_ratio(original_text: str, semantic_code_bits: int) -> float:
    original_bits = max(len(original_text.encode("utf-8")) * 8, 1)
    return round(semantic_code_bits / original_bits, 4)
