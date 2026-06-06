from semantic_text_codec import SemanticCodec


def test_meeting_sentence_recovers_meaning() -> None:
    codec = SemanticCodec(mode="discrete", semantic_tokens=4, codebook_size=256)
    result = codec.transmit("The meeting has been postponed because of the heavy rain.")

    assert result.semantic_code
    assert result.code_bits == 32
    assert result.recovered == "The meeting was delayed due to heavy rain."
    assert result.metrics["sentence_similarity"] >= 0.5


def test_continuous_mode_returns_fixed_dimension_vector() -> None:
    codec = SemanticCodec(mode="continuous", dimensions=8)
    result = codec.transmit("The software engineer fixed the server problem.")

    assert len(result.semantic_code) == 8
    assert result.recovered == "The developer resolved the server issue."
