from __future__ import annotations

import math
from collections import Counter

from semantic_text_codec.models.semantic_encoder import CONCEPT_LEXICON
from semantic_text_codec.models.tokenizer import Tokenizer


TOKENIZER = Tokenizer()
STOPWORDS = {
    "a",
    "an",
    "and",
    "because",
    "been",
    "due",
    "has",
    "of",
    "the",
    "to",
    "was",
}


def exact_match(original: str, recovered: str) -> bool:
    return original.strip() == recovered.strip()


def bleu(reference: str, candidate: str, max_n: int = 2) -> float:
    ref_tokens = TOKENIZER.tokenize(reference)
    cand_tokens = TOKENIZER.tokenize(candidate)
    if not ref_tokens or not cand_tokens:
        return 0.0

    precisions = []
    for n in range(1, max_n + 1):
        ref_counts = Counter(_ngrams(ref_tokens, n))
        cand_counts = Counter(_ngrams(cand_tokens, n))
        if not cand_counts:
            precisions.append(0.0)
            continue
        overlap = sum(min(count, ref_counts[gram]) for gram, count in cand_counts.items())
        precisions.append((overlap + 1) / (sum(cand_counts.values()) + 1))

    geo_mean = math.exp(sum(math.log(score) for score in precisions) / max_n)
    brevity_penalty = min(1.0, math.exp(1 - len(ref_tokens) / len(cand_tokens)))
    return round(brevity_penalty * geo_mean, 4)


def rouge_l(reference: str, candidate: str) -> float:
    ref_tokens = TOKENIZER.tokenize(reference)
    cand_tokens = TOKENIZER.tokenize(candidate)
    if not ref_tokens or not cand_tokens:
        return 0.0
    lcs = _lcs_length(ref_tokens, cand_tokens)
    precision = lcs / len(cand_tokens)
    recall = lcs / len(ref_tokens)
    if precision + recall == 0:
        return 0.0
    return round((2 * precision * recall) / (precision + recall), 4)


def sentence_similarity(reference: str, candidate: str) -> float:
    ref_concepts = set(_concepts(reference))
    cand_concepts = set(_concepts(candidate))
    if not ref_concepts or not cand_concepts:
        return 0.0
    score = len(ref_concepts & cand_concepts) / len(ref_concepts | cand_concepts)
    return round(score, 4)


def _concepts(text: str) -> list[str]:
    return [
        CONCEPT_LEXICON.get(token, token)
        for token in TOKENIZER.tokenize(text)
        if len(token) > 1 and token not in STOPWORDS
    ]


def _ngrams(tokens: list[str], n: int) -> list[tuple[str, ...]]:
    return [tuple(tokens[index : index + n]) for index in range(0, len(tokens) - n + 1)]


def _lcs_length(left: list[str], right: list[str]) -> int:
    table = [[0] * (len(right) + 1) for _ in range(len(left) + 1)]
    for i, left_token in enumerate(left, start=1):
        for j, right_token in enumerate(right, start=1):
            if left_token == right_token:
                table[i][j] = table[i - 1][j - 1] + 1
            else:
                table[i][j] = max(table[i - 1][j], table[i][j - 1])
    return table[-1][-1]
