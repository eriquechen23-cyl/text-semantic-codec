from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from semantic_text_codec.metrics.compression_ratio import compression_ratio
from semantic_text_codec.metrics.semantic_efficiency import semantic_efficiency
from semantic_text_codec.metrics.text_metrics import bleu, exact_match, rouge_l, sentence_similarity
from semantic_text_codec.models.continuous_bottleneck import ContinuousBottleneck
from semantic_text_codec.models.discrete_codebook import DiscreteCodebook
from semantic_text_codec.models.semantic_decoder import SemanticDecoder
from semantic_text_codec.models.semantic_encoder import SemanticEncoder, SemanticFrame


Mode = Literal["discrete", "continuous"]


@dataclass(frozen=True)
class CodecResult:
    original: str
    semantic_frame: SemanticFrame
    semantic_code: list[int] | list[float]
    recovered: str
    code_bits: int
    metrics: dict[str, float | bool]


class SemanticCodec:
    """Text semantic communication pipeline."""

    def __init__(
        self,
        mode: Mode = "discrete",
        codebook_size: int = 256,
        semantic_tokens: int = 4,
        dimensions: int = 16,
    ) -> None:
        self.mode = mode
        self.encoder = SemanticEncoder()
        self.decoder = SemanticDecoder()
        self.discrete = DiscreteCodebook(codebook_size=codebook_size, semantic_tokens=semantic_tokens)
        self.continuous = ContinuousBottleneck(dimensions=dimensions)

    def transmit(self, text: str) -> CodecResult:
        frame = self.encoder.encode(text)
        if self.mode == "discrete":
            semantic_code: list[int] | list[float] = self.discrete.encode(frame)
            code_bits = self.discrete.bits()
        elif self.mode == "continuous":
            semantic_code = self.continuous.encode(frame)
            code_bits = self.continuous.bits()
        else:
            raise ValueError(f"Unsupported mode: {self.mode}")

        recovered = self.decoder.decode(frame)
        metrics = self._metrics(text, recovered, code_bits)
        return CodecResult(
            original=text,
            semantic_frame=frame,
            semantic_code=semantic_code,
            recovered=recovered,
            code_bits=code_bits,
            metrics=metrics,
        )

    def _metrics(self, original: str, recovered: str, code_bits: int) -> dict[str, float | bool]:
        similarity = sentence_similarity(original, recovered)
        return {
            "exact_match": exact_match(original, recovered),
            "bleu": bleu(original, recovered),
            "rouge_l": rouge_l(original, recovered),
            "sentence_similarity": similarity,
            "compression_ratio": compression_ratio(original, code_bits),
            "semantic_efficiency": semantic_efficiency(similarity, code_bits),
        }
