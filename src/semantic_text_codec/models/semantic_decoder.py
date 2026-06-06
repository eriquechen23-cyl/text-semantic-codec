from __future__ import annotations

from semantic_text_codec.models.semantic_encoder import SemanticFrame


class SemanticDecoder:
    """Rule-based semantic decoder for stage-01 decision testing."""

    def decode(self, frame: SemanticFrame) -> str:
        concepts = set(frame.concepts)
        ordered = frame.concepts

        if {"meeting", "delay", "rain"}.issubset(concepts):
            if "heavy" in concepts:
                return "The meeting was delayed due to heavy rain."
            return "The meeting was delayed due to rain."

        if {"developer", "resolve", "server", "issue"}.issubset(concepts):
            return "The developer resolved the server issue."

        if {"delivery", "arrive", "before", "8am"}.issubset(concepts):
            return "The delivery must arrive before 8 AM."

        if {"automobile", "parked"}.issubset(concepts):
            return "The automobile was parked at the location."

        if ordered:
            readable = " ".join(ordered)
            return readable[:1].upper() + readable[1:] + "."

        return frame.original_text
