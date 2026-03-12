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
   * The application threw a Runtime Error because both db and app were dependent on one another while neither were fully initalized . 
* **How did the team identify it?**
   * We ran the tests, specifically the test_db_init.py tests. 
* **How was it resolved?**
   * We modified models.py to instead initalize its own instance of SQL Alchemy and then have db = SQLAlchemy()

## Forward Hook
Your schema is the foundation every future ICEX builds on. Next week (ICEX_MJ04),
you will write tests that verify this schema behaves correctly under valid input,
boundary conditions, and invalid input — at all three levels of the test taxonomy.
The decisions you documented today in `docs/schema.md` are the behaviors you will
be testing tomorrow.
