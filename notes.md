# Interview Stories

## Story 1 — API bug: 200 instead of 404

While testing the products API on fakestoreapi, I wrote a test
for GET /products/99999 expecting a 404 since the product
doesn't exist. The test failed — the API was returning 200
with a null body.

I didn't assume my test was wrong. I verified through three
channels: the test failure message, curl in the terminal, and
opening the URL directly in the browser. All three confirmed
the same thing — 200 with null.

I documented it as a bug in the test with a comment explaining
the business impact: a frontend that checks status codes to
handle errors would receive 200 and assume success, rendering
a blank product page with no error message shown to the user.
I updated the assertion to reflect actual behaviour and noted
it as a known bug.

What I learned: always verify through multiple channels before
deciding whether the test or the code is wrong. And always
document the business impact of a bug, not just the technical
detail.

## Story 2 — Cloudflare 403 blocking CI

My tests passed locally but failed in GitHub Actions with a
403 status code. The error was "Failed to fetch product
catalogue — assert 403 == 200".

I investigated by reading the CI logs carefully. The response
body said "Just a moment..." which is a Cloudflare challenge
page. I understood that GitHub Actions servers use known IP
ranges that Cloudflare identifies as automated traffic and
blocks.

The fix was migrating from fakestoreapi to DummyJSON which
is built specifically for developer tooling and allows
automation traffic. I also updated all response assertions
because DummyJSON wraps the products array inside a products
key with pagination metadata, whereas fakestoreapi returned
a plain array.

What I learned: tests passing locally but failing in CI almost
always means an environment difference. Always read the actual
error response, not just the status code. And always verify
that the APIs you depend on allow traffic from CI environments.

## Story 3 — fixture return type error

I updated my product_catalogue fixture to return response.json()
instead of the response object. My test immediately threw
AttributeError: list object has no attribute json.

I read the error carefully. The fixture was now returning a
Python list — the parsed product array. But my test was still
calling .json() on it as if it were a response object. The
fixture return type changed but the tests weren't updated.

The fix was updating every test that used the fixture to work
with the list directly instead of calling .json() on it. I
also learned that the SLA test cannot use a cached fixture
at all — it needs to make its own live API call to measure
real response time, because a cached response has an elapsed
time from when the fixture ran, not when the test ran.

What I learned: when you change what a fixture returns, you
must audit every test that uses it. And always distinguish
between data fixtures (return parsed data) and measurement
tests (must make their own live call).

## Key concepts I can explain

Fixtures: prerequisite setup shared across tests. Scope
controls how often setup runs — session means once per suite,
function means once per test.

Factory fixtures: return a callable instead of data, allowing
tests to pass dynamic arguments. Used when different tests
need the same endpoint with different parameters.

Flaky tests: tests that pass and fail inconsistently without
code changes. Caused by timing issues, network variability,
or shared state between tests. Fixed with explicit waits,
retry logic, and test isolation.

POM: locators and page actions live in page classes, not in
test files. When a UI element changes, you update one file
and all tests that use that page are fixed automatically.

AI validation vs hard assertions: hard assertions check exact
values. LLM validation checks semantic quality — whether data
makes sense in a business context. Useful for catching
realistic-looking but wrong data that passes all field checks.

## 1. Severity vs Priority

Severity is how serious the defect is from a technical/system impact perspective.
Priority is how urgently the defect should be fixed from a business perspective.

## 👉 In simple terms:

Severity = How bad is the problem?
Priority = How fast should we fix it?
Example (from your kind of Macrometa work)

## Suppose:

The UI button color is wrong → looks bad but system works
Severity: Low
Priority: High (if client-facing release)
The API returns incorrect data but UI is not yet using it
Severity: High (data issue is critical)
Priority: Medium (not impacting users immediately)

## 💡 Interview tip: Always show that severity = technical impact, priority = business decision.

## 2. Defect Life Cycle

The defect life cycle describes the stages a bug goes through from identification to closure.

## Typical stages:

New
Tester logs the defect
Assigned
Assigned to a developer
Open / In Progress
Developer starts working on it
Fixed
Developer resolves the issue
Retest
Tester verifies the fix
Closed
If working as expected
Reopened (if needed)
If issue still exists
Deferred / Rejected / Duplicate (optional cases)
Deferred → fix later
Rejected → not a bug
Duplicate → already reported

## 💡 Real-world note: In Agile teams (like yours), tools like Jira manage these statuses.

## 3. Smoke vs Sanity Testing

These two confuse a lot of people — here’s the clean difference.

Smoke Testing
Done on a new build
Checks if the application is stable enough for further testing
Covers critical functionalities only

## 👉 Example:

App launches
Login works
Main page loads

## ✔ Goal: “Is the build testable?”

Sanity Testing
Done after bug fixes or small changes
Checks if the specific functionality works correctly
Narrow and focused

## 👉 Example:

A login bug was fixed → test only login scenarios

## ✔ Goal: “Did the fix work without breaking related areas?”

## 🔥 Simple way to remember:

Smoke = Build verification (broad, shallow)
Sanity = Fix verification (narrow, deep)
