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

## Web App Prototype

The repository now includes a deployable web prototype:

- `backend/`: FastAPI API for text semantic conversion.
- `frontend/`: Angular 21 standalone UI.
- `render.yaml`: Render Blueprint with one Python web service and one static site.

### Backend Local Run

```bash
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

API endpoint:

```text
POST /api/semantic/convert
```

### Frontend Local Run

Angular 21 requires Node 20+.

```bash
cd frontend
npm install
npm start
```

The frontend calls the deployed Render backend URL from application code and does not show the backend API field in the user interface.

### Render Deployment

Create a Render Blueprint from this GitHub repo. Render will read `render.yaml` and create:

- `text-semantic-codec-api`

After deployment, set the API service `ALLOWED_ORIGINS` value to the final Vercel frontend URL instead of `*` for production use.

Current backend deployment:

```text
https://text-semantic-codec-api.onrender.com
```

Health check:

```text
https://text-semantic-codec-api.onrender.com/health
```

### Vercel Frontend Deployment

The Angular UI is configured for Vercel with `frontend/vercel.json`.

Current production deployment:

```text
https://frontend-coral-psi-78.vercel.app
```

See [reports/stage-02-render-angular/report.html](reports/stage-02-render-angular/report.html) for the deployment decision report.
