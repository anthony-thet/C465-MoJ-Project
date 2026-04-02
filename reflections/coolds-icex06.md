# Individual Security Audit — Cole Olds

## OWASP Category Finding
- **OWASP Category:** A01 - Broken Access Control 
- **Severity:** High
- **File and Line:** app/routes/auth.py:50
- **Risk description:** Bandit didn't detect anything here but this could be a risk for A01

## OWASP Traceability
- **OWASP Category:** A01 - Broken Access Control
- **Why this category:** If this @login_required code section was not included in this section then a user may be able to gain information to the admin users and gain access through other vulnerabilities such as spoofing. 

## Attacker Goal
- **What could an attacker do with this?** As stated above, if this vulnerability remained a user could acquire a list of admin privileged users. Then after gaining access to this user list they could begin spoofing and attempting to gain access to the admin users through other vulnerabilities within our system. Mainly the lack of MFA or lockout protocols. 

## Proposed Fix
- **What code change would address this?** Included an @login_required code segment to ensure a user must be logged in and thus can only be a joke-teller or an already admin privilged user. 
- **What is the tradeoff?** This fixes the issue completely. The only way now for a user to gain the list of admin users is for they themselves to already be admin authorized user. The only other role that could attmept to run this command would but any role besides admin is cateogrically unable to run said command. 

## Reflection
- **Is this finding a real risk for MoJ, or a false positive?** This would have been a major risk factor without the changes to the codebase. However, with the additon of the code segment and so long as we continue to ensure a user is logged in for any similar admin privilege calls then the risk is mitigated completely. If we were to not include this line then there is a certain risk involved that comes along with it that if some role is not strictly prohibitied such as an anonyomous user they may be able to gain access to information they shouldn't be able to gather. 
