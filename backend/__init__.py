"""Expose the FastAPI ASGI app at the package level so
`uvicorn backend:app` works when run from the repository root.
"""
try:
    # Import the app from the inner package `app.main`
    from .app.main import app  # type: ignore
except Exception:  # fallback for environments where relative import may behave differently
    # Attempt absolute import path (helps when running from different cwd)
    try:
        from app.main import app  # type: ignore
    except Exception:
        # If import fails, re-raise the original error for visibility
        raise

__all__ = ["app"]
