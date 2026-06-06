from __future__ import annotations

from semantic_text_codec.models.semantic_codec import CodecResult


def format_codec_result(result: CodecResult) -> str:
    metric_lines = "\n".join(f"{name}: {value}" for name, value in result.metrics.items())
    return (
        f"Original sentence:\n{result.original}\n\n"
        f"Semantic concepts:\n{result.semantic_frame.concepts}\n\n"
        f"Semantic flags:\n{result.semantic_frame.flags}\n\n"
        f"Semantic code:\n{result.semantic_code}\n\n"
        f"Recovered sentence:\n{result.recovered}\n\n"
        f"Semantic code size:\n{result.code_bits} bits\n\n"
        f"{metric_lines}"
    )
