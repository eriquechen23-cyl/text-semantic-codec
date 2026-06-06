from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Literal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

PROJECT_SRC = Path(__file__).resolve().parents[1] / "src"
if PROJECT_SRC.exists() and str(PROJECT_SRC) not in sys.path:
    sys.path.insert(0, str(PROJECT_SRC))

from semantic_text_codec import SemanticCodec


Mode = Literal["discrete", "continuous"]


class ConvertRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)
    mode: Mode = "discrete"
    codebook_size: int = Field(256, ge=2, le=4096)
    semantic_tokens: int = Field(4, ge=1, le=32)
    dimensions: int = Field(16, ge=1, le=1024)


class ConvertResponse(BaseModel):
    original: str
    mode: Mode
    semantic_concepts: list[str]
    semantic_flags: dict[str, bool]
    semantic_code: list[int] | list[float]
    recovered: str
    code_bits: int
    metrics: dict[str, float | bool]


def _allowed_origins() -> list[str]:
    raw_origins = os.getenv("ALLOWED_ORIGINS", "*")
    return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]


app = FastAPI(
    title="Text Semantic Codec API",
    version="0.2.0",
    summary="Text semantic communication API for compact meaning-preserving reconstruction.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins(),
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "Text Semantic Codec API",
        "status": "ready",
        "docs": "/docs",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/semantic/convert", response_model=ConvertResponse)
def convert_text(request: ConvertRequest) -> ConvertResponse:
    codec = SemanticCodec(
        mode=request.mode,
        codebook_size=request.codebook_size,
        semantic_tokens=request.semantic_tokens,
        dimensions=request.dimensions,
    )
    result = codec.transmit(request.text)
    return ConvertResponse(
        original=result.original,
        mode=request.mode,
        semantic_concepts=result.semantic_frame.concepts,
        semantic_flags=result.semantic_frame.flags,
        semantic_code=result.semantic_code,
        recovered=result.recovered,
        code_bits=result.code_bits,
        metrics=result.metrics,
    )
