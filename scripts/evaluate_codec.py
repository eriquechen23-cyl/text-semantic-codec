from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from semantic_text_codec.evaluation.evaluator import Evaluator
from semantic_text_codec.models.semantic_codec import SemanticCodec


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate the semantic codec on a sentence JSON file.")
    parser.add_argument("--data", default="data/sample_sentences.json")
    parser.add_argument("--mode", choices=["discrete", "continuous"], default="discrete")
    args = parser.parse_args()

    data_path = PROJECT_ROOT / args.data
    sentences = json.loads(data_path.read_text(encoding="utf-8"))
    evaluator = Evaluator(SemanticCodec(mode=args.mode))
    print(json.dumps(evaluator.run(sentences), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
