from semantic_text_codec.metrics.compression_ratio import compression_ratio
from semantic_text_codec.metrics.text_metrics import bleu, exact_match, sentence_similarity


def test_exact_match_is_strict() -> None:
    assert exact_match("My car was parked there.", "My automobile was parked there.") is False


def test_sentence_similarity_handles_synonyms() -> None:
    score = sentence_similarity("My car was parked there.", "My automobile was parked there.")
    assert score >= 0.5


def test_bleu_penalizes_paraphrase_more_than_similarity() -> None:
    reference = "The software engineer fixed the server problem."
    candidate = "The developer resolved the server issue."

    assert bleu(reference, candidate) < sentence_similarity(reference, candidate)


def test_compression_ratio_is_code_over_original_bits() -> None:
    assert compression_ratio("abcd", 8) == 0.25
