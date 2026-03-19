"""
Clerk JWT verification using JWKS.
Every protected endpoint depends on get_current_user().
"""

import time
import httpx
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.config import settings

bearer_scheme = HTTPBearer()

_jwks_cache: dict = {}
_jwks_fetched_at: float = 0.0
JWKS_TTL = 3600


async def _get_jwks() -> dict:
      global _jwks_cache, _jwks_fetched_at
      now = time.time()
      if _jwks_cache and (now - _jwks_fetched_at) < JWKS_TTL:
                return _jwks_cache
            async with httpx.AsyncClient() as client:
                      resp = await client.get(settings.clerk_jwks_url, timeout=10)
                      resp.raise_for_status()
                  _jwks_cache = resp.json()
    _jwks_fetched_at = now
    return _jwks_cache


async def get_current_user(
      credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
      """Verifies Clerk JWT and returns decoded payload with user info."""
    token = credentials.credentials
    jwks = await _get_jwks()

    try:
              header = jwt.get_unverified_header(token)
              kid = header.get("kid")
              key = next(
                  (k for k in jwks.get("keys", []) if k.get("kid") == kid), None
              )
              if key is None:
                            raise HTTPException(
                                              status_code=status.HTTP_401_UNAUTHORIZED,
                                              detail="No matching JWK found for token kid",
                            )

              public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
              payload = jwt.decode(
                  token, public_key, algorithms=["RS256"],
                  options={"verify_aud": False},
              )
              return payload

except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
except jwt.InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {exc}")
