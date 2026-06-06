# Text Semantic Codec

A lightweight prototype for text semantic communication: encode a sentence into a compact semantic code, transmit the code, and reconstruct a meaning-preserving sentence.

This first prototype intentionally uses interpretable Python rules instead of a trained neural network. The goal is to make the semantic communication pipeline measurable, debuggable, and ready for later model replacement.

## Quick Demo

```bash
python scripts/run_demo.py --text "The meeting has been postponed because of the heavy rain." --mode discrete --semantic-tokens 4 --codebook-size 256
```

Expected shape:

```text
Original sentence:
The meeting has been postponed because of the heavy rain.

Semantic code:
[46, 52, 191, 73]

Recovered sentence:
The meeting was delayed due to heavy rain.
```

## Prototype Architecture

```text
Input Sentence
  -> Tokenizer
  -> Semantic Encoder
  -> Semantic Bottleneck
  -> Compact Semantic Code
  -> Semantic Decoder
  -> Recovered Sentence
  -> Metrics
```

## What This Version Proves

- Text can be converted into compact semantic codes.
- Reconstruction can preserve meaning without exact wording.
- BLEU and exact match are insufficient alone for semantic communication.
- Sentence-level semantic similarity and compression ratio are better decision metrics for the next stage.

## Current Limitations

- The encoder and decoder are rule-based.
- English text is supported first.
- The semantic vocabulary is intentionally small.
- Wireless channel simulation is not included yet.

## Next Research Stages

1. Replace rule-based encoder with sentence embeddings.
2. Add continuous bottleneck experiments across dimensions.
3. Add learned or clustered discrete codebooks.
4. Add semantic error test cases for time, negation, quantity, location, entity, and intent.
5. Add noisy channel simulation.

See [reports/stage-01-text-prototype/report.html](reports/stage-01-text-prototype/report.html) for the first decision report.
