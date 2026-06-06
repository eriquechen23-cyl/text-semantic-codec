from __future__ import annotations

import hashlib

from semantic_text_codec.models.semantic_encoder import SemanticFrame


class DiscreteCodebook:
    """Deterministic stand-in for a learned vector-quantized semantic codebook."""

    def __init__(self, codebook_size: int = 256, semantic_tokens: int = 4) -> None:
        if codebook_size < 2:
            raise ValueError("codebook_size must be at least 2")
        if semantic_tokens < 1:
            raise ValueError("semantic_tokens must be at least 1")
        self.codebook_size = codebook_size
        self.semantic_tokens = semantic_tokens

    def encode(self, frame: SemanticFrame) -> list[int]:
        units = frame.concepts or frame.tokens
        codes = [self._hash_to_index(unit) for unit in units[: self.semantic_tokens]]
        while len(codes) < self.semantic_tokens:
            codes.append(self._hash_to_index(f"{frame.signature()}::{len(codes)}"))
        return codes

    def bits(self) -> int:
        return self.semantic_tokens * (self.codebook_size - 1).bit_length()

    def _hash_to_index(self, value: str) -> int:
        digest = hashlib.sha256(value.encode("utf-8")).digest()
        return int.from_bytes(digest[:4], "big") % self.codebook_size
