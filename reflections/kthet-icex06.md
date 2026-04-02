# Individual Security Audit — Anthony Thet

## Finding
- **Bandit ID:** B105
- **Severity / Confidence:** Low / Medium
- **File and Line:** app/__init__.py:12:15
- **What bandit detected:** A hardcoded key for app.config['SECRET_KEY']

## OWASP Traceability
- **OWASP Category:** A02
- **Why this category:** Maps to A02 because the application uses a hardcoded key. OWASP describes this category as including insecure default settings and improperly secured configurations, which this hardcoded key falls into.

## Attacker Goal
- **What could an attacker do with this?** There is a spoofing and tampering risk involved as if an attacker knows the hardcoded key, they can create or alter cookies and send it in a request to the app. The attacker could spoof another user's identity or tamper with things and have unauthorized access. 

## Proposed Fix
- **What code change would address this?** Replace the hardcoded secret key with a value loaded from an environment variable.
- **What is the tradeoff?** There's not much of a tradeoff. You just have to manage an environment variable and prevent misconfigurations.

## Reflection
- **Is this finding a real risk for MoJ, or a false positive?** Considering the scale of the system serving 600,000 registered users, a hardcoded key would be a real risk. Attackers can impersonate users and moderators and have access to data they shouldn't have. The vision for MOJ includes rotating keys in its security model.