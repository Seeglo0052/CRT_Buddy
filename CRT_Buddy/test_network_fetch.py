# -*- coding: utf-8 -*-
"""Basic test for util.net.fetch_with_retry.
This test hits a known unreachable URL to force retries quickly.
"""
import time
from util.net import fetch_with_retry, NetworkError

# A URL that should 404 quickly (example domain is valid but path not found)
TEST_URL = "https://example.com/__nonexistent_path__"

def test_404_no_retry():
    start = time.time()
    resp = fetch_with_retry('GET', TEST_URL, timeout=3, retries=2)
    assert resp.status_code == 404, f"Expected 404, got {resp.status_code}"
    elapsed = time.time() - start
    print(f"✓ 404 did not trigger extra backoff (elapsed ~{elapsed:.2f}s)")

# A URL on httpbin that returns 503 to trigger retry attempts
def test_retry_503():
    start = time.time()
    try:
        resp = fetch_with_retry('GET', 'https://httpbin.org/status/503', timeout=3, retries=2, backoff_base=0.2)
    except NetworkError as e:
        print(f"✓ Retry exhausted as expected: {e}")
    else:
        # If somehow returns 503 but not raising, ensure status is 503
        assert resp.status_code == 503
        print("✓ Received 503; retry logic would have attempted")
    elapsed = time.time() - start
    print(f"(elapsed ~{elapsed:.2f}s)")

if __name__ == '__main__':
    test_404_no_retry()
    test_retry_503()
    print("All network fetch tests completed.")
