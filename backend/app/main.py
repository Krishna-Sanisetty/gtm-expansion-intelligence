"""Minimal FastAPI entrypoint for GTM Expansion Intelligence."""

from fastapi import FastAPI

app = FastAPI(
    title="GTM Expansion Intelligence",
    description="Evidence-driven post-sales GTM intelligence API (skeleton).",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness check used by local development and future container probes."""
    return {
        "status": "ok",
        "service": "gtm-expansion-intelligence",
    }
