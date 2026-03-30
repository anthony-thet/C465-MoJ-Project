## Client / User
### Events
- Successful Joke Submission
  - Data Fields: timestamp, user_id, joke_id
  - Reason: Provides a receipt for user and verifies succesful data persistence
  - Log Level: INFO
  - Risk: If absent, no way to to varify a joke exists or was created
- Rating Submission
  - Data Fields: timestamp, user_id, joke_id, dimension, score
  - Reason: Logs the specific impact of a user on the three-dimensional rating
  - Log Level: DEBUG
  - Risk: WIthout these logs, we would not be able to recalculate scores when a user requests deletion
- Account Deletion Initiation
  - Data Fields: timestamp, user_id, request, content_count
  - Reason: Provides a trigger for the right to delete and records the start of the deletion process
  - Log Level: WARNING
  - Risk: If this event wasn't logged, we could not prove that we abided by data deletion and privacy laws
- Content Moderation Flag
  - Data Fields: timestamp, joke_id, report_id, reason_category
  - Reason: Records why a joke was hidden or deleted which is necessary for transparency and regulation for explaining issues to corresponding teller
  - Log Level: WARNIN G
  - Risk: Users could feel silenced or targetted if we did not have these logged reasons on why a joke was removed or hidden
- Profile Information Change
  - Data Fields: timestamp, user_id, field_changed, request_ip
  - Reason: Tracks when information for an account is modified and allows a user to revirew their own account change activity and prevent unauthorized changes
  - Log Level: INFO
  - Risk: If someone were to change a user's email to steal their account, if we did not have this log we would have no evidence to reclaim the account
### Tools
Gemini

## Operational
### Events
- Log/Event Title
  - Data Fields:
  - Reason:
  - Log Level:
  - Risk:
### Tools


## Support / Helpdesk
### Events
- Request received
  - Data Fields: timestamp, request_id/correlation_id, HTTP method, route, authenticated user ID or anonymous, user role, source IP, user agent
  - Reason: This gives support the basic context needed to trace a user’s issue through the app.
  - Log Level: INFO
  - Risk: Without it, support may not be able to identify which request caused the problem.
- Failed login attempt
  - Data Fields: timestamp, request_id, username attempted, source IP, outcome, internal failure reason (unknown user, wrong password, locked account)
  - Reason: This helps support diagnose account access issues and spot suspicious login activity.
  - Log Level: WARNING
  - Risk: Without it, the team may miss brute-force attempts or be unable to explain why users cannot log in.
- Authorization denied on protected route
  - Data Fields: timestamp, request_id, user ID or anonymous, user role, route, method, required role/permission, response status
  - Reason: This helps support see why a user was blocked from a protected page or action.
  - Log Level: WARNING
  - Risk: Without it, support cannot easily tell whether access failed because of role, login state, or a bug.
- Input validation failure
  - Data Fields: timestamp, request_id, user ID, route, field name, validation rule violated, safe summary of bad input, response status
  - Reason: This helps support quickly identify why a request was rejected.
  - Log Level: INFO
  - Risk: Without it, support may not know whether a 400 error came from bad input or a client-side issue.
- Unhandled server exception
  - Data Fields: timestamp, request_id, user ID, route, method, exception type, stack trace, app version/commit hash, hostname
  - Reason: This gives developers and support the details needed to investigate a server failure.
  - Log Level: ERROR
  - Risk: Without it, 500 errors may happen with no clear record of what broke or where.
### Tools
ChatGPT

## Regulatory / Compliance
### Events
- Successful Login Attempt
  - Data Fields: timestamp, IP address, user_id
  - Reason: Keep a log of account access.
  - Log Level: INFO
  - Risk: If an attacker gets into an account but there is no log of where the login was from, it may be impossible to detect the account has been hacked into or to remove the intruder.

- Failed Login Attempt
  - Data Fields: timestamp, attempted_username, attempted_password, failure reason, IP
  - Reason: help to identify suspicious activity and brute force attacks
  - Log Level: WARNING
  - Risk: without this, a brute force attack could be done with tons of failed attempts to login to an account, but there would not be any record of this pattern, letting it go by undetected.
 
- Data Retention Deletion
  - Data Fields: data_type, records deleted, timestamp, retention period
  - Reason: Show that user data is not kept longer than allowed, showing compliance with retention policy
  - Log Level: INFO
  - Risk: if user data is store indefinitely or the organization cannot prove compliance with retention policies, they could face legal penalties or  additional issues in the case of a data breach.

- Data Update
  - Data Fields: user_id, new data, old data, timestamp, IP
  - Reason: keep a record of changes to user data in case this needs to be reviewed or reverted
  - Log Level:INFO or WARNING
  - Risk: If data is altered without a record of the changes, it may be hard to restore the correct data or investigate the changes.
 
- User Data Access
  - Data Fields: timestamp, user_id for person accessing data, user_id for the target, data accessed
  - Reason: maintain a record of access for user data to keep up accountability and regulatory compliance.
  - Log Level: INFO
  - Risk: If a user accesses another user’s private data (like their email or something), but there is no record of who accessed it, this could hinder investigation into the issue and violate accountability requirement
 
- GDPR Erasure Request
  - Data Fields: timestamp, user_id, request, content_count
  - Reason: Comply with the right to erasure, allowing content or accounts to be removed from the application.
  - Log Level: INFO
  - Risk: If this is not logged, we could face legal penalties as we are unable to prove that we are abiding by GDPR Compliance
### Tools
chatGPT

---
# Section 1: Individual Summaries
- `@coolds`
  - Dimension: Client / User
  - Recommended Log Events: Profile Information Change, Successful Joke Submission, Account Deletion Initiation
  - Insight: The key aspect of this dimension is keeping track of any changes a user makes to their account and ensures that we track said changes for support.
- `@kthet`
  - Dimension: Support / Helpdesk
  - Recommended Log Events: Request Received, Authorization Denied on Protected Route, Unhandled Server Exception
  - Insight: For support and helpdesk work, the most valuable logs are the ones that make it easy to reconstruct a user’s experience from start to finish. A support team usually needs to know what request the user made, whether the system denied it for a known reason, and whether the application itself failed. These events give enough context to troubleshoot common problems like access issues, bad requests, and server errors without guessing.
- `@maklsmit`
  - Dimension:
  - Recommended Log Events:
  - Insight: 
- `@lsiverts`
  - Dimension:
  - Recommended Log Events:
  - Insight: 
- `@amatariy`
  - Dimension:
  - Recommended Log Events:
  - Insight:

# Section 2: Unified Logging Specification
| # | Event | Fields | Log Level | Dimension(s) | Priority |
|---|---------|-------------------|------|----------------|--------|
|   |   |   |   |   |   |

# Section 3: Conflicts and Resolutions

# Section 4: Synthesis Reflection

# Section 5: Team Member Information
- Cole Olds | `@coolds` | Client / User
- Lily Sivertson | `@lsiverts` |
- Makena Smith | `@maklsmit` |
- Amin Matariyeh | `@amatariy` |
- Anthony Thet | `@kthet` | Support / Helpdesk

# Ethical Challenge
