# Individual Security Audit — maklsmit

## Finding
- **Bandit ID:** B105
- **Severity / Confidence:** LOW/MEDIUM
- **File and Line:** app/__init__.py:12
- **What bandit detected:** A hard-coded password exists. 

## OWASP Traceability
- **OWASP Category:** A02 Cryptographic Failures
- **Why this category:** This category covers instances of failing to prevent the exposure of sensitive data. Using a simple hard-coded key makes it easier for someone to guess the key and use it to access or modify data, thus causing a cryptographic failure.

## Attacker Goal
- **What could an attacker do with this?** If an attacker can guess the secret key, than can pretend to be a user with a session to send packets that the server would accept since the session would be seen as valid. This could also bring the attacker closer to accessing the database and other user data since the secret key is vital to security with Flask.

## Proposed Fix
- **What code change would address this?** Instead of a simple secret key, we could create a randomized key by importing secrets and using secrets.token_hex(24) to make a difficult hex. Then, we can either have our secret key be set to this token or setup a config file to try to keep it more secured. 

- **What is the tradeoff?** It would improve security since it would be a lot harder for someone to guess the secret key, but bandit might still flag it since it is hard-coded.

## Reflection
- **Is this finding a real risk for MoJ, or a false positive?** This is a real risk, but not for what bandit flagged it for. Since Flask uses the secret key for encryption and decryption, having a simple secret key that could be easy to guess puts the program and database at risk to an attack. The attacker would be able to pose as a valid user and modify data or even access sensitive user data.