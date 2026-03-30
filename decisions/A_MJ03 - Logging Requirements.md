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
- Log/Event Title
  - Data Fields:
  - Reason:
  - Log Level:
  - Risk:
### Tools


## Regulatory / Compliance
### Events
- Log/Event Title
  - Data Fields:
  - Reason:
  - Log Level:
  - Risk:
### Tools
---
# Section 1: Individual Summaries
- `@coolds`
  - Dimension: Client / User
  - Recommended Log Events:
  - Insight: 
- `@kthet`
  - Dimension:
  - Recommended Log Events:
  - Insight: 
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
- Anthony Thet | `@kthet` |

# Ethical Challenge
