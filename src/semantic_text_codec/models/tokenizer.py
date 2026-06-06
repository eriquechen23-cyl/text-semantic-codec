from __future__ import annotations

import re


TOKEN_PATTERN = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?")


class Tokenizer:
    """Small tokenizer for the stage-01 English text prototype."""

    def tokenize(self, text: str) -> list[str]:
        return [match.group(0).lower() for match in TOKEN_PATTERN.finditer(text)]
