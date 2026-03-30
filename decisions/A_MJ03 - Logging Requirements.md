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
- Request Completed
  - Data Fields: timestamp, endpoint, method, status_code, response_time
  - Reason: Shows normal behavior of the app and helps track how endpoints like /jokes are being used and if they are slow
  - Log Level: INFO
  - Risk: Without this, we would not know how the system is performing or which endpoints are being used the most

- Request Validation Failure
  - Data Fields: timestamp, endpoint, method, error_code
  - Reason: Tracks bad input requests like missing or invalid fields so we can identify patterns or client issues
  - Log Level: WARNING
  - Risk: Without this, we would not know if users are consistently sending bad requests or if there is a frontend issue

- Server Error (Exception)
  - Data Fields: timestamp, endpoint, method, error_type
  - Reason: Helps identify when something breaks in the app and separates real system errors from user mistakes
  - Log Level: ERROR
  - Risk: Without this, we would not know what caused failures in the system or where they happened

- Database Initialization Failure
  - Data Fields: timestamp, database_uri, error_message
  - Reason: Ensures we know when the database fails to start since the app depends on it to function
  - Log Level: CRITICAL
  - Risk: Without this, the app could fail completely and we would not know why

- Database Operation Failure
  - Data Fields: timestamp, model_name, operation, error_message
  - Reason: Tracks failures when interacting with models like User and Joke
  - Log Level: ERROR
  - Risk: Without this, data issues would go unnoticed and could break features silently

- Service Start / Restart
  - Data Fields: timestamp, service_instance, status
  - Reason: Tracks when the app starts or restarts to help explain sudden issues
  - Log Level: INFO
  - Risk: Without this, it would be harder to connect failures to restarts or deployments

- Environment / Dependency Failure
  - Data Fields: timestamp, environment, dependency, error_message
  - Reason: Helps track issues caused by environment differences like CI runner problems
  - Log Level: ERROR
  - Risk: Without this, we would not know why something works on one machine but not another

- Slow Request or Query
  - Data Fields: timestamp, endpoint_or_query, duration, threshold
  - Reason: Identifies performance issues before they become bigger problems
  - Log Level: WARNING
  - Risk: Without this, slow performance could go unnoticed until it affects users

### Tools
ChatGPT


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
ChatGPT

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
  - Dimension:  Regulatory / Compliance
  - Recommended Log Events: failed login attempt, GDPR Erasure request, Data Access.
  - Insight: For this dimension, the main priority is complying with ethical and legal obligations. The GDPR erasure request would be important to this, to make sure that the program is abiding by the right to erasure. Data access allows to see when and what data that people are accessing, which is important in ensuring that people are not accessing data they should not be, or taking advantage of priveledges they may have to look up sensitive information. Finally, failed login attempt helps to identify and ideally slow down/prevent brute force attacks on accounts. Together these events help to log activity to make it easier to check for any unethical behaviors or legal issues.
- `@amatariy`
  - Dimension: Operational
  - Recommended Log Events: Request Completed, Database Initialization Failure, Environment / Dependency Failure
  - Insight: From our ICEX work, a lot of issues came from environment differences, database setup, and unexpected errors rather than just code bugs. Because of that, operational logging should focus on tracking requests, failures, and system behavior so we can quickly figure out what broke and where.

# Section 2: Unified Logging Specification
| # | Event | Fields | Log Level | Dimension(s) | Priority |
|---|---|---|---|---|---|
| 1 | Successful Login | timestamp, user_id, request_ip, user_agent | INFO - keeps track that a specific ip most likely belongs to a specific user | Regulatory, Client | High |
| 2 | Failed Login | timestamp, attempted_username, request_ip, failure_reason | WARNING - informs us that a certain ip is attempted to log in and could be suspicious | Regulatory, Support | High |
| 3 | Unhandled Exception | timestamp, request_id, user_id, route, stack_trace | ERROR - logged as an error to inform admins of it and for maintaing MoJ's uptime | Support, Operational | High |
| 4 | Joke Submission | timestamp, user_id, joke_id, status (Success/Fail) | INFO - purely informational and maintains the list of all accepted jokes | Client, Support | Medium |
| 5 | Rating Submission | timestamp, user_id, joke_id, dimension, score | DEBUG - allows us to identify why a joke has a specific score | Client | Low |
| 6 | Erasure Request | timestamp, user_id, request_type (Account/GDPR) | WARNING - informs admins that an erasure request was made and consolidate the information | Regulatory, Client | High |
| 7 | Profile Change | timestamp, user_id, field_changed, old/new value, IP | INFO - informs user and admins of changed information and a backlog of all changes | Regulatory, Client | Medium |
| 8 | Auth Denied | timestamp, request_id, user_id, route, required_role | WARNING - similar to failed login as it maintains security and logs suspicious behavior | Support, Security | Medium |
| 9 | Content Moderation | timestamp, joke_id, report_id, reason_category | WARNING - allows admins to identify why specific content was hidden or removed | Client, Regulatory | Medium |
| 10 | Internal Data Access | timestamp, accessor_id, target_user_id, scope | INFO - informs admins of requests for data access and its scope | Regulatory, Security | High |

# Section 3: Conflicts and Resolutions
**Conflict Identified:** The Failed Login event exists in both the Support and Regulatory dimensions. Support requires detailed logs for why the login failed so that we can help users get back into their accounts. Regulatory requires this data to be strictly controlled or encrypted so that we don't leak anything valuable to someone wishing to steal or access an account.

**Resolution:** We decided that for this specific log we would abide by both the support and regulatory dimension's logging requirements. This means that to the front end user we would only display a general authentication failed message so that they can not garner any specific information about their request. However, the back-end will still log the specific reason so that Support still has the data needed for any troubleshooting without creating any vulnerabilities.

# Section 4: Synthesis Reflection
The team discussion surfaced the need for a more unified hierarchy for requests or logs as a whole. In all of our own research we tended to focus on specifically what each dimension would need and so all the data was local. However, in actuality if we look at a dimension such as Support which is essentially where a lot of the logged events and gaps would be prevalent, we can realize that we need a more structured approach so that duplicate requests ids and identifiers would not appear. 

This specification and overall structure closes the gap in our STRIDE table by ensuring that every action taken by any user or admin can be tracked and identified. This means that a user can not deny they took an action and admins can not hide any unauthorized data access or deletion.

# Section 5: Team Member Information
- Cole Olds | `@coolds` | Client / User
- Lily Sivertson | `@lsiverts` | Regulatory / Compliance
- Makena Smith | `@maklsmit` |
- Amin Matariyeh | `@amatariy` | 
- Anthony Thet | `@kthet` | Support / Helpdesk

# Ethical Challenge
The line between security and surveillence in MoJ is drawn mostly clear when we look at the User Data Access log. Logging is for seucrity when it only tracks system events and prevents harm. However, this line can be very easily breached if those same logs are used to build a profile of a user and start identifying their habits and patterns. This log comes the closest to that line as it records exactly what user is looking at what data. In order to safeguard this specific log we should mask the user_id on these types of logs and any attempt to access the unmasked user_id should be tracked as well and logged. 
