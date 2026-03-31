# ICEX_MJ01: Founding the Ministry
* **Date:** 2026-03-03
* **Team Members Present:** `@coolds`, `@lsiverts`, `@maklsmit`, `@amatariy`, `@kthet`
* **Roles:**
    * Repo Admin: `@kthet`
    * Process Lead: `@coolds`
    * Dev Lead: `@amatriy`, `@maklsmit`
    * QA Sentinel: `@lsiverts`
* **Summary of Work:** Established the MoJ Flask skeleton with GET /jokes and POST /jokes
  routes, wrote the first pytest test using GIVEN/WHEN/THEN format, and set up the
  Engineering Log repos for all team members.

* **Planted Problem:**
    * **What was the problem?**
       * Running pytest gave ModuleNotFoundError: No module named 'app', which meant pytest could not find the app package.
    * **How did the team identify it?**
       * Ran pytest tests/ -v and observed the import error on the first test.
    * **How was it resolved?**
       * Created an empty conftest.py in the root directory, which tells pytest to treat the root as the base directory, making the app module importable.

* **Forward hook:** Next session (ICEX_MJ02), your team's runners will have different
  operating systems. Before class, make sure every team member's self-hosted runner
  is installed and shows as **Idle** in the repo's runner list.
---
# ICEX_MJ02: The Silliness Detector
* **Date:** 2026-03-05
* **Team Members Present:** `@maklsmit`, `@lsiverts`, `@kthet`, `@amatariy`, `@coolds`
* **Roles:**
    * Repo Admin: `@lsiverts`
    * Process Lead: `@maklsmit`
    * Dev Lead: `@amatariy`, `@kthet`
    * QA Sentinel: `@coolds`
* **OS Inventory:**
    * `@maklsmit` — Windows 11
    * `@lsiverts` — Windows 11
    * `@kthet` — macOS 14.6.1
    * `@amatariy` — macOS 26.2
    * `@coolds` - Windows 11
* **Runner that picked up the first push:** `@kthet` (macOS)
* **Summary of Work:** Configured self-hosted runners on all team members' laptops,
  wired up the GitHub Actions CI workflow, diagnosed and fixed the heterogeneous
  environment problem.

* **Planted Problem:**
    * **What was the problem?**
       * The term 'pip' was not recognized as the name of a cmdlet, function, script file, or operable program.
    * **Which runners failed / which passed?** 
       * The runner coolds with Windows 11 failed. The runners AnthonyC365 with macOS 14.6.1 and maklsmit-Windows with Windows 11, passed.
    * **Diagnostic process:** 
       * Checked the test output and read through it to see that pip was not recognized.
    * **Fix applied:** 
       * Declared the python setup before the pip install. This fixes the problem because the python setup installs pip so that it will be recognized later to be able to install the requirements.

* **Forward hook:** Your CI pipeline now runs tests on every push. Next session
  (ICEX_MJ03), your data moves out of a Python list and into a real database.
  Think about what your CI pipeline will need to know about the database
  before the tests can run against it.
---
# ICEX_MJ03: The Official Ledgers
* **Date:** 2026-03-10
* **Team Members Present:** `@maklsmit`, `@lsiverts`, , `@amatariy`, `@coolds`
* **Roles:**
    * Repo Admin: `@coolds`
    * Process Lead: `@lsiverts`
    * Dev Lead: `@maklsmit`, 
    * QA Sentinel: `@amatariy`
* **Summary of Work:** Defined User and Joke SQLAlchemy models, wired the App Factory
  pattern with Flask-Migrate, initialized the database, and documented schema decisions
  including deliberate data capture choices for v1.

## Planted Problem
* **What was the problem?**
   * DB wasn't working from Models as it was never initalized fully at any point. 
* **How did the team identify it?**
   * There was an error in __init__ that db wasn't working from models. Later verification was from the test_db_init.py to ensure it was working as intended.
* **How was it resolved?**
   * We modified models.py to instead initalize its own instance of SQL Alchemy and then have db = SQLAlchemy()

## Forward Hook
Your schema is the foundation every future ICEX builds on. Next week (ICEX_MJ04),
you will write tests that verify this schema behaves correctly under valid input,
boundary conditions, and invalid input — at all three levels of the test taxonomy.
The decisions you documented today in `docs/schema.md` are the behaviors you will
be testing tomorrow.
---
# ICEX_MJ04: Upgrading the Detector
* **Date:** 2026-03-12
* **Team Members Present:** `@maklsmit`, `@lsiverts`, `@amatariy`, `@coolds`, `@kthet`
* **Roles:**
    * Repo Admin: `@maklsmit`
    * Process Lead: `@amatariy`
    * Dev Lead: `@coolds`, `@lsiverts`
    * QA Sentinel: `@kthet`
* **Summary of Work:** Added a parallel flake8 linting CI job; wrote a
  three-level test suite for POST /jokes using GIVEN/WHEN/THEN format;
  ran pytest --cov and observed coverage output.

## Planted Problem
* **What was the problem?**
  * Many files were failing to meet the lint standards.
* **How did the team identify it?**
  * Lint kept failing and checking the CI logs for flake8 shows all the errors.
* **How was it resolved?**
  * Went through the repository and reformatted files to flake8's liking.

## Coverage Output
| Name | Stmts | Miss | Cover | Missing |
|---|---|---|---|---|
| app/__init__.py | 11 | 0 | 100% | |
| app/models.py | 19 | 2 | 89% | 17, 28 |
| app/routes/jokes.py | 14 | 0 | 100% | |
|---|---|---|---|---|
| TOTAL |44 | 2 | 95% |

## Individual Extension Route Assignments
| Team Member | Claimed Route / Function |
|---|---|
| `@kthet` | test_submit_joke_whitespace_only |
| `@maklsmit` | test_submit_joke_over_max_length |
| `@lsiverts` | test_submit_joke_empty_text |
| `@coolds` | test_submit_joke_max_length |
| `@amatariy` | test_submit_joke_valid |

## Forward Hook
* Your test suite now specifies what POST /jokes should do — at every level.
Next week (Cycle 1 Close), your team will assess the health of the full
test suite across all routes. The gap between what you tested today and
what the full app does is the gap you will document in the Test Health block.
Start thinking now: which routes have no tests at all?
---
# Cycle 1 Close — moj-c1-v1.0
* **Date:** 2026-03-23
* **Team Members:** `@maklsmit`, `@lsiverts`, `@kthet`, `@amatariy`, `@coolds`
* **Summary:** Team has begun working on the MoJ and have built the foundation for the entire system. We now have a running flask application with a CI pipeline that ensures that all changes still work as intended and pass linter tests. Jokes.py can now handle the edge cases as listed. 
* **Complexity Horizon:** Our MVP does not yet meet the standard 99.5% uptime and is in fact not fully operational and ready to handle users.
---
# ICEX 5: Joke-Teller Licenses
* **Date:** 2026-03-24
* **Team Members Present:** `@maklsmit`, `@lsiverts`, `@kthet`, `@amatariy`, `@coolds`
* **Roles:**
    * Repo Admin: `@coolds`
    * Process Lead: `@lsiverts` 
    * Dev Lead: `@kthet`, `@amatariy`
    * QA Sentinel: `@maklsmit`
* **Summary of Work:** Implemented a role based security system using Flask logins to log users and ensure that users can login, logout, and register themselves. Also has an extensive test plan toe ensure users can register as needed and that users besides admin can not see admin users.

### Planted Problem
* **What was the bug?** The issue wouldn't be an issue for a joke teller specifically but if the user was not logged in and instead an Anonyomous user and so the code didn't return the correct error. 
* **How did the team identify it?** There was a specific test that tested if a person of joketeller role could acquire the list of admin users: 'test_admin_access_forbidden_for_teller'
* **How was it resolved?** Added a @login_required block above the specific admin block to ensure the user is logged in and has a role so that the '!= admin' would work as intended.

* **Forward Hook:** Next time, we meet the attacker. ICEX 6 applies STRIDE to the
  endpoints you just built — every route you wrote today becomes an attack surface
  to enumerate and harden.
---
# ICEX 6: Forging Unforgeable Licenses
* **Date:** 2026-03-26
* **Team Members Present:** `@kthet`, `@lsiverts`, `@coolds`, `@maklsmit`, `@amatariy`
* **Roles:**
    * Repo Admin: `@maklsmit`
    * Process Lead: `@kthet`
    * Dev Lead: `@lsiverts`, `@amatariy`
    * QA Sentinel: `@coolds`
* **Summary of Work:** We installed a much needed security check into our system. This security check runs our currently installed requirements and audits them using pip-audit to ensure there are widely known security issues. We also addressed the STRIDE table and document each category of stride and it's importance and reference to our MoJ. Also for the hardening issue we deduced the non-repudiation and DoS gap to be the most substantial issues and has depicted by the assignment description have made issues reflecting this decision.

### Planted Problem
* **What was the bug?** There were two issues. First is that python was not setup before installing and running pip-audit in the security job. The second was that pip-audit was auditing the local packages and not specifically the dependencies we cared about in requirements.txt.
* **How did the team identify it?** The runner was passing the security check but not actually running pip audit on the requirements.
* **How was it resolved?** We set up python before installing pip-audit. We ran "pip-audit -r requirements.txt" and we removed the || operator and instead added the line "continue-on-error: true". 

* **Forward Hook:** Next time, MoJ gets an opinion system. ICEX 7 adds three-axis
  attributed ratings — funniness, appropriateness, and originality. Every threat in
  your STRIDE table applies to the rating endpoints too. The security issues you
  opened today are the backlog you carry into feature development.
---
# ICEX 7: The Department of Conditions and Alarm
* **Date:** 2026-03-31
* **Team Members Present:** `@lsiverts`, `@coolds`, `@maklsmit`, `@amatariy`
* **Roles:**
    * Repo Admin: `@userX`
    * Process Lead: `@userY`
    * Dev Lead: `@userZ`
    * QA Sentinel: `@userW`
* **Summary of Work:** [1-2 sentences on what was accomplished]

### Planted Problem (either one)
* **What was the bug?** [Describe the omission in the starter model]
* **What was the consequence?** [What behavior did tests reveal without the fix?]
* **How was it resolved?** [What was added and why does it matter?]

### Security Carry-Forward
* **STRIDE threat 1 from ICEX 6 that applies to ratings:** [Threat name + 1-2 sentence explanation of how it applies to the rating endpoints]
* **STRIDE threat 2 from ICEX 6 that applies to ratings:** [Threat name + 1-2 sentence explanation]

* **Evidence & Reflection:** The POST endpoint is non-idempotent and the PUT endpoint is idempotent. In one sentence: what would break in MoJ's user experience if both were non-idempotent (both POST)?
