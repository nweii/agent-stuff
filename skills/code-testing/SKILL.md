---
name: code-testing
description: "Plan, write, review, and maintain software tests. Use when building features or fixing bugs test-first with a red-green loop, writing or rewriting unit/integration/e2e tests, reviewing or auditing test quality, choosing what level of test to write, working with mocks and fixtures, or keeping an existing suite in mind while making code changes."
metadata:
  author: nweii
  version: "1.0.0"
  credit: "Based on Matt Pocock's tdd skill (mattpocock/skills), with verification discipline from obra/superpowers and Kent Beck's Test Desiderata (testdesiderata.com) via Lex-Inc/roughdraft and benomahony/testdesiderata."
---

# Code testing

Three modes. Pick by task:

- **Building or fixing** → Test-first loop
- **Reviewing or auditing existing tests** → Desiderata review
- **Deciding strategy or test level** → Choosing the test level

All three share the same philosophy.

## Philosophy

**Core principle**: Tests should verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't.

**Good tests** are integration-style: they exercise real code paths through public APIs. They describe _what_ the system does, not _how_ it does it. A good test reads like a specification — "user can checkout with valid cart" tells you exactly what capability exists. These tests survive refactors because they don't care about internal structure.

**Bad tests** are coupled to implementation. They mock internal collaborators, test private methods, or verify through external means (like querying a database directly instead of using the interface). The warning sign: your test breaks when you refactor, but behavior hasn't changed. If you rename an internal function and tests fail, those tests were testing implementation, not behavior.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## Test-first loop

### 1. Planning

Before writing any code:

- Confirm with user what interface changes are needed
- Confirm with user which behaviors to test (prioritize)
- Identify opportunities for [deep modules](deep-modules.md) (small interface, deep implementation)
- Design interfaces for [testability](interface-design.md)
- List the behaviors to test (not implementation steps)
- Get user approval on the plan

Ask: "What should the public interface look like? Which behaviors are most important to test?"

**You can't test everything.** Confirm with the user exactly which behaviors matter most. Focus testing effort on critical paths and complex logic, not every possible edge case.

### 2. Tracer bullet

Write ONE test that confirms ONE thing about the system:

```
RED:   Write test for first behavior → test fails
GREEN: Write minimal code to pass → test passes
```

This is your tracer bullet — proves the path works end-to-end.

**Verify RED before writing code.** Run the test and confirm it fails *for the expected reason* — the feature is missing, not a typo or import error. A test that errors instead of failing, or fails for the wrong reason, proves nothing about what it protects. A test that passes immediately is testing existing behavior; fix the test.

### 3. Incremental loop

For each remaining behavior:

```
RED:   Write next test → fails
GREEN: Minimal code to pass → passes
```

Rules:

- One test at a time
- Only enough code to pass current test
- Don't anticipate future tests
- Keep tests focused on observable behavior

**Verify GREEN properly.** The new test passes, the rest of the suite still passes, and the output is pristine — no stray errors or warnings. If another test broke, fix it now.

### 4. Refactor

After all tests pass, look for [refactor candidates](refactoring.md):

- [ ] Extract duplication
- [ ] Deepen modules (move complexity behind simple interfaces)
- [ ] Apply SOLID principles where natural
- [ ] Consider what new code reveals about existing code
- [ ] Run tests after each refactor step

**Never refactor while RED.** Get to GREEN first.

### Anti-pattern: horizontal slices

**DO NOT write all tests first, then all implementation.** This is "horizontal slicing" — treating RED as "write all tests" and GREEN as "write all code."

This produces crap tests:

- Tests written in bulk test _imagined_ behavior, not _actual_ behavior
- You end up testing the _shape_ of things (data structures, function signatures) rather than user-facing behavior
- Tests become insensitive to real changes — they pass when behavior breaks, fail when behavior is fine

**Correct approach**: Vertical slices via tracer bullets. One test → one implementation → repeat. Each test responds to what you learned from the previous cycle.

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical):
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  ...
```

### Bug fixes

Reproduce the bug with the smallest failing behavioral test before implementing the fix. The test proves the fix and prevents regression.

## Desiderata

Use Kent Beck's test properties as design lenses (not a rigid checklist), so that you can make explicit tradeoffs among valuable properties.

- Isolated: test results should not depend on execution order or shared mutable state.
- Composable: independently valuable tests should combine without hidden coupling or cascading setup requirements.
- Deterministic: unchanged code and inputs should produce the same result every run.
- Fast: tests should be quick enough that agents and humans will run them while working.
- Writable: tests should be cheap to create relative to the behavior protected.
- Readable: tests should make their motivation and expected behavior clear to the next maintainer.
- Behavioral: tests should change result when the behavior under test changes.
- Structure-insensitive: tests should survive internal refactors that preserve behavior.
- Automated: tests should run without manual intervention.
- Specific: failures should make the likely cause obvious.
- Predictive: passing tests should give justified confidence that production behavior is acceptable.
- Inspiring: the suite should increase confidence, not create noise, flakes, or avoidance.

### Reviewing existing tests

Apply the desiderata above, then check for the failure modes that survive checklist review. A test can satisfy every desideratum structurally and still be worthless:

- Weak assertions: `assert response is not None` passes but protects almost nothing. Assert on the behavior, not on existence.
- Wrong test data: hardcoded values that happen to pass but do not represent real usage. Ask whether the fixture resembles production input.
- Missing coverage: a green suite says nothing about the branches it never exercises. Name the untested paths when they carry real risk.
- Misleading test names: a test named for one behavior that actually exercises another. Verify the name matches the assertion.
- Over-specified mocks: mocks that technically follow the API while encoding wrong assumptions about the collaborator. Prefer real collaborators when cheap; verify mock contracts against the real interface when not.

### Tradeoffs

When a test intentionally sacrifices one desideratum for another, make that explicit in a short comment or final summary. Common acceptable tradeoffs:

- Slower e2e coverage for a critical file-system or browser integration path.
- A slightly larger fixture when readability and production similarity matter more than minimal setup.
- Multiple focused tests instead of one broad test when specificity and determinism matter more than brevity.

## Choosing the test level

1. State the behavior or risk the test must protect in one sentence before choosing the level.
2. Choose the fastest test level that remains predictive of production behavior. Escalate from pure unit tests to integration or e2e tests only when the boundary itself is the behavior under test.
3. For UI behavior, prefer component tests for local interaction logic; reach for browser e2e only when browser, file, server, or cross-view behavior is the product risk.
4. Avoid snapshot-heavy or DOM-structure-heavy assertions unless the rendered structure itself is the public contract.
5. Run the narrow relevant command first, then the broader package or repo command when the change is broad enough to justify it.

## When stuck

| Problem | Solution |
|---------|----------|
| Don't know how to test | Write wished-for API. Write assertion first. Ask your human partner. |
| Test too complicated | Design too complicated. Simplify interface. |
| Must mock everything | Code too coupled. Use dependency injection. |
| Test setup huge | Extract helpers. Still complex? Simplify design. |
