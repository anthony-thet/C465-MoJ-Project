# STRIDE Analysis: POST /login

| Threat | Attack Scenario | Current Mitigation | Gap? | OWASP Category |
|--------|----------------|-------------------|------|----------------|
| **S** — Spoofing | Attacker guesses credentials of a valid user | check_password validates |  |  |
| **T** — Tampering | Attacker modifies request to bypass checks | request.get_json() handles  |  |  |
| **R** — Repudiation | Teller claims they didn't do an action | None |  |  |
| **I** — Info Disclosure | Data leaked due to errors | Generic "Invalid Credentials" is used |  |  |
| **D** — Denial of Service | Attacker floods /login with requests | None |  |  |
| **E** — Elevation of Privilege | User gains admin privileges by modifiying data | current_user.role != 'admin' check |  |  |
