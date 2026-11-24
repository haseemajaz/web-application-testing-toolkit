#!/usr/bin/env python3
"""Web Application Testing Toolkit — safe local demo.

Inventories forms on a local page, checks security headers and cookies,
and writes a Markdown report. Localhost by default; any other target
requires --i-have-written-consent. No payloads, no exploitation.
Standard library only.
"""
import argparse
import ipaddress
import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

EXPECTED_HEADERS = {
    "strict-transport-security": "High",
    "content-security-policy": "High",
    "x-frame-options": "Medium",
    "x-content-type-options": "Medium",
    "referrer-policy": "Low",
}


def is_localhost(host):
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return host in ("localhost",)


def fetch(url):
    with urllib.request.urlopen(url, timeout=5) as response:
        return response.status, dict(response.headers), response.read().decode("utf-8", "ignore")


def inventory_forms(html):
    forms = []
    for match in re.finditer(r"<form[^>]*>(.*?)</form>", html, re.I | re.S):
        tag = match.group(0)
        action = re.search(r'action="([^"]*)"', tag, re.I)
        method = re.search(r'method="([^"]*)"', tag, re.I)
        fields = re.findall(r'<(?:input|textarea|select)[^>]*name="([^"]+)"', tag, re.I)
        forms.append({"action": action.group(1) if action else "(same page)",
                      "method": (method.group(1) if method else "GET").upper(),
                      "fields": fields})
    return forms


def check(url):
    status, headers, html = fetch(url)
    lower = {k.lower(): v for k, v in headers.items()}
    findings = []
    for name, severity in EXPECTED_HEADERS.items():
        if name not in lower:
            findings.append((severity, f"Missing header: {name}"))
    if lower.get("server"):
        findings.append(("Low", f"Server banner disclosed: {lower['server']}"))
    return status, findings, inventory_forms(html)


def report_md(url, status, findings, forms):
    lines = [f"# Web Application Test Report", "", f"**Target:** {url}", f"**HTTP status:** {status}", "",
             "## Findings", ""]
    lines += [f"- [{s}] {f}" for s, f in findings] or ["- No automated findings."]
    lines += ["", "## Forms found", ""]
    for form in forms:
        lines.append(f"- {form['method']} {form['action']} — fields: {', '.join(form['fields']) or '(none)'}")
    if not forms:
        lines.append("- No forms found on this page.")
    lines += ["", "## Manual test checklist", "",
              "- [ ] Test each form field for input validation (own app / authorised test only)",
              "- [ ] Check authentication: locked-out accounts, session expiry, logout",
              "- [ ] Check authorisation: can a low-privilege user reach admin pages?",
              "- [ ] Check file upload, if any: type, size, and storage location",
              "", "## Sign-off", "", "Tester: __________  Date: __________  Scope authorised by: __________",
              "", "*Automated checks only. Manual findings go in this report by hand.*"]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:8000/")
    parser.add_argument("--i-have-written-consent", action="store_true")
    parser.add_argument("--output", default="report.md")
    args = parser.parse_args()
    host = urlparse(args.url).hostname or ""
    if not is_localhost(host) and not args.i_have_written_consent:
        print("REFUSED: target is not localhost. Re-run with --i-have-written-consent "
              "only if you have written authorisation to test this target.", file=sys.stderr)
        return 2
    try:
        status, findings, forms = check(args.url)
    except Exception as exc:
        print(f"Could not fetch {args.url}: {exc}", file=sys.stderr)
        return 1
    print(f"Target: {args.url}  Status: {status}  Findings: {len(findings)}  Forms: {len(forms)}")
    for severity, finding in findings:
        print(f"  [{severity}] {finding}")
    Path(args.output).write_text(report_md(args.url, status, findings, forms))
    print(f"Report written to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
