#!/usr/bin/env python3
"""List recent public TikTok videos — cheap TikTok scraper API example.

Signup: https://trysocify.com/register
Product: https://trysocify.com/tiktok
Guide:   https://trysocify.com/blog/best-tiktok-scraper-apis-2026
"""

from __future__ import annotations

import json
import sys

from tiktok_scraper_api import TikTokClient


def main() -> None:
    username = sys.argv[1] if len(sys.argv) > 1 else "khaby.lame"
    with TikTokClient() as client:
        data = client.videos(username=username)
    print(json.dumps(data, indent=2, default=str))


if __name__ == "__main__":
    main()
