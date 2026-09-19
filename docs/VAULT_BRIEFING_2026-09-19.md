# Key Vault — the KYC vendor credential: written, and the blocker was not where we looked

**19 September 2026. Go-live 1 October.** Supersedes the request-for-action version of this file,
written the same morning. Three of its four asks were already satisfied and its central finding was
wrong; both are recorded below rather than deleted, because the wrong reading is easy to repeat.

Staging was missing the KYC.com sandbox credential, and the earlier reading placed the gap in a vault
that no deployment reads. **The secret now exists in `bc-stg-vault`, which is the vault the staging
app actually reads.** Nothing else on the original list needed doing. One verification is open, and
until it passes nothing here has been proven at runtime.

---

## 1. One action was needed, and it is done

`know-your-customer-com-sandbox` was copied from the working entry in `bc-dev-vault-dev` into
`bc-stg-vault`, where it did not exist. Both environments point at the same vendor sandbox
(`api.knowyourcustomer.dev`) under the same secret name, so it is the same credential.

| | before | after |
|---|---|---|
| `know-your-customer-com` | 2026-07-01 | **2026-07-01, untouched** |
| `know-your-customer-com-sandbox` | absent | created 2026-09-19 09:24 UTC, enabled |
| `know-your-customer-com-user` | 2026-07-13 | untouched |

It was a create, not an overwrite, so there was nothing to lose. The value was shape-checked for
`clientId` and `secret` before writing and never passed through a terminal or a shell history:

```bash
VAL="$(az keyvault secret show --vault-name bc-dev-vault-dev \
       --name know-your-customer-com-sandbox --query value -o tsv)"
az keyvault secret set --vault-name bc-stg-vault \
  --name know-your-customer-com-sandbox --value "$VAL" --output none
unset VAL
```

**No restart is required.** The credential does not arrive through the Spring Key Vault property
source. `AzureSecretProvider` calls the Azure SDK `SecretClient` at request time, and
`KycComOAuthClient.ensureCredentials()` resolves lazily on the first `getToken()`, assigning its
fields only after validation — so a prior failure cached nothing. The next vendor call picks the new
secret up.

---

## 2. Each app reads its own vault

This is the correction that matters. The earlier version read the three profile files, found that all
three name `https://betterco-dev.vault.azure.net/`, and concluded that dev, staging and production
share one vault named after dev — and therefore that `bc-stg-vault`, referenced by no profile, was a
red herring and writing to it "would change nothing".

Every App Service overrides both the profile and the endpoint. The settings exist in **dotted
lowercase**, which is why a search for `SPRING_PROFILES_ACTIVE` and
`SPRING_CLOUD_AZURE_KEYVAULT_SECRET_ENDPOINT` found nothing:

| App | `spring.profiles.active` | `spring.cloud.azure.keyvault.secret.endpoint` |
|---|---|---|
| `bc-dev-be` | `azure, development` | `https://bc-dev-vault-dev.vault.azure.net/` |
| `bc-stg-be` | `azure, staging` | **`https://bc-stg-vault.vault.azure.net/`** |
| `bc-app-be` | `azure, production` | `https://bc-app-vault.vault.azure.net/` |

Two consequences follow. The vendor target **is** changeable without a redeploy, since both settings
are App Settings — the earlier "it comes from the image" is wrong in the reassuring direction. And
the `azure` profile, which is what defines `secrets.provider=azure` at all, carries its own endpoint
(`application-azure.properties:12`), so the profile files alone never decided the vault.

The KYC secrets as they now stand:

| Vault | `know-your-customer-com` | `-sandbox` | `-user` |
|---|---|---|---|
| `bc-dev-vault-dev` | ✓ | ✓ | ✓ |
| `bc-stg-vault` | ✓ | ✓ **(new)** | ✓ |
| `bc-app-vault` | ✓ 2026-07-14 | ✓ (inert — production reads the base name) | ✓ |
| `BETTERCO-DEV` | — | — | — |

`BETTERCO-DEV` exists and holds other secrets, but no `know-your-customer-*` entry and no deployment
points at it. The stray `-sandbox` entry in the production vault is harmless for the same reason the
production profile keeps the base name, but it is the kind of leftover that makes a future listing
ambiguous.

---

## 3. Three of the four original asks were already satisfied

| # | Original ask | Finding |
|---|---|---|
| 1 | Create the sandbox secret | Done — §1. Target vault was `bc-stg-vault`, not `BETTERCO-DEV`. |
| 2 | Confirm the production secret exists | It does: `bc-app-vault`, enabled, 2026-07-14. |
| 3 | Confirm the app identity has `get` | Already granted: `bc-stg-app` holds `Get,List,Purge` on `bc-stg-vault`, `bc-app-app` the same on `bc-app-vault`. RBAC is off on all three vaults; these are access policies. |
| 4 | Say whether a restart is needed | No — §1. |

Two further claims in the earlier version do not hold. The three apps use **three distinct service
principals** (`bc-dev-app`, `bc-stg-app`, `bc-app-app`), so staging and production do not share
rights. And the work needed no external owner: `AZURE_DEV_ADMIN` holds `Get,Set` on all three
vaults, and we are in it.

The credential source named there, `betterco-worldwide/.env.sandbox`, **does not exist**. No KYC.com
credential is in `.env` or `.env.stg-backup-2026-09-07` either. The vault-to-vault copy in §1 is the
route that works.

---

## 4. The billed world is decided by the base url, not by the secret name

The earlier version warned that storing the live credential under the `-sandbox` name would turn
every customer test order into a real order at $19–$119. The warning is good hygiene and the
mechanism is wrong, which matters because a wrong mechanism sends the next person looking in the
wrong place.

`KycVendorTargetResolver` derives the world from `kyc-com.base-url`: a host containing
`knowyourcustomer.dev` is SANDBOX, anything else is PRODUCTION. The secret name is not an input. A
live credential stored under the sandbox name would simply fail to authenticate against the sandbox
token endpoint; it would not redirect orders to the paying host.

The path that does cost money — repointing staging's `base-url` at `api.knowyourcustomer.com` — is
now loud rather than silent. `KycOrderingSafetyCheck` refuses to start any instance where
`kyc-com.create-enabled=true` resolves to the PRODUCTION world without the `production` profile
active, and names every input in the failure message.

---

## 5. Verified config, unchanged from the earlier reading

Confirmed against `origin/dev` at `3a3345605`, not only the stale shared checkout at `05f5b307b`
that the earlier version read.

| Profile | Vendor base-url | Secret name | Ordering armed |
|---|---|---|---|
| base `application.properties` | `api.knowyourcustomer.com` — **LIVE** | `know-your-customer-com` | `create-enabled=false` |
| `development` | `api.knowyourcustomer.dev` — sandbox | `know-your-customer-com-sandbox` | **`true`** |
| `staging` | `api.knowyourcustomer.dev` — sandbox | `know-your-customer-com-sandbox` | **`true`** |
| `production` | inherits **LIVE** from base | inherits `know-your-customer-com` | **`true`** |

The live vendor remains the default and the sandbox only an override, so a jar started without its
profile still talks to the paying vendor — which is what the startup guard in §4 exists to catch.

The secret's value shape, from `KycComOAuthClient`:

```json
{"clientId":"...","secret":"..."}
```

It is parsed into a two-field record and validated **only** for non-blank. A placeholder therefore
passes validation, boots clean and fails at the vendor, which is worse than an absent secret because
every listing then shows the entry as present.

---

## 6. The verification that proves it, and it is not a vault read

A company search for a British company on staging must return the five sandbox fixtures, with
`CROPWELL BISHOP CREAMERY LIMITED | 00364890` first.

**If it returns real Companies House rows, stop.** Staging is on the live vendor, and every order
placed there is billable. Revert before anyone tests.

---

## 7. What is still not established

- **The verification in §6 has not been run.** Everything in this document is config, source and
  Azure metadata. No vendor call and no application start went into it.
- **What is deployed on staging and production.** The images are `bc-backend:bc-stg`
  (sha256:148e9f0a…, pushed 2026-09-17 16:54 UTC) and `bc-backend:bc-app` (sha256:9244995e…, 17:08
  UTC). Recent enough that the aggregator is very likely on both, but the tags are mutable and this
  is inference, not a reading.
- **Whether ordering is live on production.** Config says yes: the production profile carries
  `create-enabled=true` against the live vendor, and the startup guard passes that combination with
  a warning by design. If the aggregator is deployed there, ordering is armed.
