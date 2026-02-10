"""Expose the FastAPI ASGI app at the package level so
`uvicorn backend:app` works when run from the repository root.
"""
try:
    # Import the app from the inner package `app.main` if available
    from .app.main import app  # type: ignore
except Exception:
    try:
        from app.main import app  # type: ignore
    except Exception:
        # Do not raise during import; some test runners import the package
        # without the full runtime environment. Expose a fallback `app` = None.
        app = None  # type: ignore

__all__ = ["app"]
