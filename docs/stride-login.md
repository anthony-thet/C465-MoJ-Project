# STRIDE Analysis: POST /login

| Threat | Attack Scenario | Current Mitigation | Gap? | OWASP Category |
|--------|----------------|-------------------|------|----------------|
| **S** — Spoofing | Attacker guesses credentials of a valid user | check_password validates | Yes, no lockout for multiple incorrect guesses or MFA | A07:2025 - Authentication Failures |
| **T** — Tampering | Attacker modifies request to bypass checks | request.get_json() handles  | No, Flask-Login handles this | A08:2025 - Software or Data Integrity Failures |
| **R** — Repudiation | Teller claims they didn't do an action | None | Yes, no logging for actions taken by users or admins | A09:2025 - Security Logging and Alerting Failures |
| **I** — Info Disclosure | Data leaked due to errors | Generic "Invalid Credentials" is used | Yes, data traffic is not encrypted | A04:2025 - Cryptographic Failures |
| **D** — Denial of Service | Attacker floods /login with requests | None | Yes, no rate limiting | A02:2025 - Security Misconfiguration |
| **E** — Elevation of Privilege | User gains admin privileges by modifiying data | current_user.role != 'admin' check | No, current implementation handles this but maybe add more layers to authentication | A01:2025 - Broken Access Control |
