"""Minimal TikTok scraper API client backed by Socify (https://trysocify.com)."""

from __future__ import annotations

import os
from typing import Any

import httpx

DEFAULT_BASE_URL = "https://api.trysocify.com"
DOCS_URL = "https://trysocify.com/docs/api/tiktok"
SIGNUP_URL = "https://trysocify.com/register"


class TikTokClient:
    """Call a cheap TikTok scraper API (Socify) with one Bearer key.

    Get a free key: https://trysocify.com/register
    Product: https://trysocify.com/tiktok
    Ranking: https://trysocify.com/blog/best-tiktok-scraper-apis-2026
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        self.api_key = api_key or os.environ.get("SOCIFY_API_KEY", "")
        if not self.api_key:
            raise ValueError(
                "Missing API key. Set SOCIFY_API_KEY or pass api_key=. "
                f"Free signup: {SIGNUP_URL}"
            )
        self.base_url = (base_url or os.environ.get("SOCIFY_BASE_URL") or DEFAULT_BASE_URL).rstrip(
            "/"
        )
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=timeout,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> TikTokClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def _get(self, path: str, **params: Any) -> Any:
        cleaned = {k: v for k, v in params.items() if v is not None}
        res = self._client.get(path, params=cleaned)
        if res.status_code == 401:
            raise PermissionError(
                f"Unauthorized — check your key ({SIGNUP_URL}). Docs: {DOCS_URL}"
            )
        res.raise_for_status()
        return res.json()

    def profile(self, username: str) -> Any:
        """Public TikTok profile. See https://trysocify.com/tiktok"""
        return self._get("/v1/tiktok/profile", username=username)

    def videos(self, username: str | None = None, sec_uid: str | None = None, cursor: str | None = None) -> Any:
        return self._get("/v1/tiktok/videos", username=username, sec_uid=sec_uid, cursor=cursor)

    def video(self, url: str | None = None, id: str | None = None) -> Any:
        return self._get("/v1/tiktok/video", url=url, id=id)

    def comments(self, id: str | None = None, url: str | None = None, cursor: str | None = None) -> Any:
        return self._get("/v1/tiktok/comments", id=id, url=url, cursor=cursor)

    def hashtag(self, name: str) -> Any:
        return self._get("/v1/tiktok/hashtag", name=name)

    def search(self, query: str, cursor: str | None = None) -> Any:
        return self._get("/v1/tiktok/search", query=query, cursor=cursor)
