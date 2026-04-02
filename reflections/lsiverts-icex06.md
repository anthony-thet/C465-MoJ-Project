# Individual Security Audit — Lily Sivertson

## Finding
- **Bandit ID:** B105
- **Severity / Confidence:** Low/Medium
- **File and Line:** app/__init__.py:12
- **What bandit detected:** there is possibly a hard coded password.

## OWASP Traceability
- **OWASP Category:** A02: Cryptographic Failures
- **Why this category:** The A02 category focuses on instances where weak/ improper use of cryptography can lead to the exposure of sensitive data. This hardcoded key would fall into this category as it would make it easy for someone to gain access to the data if they were to find out the hardcoded key.

## Attacker Goal
- **What could an attacker do with this?** If an attacker has the hardcoded key then they could use it to impersonate/log in as other users by creating tokens/cookies will be accepted as valid by the system, allowing them to gain full administrative access. It could also allow the attacker to tamper with data or change things that they should not otherwise have access to.

## Proposed Fix
- **What code change would address this?** instead of hardcoding the secret key, store it in a secure secret manager and then retrieve it at runtime using authenticated access controls.
- **What is the tradeoff?** Security would be improved as it would be much harder for an attacker to gain access to the secret key, but this may add additional complexity to the program compared to a simple hardcoded key. It may also introduce a dependence on external services to manage the secret key.

## Reflection
- **Is this finding a real risk for MoJ, or a false positive?**  Yes, this could pose a real risk to MoJ. Since Flask uses symmetric encryption, someone gaining acccess to the secret key would be a serious issue since they would be able to both encrypt and decrpyt information with this. This could allow them to modify information they should not be able to, impersonate others, or access sensitive user data.
