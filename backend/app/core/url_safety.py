"""
Shared URL/host safety checks — prevents SSRF by rejecting URLs that point
at loopback, private, link-local, or otherwise internal/reserved hosts.

Used by both the web-search company resolver and the direct URL scraper,
since both eventually hand a URL to an outbound HTTP client on the server.
"""

from __future__ import annotations

from urllib.parse import urlparse
import ipaddress

LOCAL_HOSTNAMES = {
    "localhost",
    "metadata.google.internal",
}

BLOCKED_HOST_SUFFIXES = (
    ".localhost",
    ".local",
    ".internal",
    ".home.arpa",
    ".nip.io",
    ".sslip.io",
)

# Cloud metadata endpoints (AWS/GCP/Azure/DigitalOcean all use this IP).
BLOCKED_LITERAL_IPS = {"169.254.169.254"}


def is_unsafe_host(hostname: str) -> bool:
    host = (hostname or "").lower().strip()
    if not host:
        return True

    if host in LOCAL_HOSTNAMES:
        return True

    if host.endswith(BLOCKED_HOST_SUFFIXES):
        return True

    if host.startswith("localhost"):
        return True

    if host in BLOCKED_LITERAL_IPS:
        return True

    try:
        ip = ipaddress.ip_address(host)
        return (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_reserved
            or ip.is_multicast
            or ip.is_unspecified
        )
    except ValueError:
        # Not a direct IP literal — hostname will be resolved by the HTTP
        # client itself; we can't catch DNS-rebinding here, only the
        # obvious literal/hostname cases above.
        return False


def is_safe_http_url(url: str) -> bool:
    """True only for well-formed http(s) URLs that don't target an internal host."""
    try:
        parsed = urlparse(str(url))
    except Exception:
        return False

    if parsed.scheme not in {"http", "https"}:
        return False

    if not parsed.netloc:
        return False

    host = parsed.netloc.lower().split(":", 1)[0]
    return not is_unsafe_host(host)
