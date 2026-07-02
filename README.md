# BetterCo Document-Search App

A small browser UI over the BetterCo backend **Document Search** gateway: search a
company, create a case, and retrieve its documents. It talks **only** to the BetterCo
REST API (Partner key+secret → JWT) — no direct upstream/provider access.

## Run

```bash
cp .env.example .env      # fill in your Partner key/secret + workspace/org ids
pip install -r requirements.txt
python3 kyc_case_app.py   # opens http://localhost:8770
```

By default it targets whatever `BETTERCO_BASE_URL` points to (staging in the sample
`.env`). Set `KYC_GATEWAY_BASE_URL=http://localhost:8080` to hit a local backend.

## Files

| File | Purpose |
|---|---|
| `kyc_case_app.py` | Zero-dependency `http.server` app + local API |
| `kyc_gateway_client.py` | BetterCo REST client (auth + gateway calls) |
| `kyc_case.html` | Single-page UI (bilingual DE/EN) |

## Buttons

- **Create case** — real create via the gateway (billable when the backend has creation enabled).
- **Dry run** — builds and shows the would-be payload entirely in the browser; sends nothing.
