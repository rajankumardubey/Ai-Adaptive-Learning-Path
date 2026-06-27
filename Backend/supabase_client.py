"""Supabase client helper.

This creates a shared Supabase client using `SUPABASE_URL` and `SUPABASE_KEY`
from `Backend/config.py` (loaded from environment or .env). The implementation
is defensive: if `supabase` package isn't installed the module still loads and
`get_supabase()` will return None.

To use in code:
    from supabase_client import get_supabase
    client = get_supabase()
    if client:
        resp = client.table('users').select('*').execute()

Install dependency: add `supabase` to your Python environment (see
`Backend/requirements.txt`).
"""
from typing import Optional
from config import settings

try:
    from supabase import create_client
except Exception:  # pragma: no cover - optional dependency
    create_client = None


_client = None

def _init_client():
    global _client
    if _client is not None:
        return _client
    if not create_client:
        return None
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        return None
    _client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    return _client


def get_supabase() -> Optional[object]:
    """Return a supabase client or None if unavailable.

    This is a light wrapper so other modules can import this function and
    obtain the client without raising if the package or credentials are
    missing.
    """
    return _init_client()
