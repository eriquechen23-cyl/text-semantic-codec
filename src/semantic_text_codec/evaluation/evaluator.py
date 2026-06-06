from __future__ import annotations

from dataclasses import asdict

from semantic_text_codec.models.semantic_codec import SemanticCodec


class Evaluator:
    def __init__(self, codec: SemanticCodec | None = None) -> None:
        self.codec = codec or SemanticCodec()

    def run(self, sentences: list[str]) -> list[dict[str, object]]:
        return [asdict(self.codec.transmit(sentence)) for sentence in sentences]
