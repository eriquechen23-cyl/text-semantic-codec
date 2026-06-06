from __future__ import annotations

import hashlib

from semantic_text_codec.models.semantic_encoder import SemanticFrame


class ContinuousBottleneck:
    """Compact hashed vector used to explore continuous bottleneck behavior."""

    def __init__(self, dimensions: int = 16, precision: int = 3) -> None:
        if dimensions < 1:
            raise ValueError("dimensions must be at least 1")
        self.dimensions = dimensions
        self.precision = precision

    def encode(self, frame: SemanticFrame) -> list[float]:
        vector = [0.0 for _ in range(self.dimensions)]
        for concept in frame.concepts or frame.tokens:
            digest = hashlib.sha256(concept.encode("utf-8")).digest()
            index = digest[0] % self.dimensions
            sign = 1.0 if digest[1] % 2 == 0 else -1.0
            magnitude = 0.25 + (digest[2] / 255.0)
            vector[index] += sign * magnitude
        return [round(value, self.precision) for value in vector]

    def bits(self) -> int:
        return self.dimensions * 32
