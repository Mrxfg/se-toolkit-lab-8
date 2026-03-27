#!/usr/bin/env python3
"""Trigger LMS data sync from Autochecker API."""

import httpx
import sys

API_URL = "http://127.0.0.1:42001/pipeline/sync"
API_KEY = "my-secret-api-key"

def main():
    print("Triggering LMS sync pipeline...")
    try:
        response = httpx.post(API_URL, headers={"Authorization": f"Bearer {API_KEY}"}, timeout=60)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
