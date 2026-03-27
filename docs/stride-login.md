# STRIDE Analysis: POST /login

| Threat | Attack Scenario | Current Mitigation | Gap? | OWASP Category |
|--------|----------------|-------------------|------|----------------|
| **S** — Spoofing | Attacker guesses credentials of a valid user | check_password validates | Yes, no lockout for multiple incorrect guesses or MFA | A07 - Identification and Authentication Failures |
| **T** — Tampering | Attacker modifies request to bypass checks | request.get_json() handles  | No, Flask-Login handles this | Outside OWASP selection |
| **R** — Repudiation | Teller claims they didn't do an action | None | Yes, no logging for actions taken by users or admins | Outside OWASP selections |
| **I** — Info Disclosure | Data leaked due to errors | Generic "Invalid Credentials" is used | Yes, data traffic is not encrypted | A02 - Cryptographic Failures |
| **D** — Denial of Service | Attacker floods /login with requests | None | Yes, no rate limiting | Outside OWASP selection |
| **E** — Elevation of Privilege | User gains admin privileges by modifiying data | current_user.role != 'admin' check | No, current implementation handles this but maybe add more layers to authentication | A01 - Broken Access Control |
