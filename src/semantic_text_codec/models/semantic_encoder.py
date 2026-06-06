from __future__ import annotations

from dataclasses import dataclass

from semantic_text_codec.models.tokenizer import Tokenizer


CONCEPT_LEXICON: dict[str, str] = {
    "meeting": "meeting",
    "conference": "meeting",
    "postponed": "delay",
    "postpone": "delay",
    "delayed": "delay",
    "delay": "delay",
    "heavy": "heavy",
    "rain": "rain",
    "software": "software",
    "engineer": "developer",
    "developer": "developer",
    "fixed": "resolve",
    "fix": "resolve",
    "resolved": "resolve",
    "server": "server",
    "problem": "issue",
    "issue": "issue",
    "delivery": "delivery",
    "arrive": "arrive",
    "arrival": "arrive",
    "before": "before",
    "after": "after",
    "must": "requirement",
    "should": "requirement",
    "8": "8am",
    "am": "8am",
    "car": "automobile",
    "automobile": "automobile",
    "parked": "parked",
    "there": "location",
}

NEGATION_WORDS = {"no", "not", "never", "none", "cannot", "can't"}
TIME_WORDS = {"before", "after", "am", "pm", "today", "tomorrow", "yesterday"}
QUANTITY_WORDS = {"one", "two", "three", "first", "second", "third"}
LOCATION_WORDS = {"there", "here", "office", "home", "server"}
INTENT_WORDS = {"must", "should", "need", "needs", "required"}


@dataclass(frozen=True)
class SemanticFrame:
    original_text: str
    tokens: list[str]
    concepts: list[str]
    flags: dict[str, bool]

    def signature(self) -> str:
        concept_part = "|".join(self.concepts)
        flag_part = "|".join(name for name, enabled in sorted(self.flags.items()) if enabled)
        return f"{concept_part}::{flag_part}"


class SemanticEncoder:
    """Maps text into a compact, inspectable semantic frame."""

    def __init__(self, tokenizer: Tokenizer | None = None) -> None:
        self.tokenizer = tokenizer or Tokenizer()

    def encode(self, text: str) -> SemanticFrame:
        tokens = self.tokenizer.tokenize(text)
        concepts = self._concepts_from_tokens(tokens)
        flags = {
            "negation": any(token in NEGATION_WORDS for token in tokens),
            "time": any(token in TIME_WORDS or token.isdigit() for token in tokens),
            "quantity": any(token in QUANTITY_WORDS or token.isdigit() for token in tokens),
            "location": any(token in LOCATION_WORDS for token in tokens),
            "intent": any(token in INTENT_WORDS for token in tokens),
        }
        return SemanticFrame(original_text=text, tokens=tokens, concepts=concepts, flags=flags)

    def _concepts_from_tokens(self, tokens: list[str]) -> list[str]:
        concepts: list[str] = []
        for token in tokens:
            concept = CONCEPT_LEXICON.get(token)
            if concept and concept not in concepts:
                concepts.append(concept)
        if concepts:
            return concepts
        return [token for token in tokens if len(token) > 2][:8]
