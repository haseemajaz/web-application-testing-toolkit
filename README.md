# 12 — Web Application Testing Toolkit

**Area:** Security Engineering · **Stack:** Python 3.10+ (standard library only) · **Status:** Portfolio starter, safe local demo

## What it does

A controlled testing workflow for a web application you own or have written permission to test, in one tool:

- **Header and cookie checks** on a local URL (same checks as project 11, reused as a module-style workflow)
- **Form inventory:** fetches a page, lists its forms, methods, and fields, so you can plan manual testing instead of guessing
- **Reporting:** writes a Markdown report (`report.md`) with findings, a test checklist, and a sign-off section — the document an employer actually wants to see
- **Workflow doc:** `docs/testing-workflow.md` walks through a full test, from scope to report, including what *not* to do

No payloads, no automated exploitation, no credential stuffing. The toolkit finds the surface and documents it; a human does the testing.

## What an employer sees

- You can scope a test, inventory a target, and write a report a client can act on
- You know the difference between automated checks and manual testing
- Your output is a report, not a terminal dump

## How to run

```bash
cd 12-web-application-testing-toolkit

# Against a local app only (default)
python3 web_toolkit.py --url http://127.0.0.1:8000/

# Any other target requires explicit consent, otherwise it refuses
python3 web_toolkit.py --url https://example.com/ --i-have-written-consent
```

Start a local server first to try it: `python3 -m http.server 8000` in any folder, then run the command above.

## Try it yourself

Point it at a local page with a form, check `report.md`, and follow `docs/testing-workflow.md` to manually test one form field at a time, recording each result in the report.

## Safety — read this

Educational only. **Only test applications you own or have written permission to test.** Unauthorised testing is illegal in many jurisdictions. This tool refuses non-localhost targets without the consent flag, sends no payloads, and stores no credentials.
