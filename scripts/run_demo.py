from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from semantic_text_codec import SemanticCodec
from semantic_text_codec.utils.formatting import format_codec_result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the text semantic codec demo.")
    parser.add_argument("--text", required=True, help="Input sentence to transmit.")
    parser.add_argument("--mode", choices=["discrete", "continuous"], default="discrete")
    parser.add_argument("--codebook-size", type=int, default=256)
    parser.add_argument("--semantic-tokens", type=int, default=4)
    parser.add_argument("--dimensions", type=int, default=16)
    args = parser.parse_args()

    codec = SemanticCodec(
        mode=args.mode,
        codebook_size=args.codebook_size,
        semantic_tokens=args.semantic_tokens,
        dimensions=args.dimensions,
    )
    print(format_codec_result(codec.transmit(args.text)))


if __name__ == "__main__":
    main()
