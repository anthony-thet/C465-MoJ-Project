#### ICEX_MJ01: Founding the Ministry
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
