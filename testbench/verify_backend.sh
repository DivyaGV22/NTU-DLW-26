#!/usr/bin/env bash
# Verify that the Learning Analytics backend is running and responding.
# Run this from any directory after starting the backend (default: http://localhost:8000).
# Usage: ./verify_backend.sh   or   bash verify_backend.sh

BASE_URL="http://localhost:8000"
echo "Checking backend at $BASE_URL ..."

if curl -s -f "$BASE_URL" > /dev/null; then
    echo "OK - Backend is running."
    curl -s "$BASE_URL"
    echo ""
    exit 0
else
    echo "FAIL - Backend did not respond. Is it running on port 8000?"
    exit 1
fi
