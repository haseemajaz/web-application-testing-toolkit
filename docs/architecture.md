# Architecture — Web Application Testing Toolkit

## Flow

```
--url (localhost by default)
  →  consent guard, else refuse (exit 2)
  →  fetch()  →  status, headers, HTML
  →  header / cookie checks  →  findings
  →  inventory_forms()  →  forms, methods, fields
  →  report_md()  →  report.md (findings + forms + manual checklist + sign-off)
```

## Components

| Piece | Role |
|---|---|
| `fetch()` | One GET with a timeout, standard library only |
| `inventory_forms()` | Regex form inventory: action, method, field names |
| `EXPECTED_HEADERS` | Header checks with severity |
| `report_md()` | The deliverable: a Markdown report a client can read |
| `docs/testing-workflow.md` | The human workflow the tool supports |

## Design decisions

- **The report is the product.** Automated checks are the easy part; a readable report with scope, findings, and sign-off is what a client pays for.
- **No payloads.** The toolkit inventories and documents; it does not exploit. That keeps it publishable and legal to demo.
- **Localhost by default, consent flag for anything else.** Same guard as project 11, so the safety rule is consistent across the portfolio.
