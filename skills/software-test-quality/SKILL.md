---
name: software-test-quality
description: "Review software test suites and choose test levels. Use when auditing unit, integration, component, or end-to-end tests; assessing assertions, fixtures, mocks, coverage, or flakiness; or deciding which test level best protects a behavior or risk."
metadata:
  author: nweii
  version: "1.0.0"
  credit: "Uses Kent Beck's Test Desiderata (testdesiderata.com) via Lex-Inc/roughdraft and benomahony/testdesiderata."
---

# Software test quality

Choose the branch that matches the task:

- Existing tests or suite → Review test quality
- Proposed behavior or risk → Choose the test level

Use the `tdd` skill instead when building a feature or fixing a bug test-first.

## Review test quality

Review tests through their public seam: the interface where callers observe behavior. A test should fail when that behavior breaks and survive internal refactors that preserve it.

Apply the Desiderata as design lenses, not a checklist:

- Isolated: results do not depend on execution order or shared mutable state.
- Composable: tests combine without hidden coupling or cascading setup.
- Deterministic: unchanged code and inputs produce the same result.
- Fast: tests are quick enough to run while working.
- Writable: creation cost is proportionate to the behavior protected.
- Readable: motivation and expected behavior are clear.
- Behavioral: the result changes when the behavior changes.
- Structure-insensitive: internal refactors do not change the result.
- Automated: tests run without manual intervention.
- Specific: failures make the likely cause clear.
- Predictive: passing gives justified confidence in production behavior.
- Inspiring: the suite increases confidence instead of creating noise, flakes, or avoidance.

Then inspect the failure modes that a structural review can miss:

- Weak assertions that prove existence instead of behavior.
- Fixtures that do not represent production inputs.
- Risky paths that the suite never exercises.
- Names that disagree with the behavior asserted.
- Mocks that encode assumptions the real collaborator does not satisfy.
- Tautological expectations derived through the same logic as the implementation.

When a test's sensitivity is uncertain and a controlled check is cheap, break the protected behavior minimally and confirm that the test fails for the expected reason. Restore the behavior before continuing.

Report every material weakness, the behavior or risk it affects, and any intentional Desiderata tradeoff. The review is complete when every in-scope test has been assessed and each finding identifies concrete evidence.

## Choose the test level

1. State the behavior or risk to protect in one sentence.
2. Identify the public seam where that behavior can be observed.
3. Choose the fastest level that remains predictive of production behavior.
4. Escalate from unit to integration, component, or end-to-end only when the boundary itself carries the risk.

For local UI interaction logic, prefer a component test. Use browser end-to-end coverage when the browser, file system, server, navigation, or cross-view interaction is the product risk. Use snapshots or DOM-structure assertions only when rendered structure is the public contract.

The choice is complete when it names the protected risk, seam, test level, and why a cheaper level would not be predictive enough.
