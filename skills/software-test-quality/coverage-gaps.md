# Cover meaningful gaps

Inspect the requested recent changes against existing tests. Establish the comparison range from the task or repository history, and prioritize new untested behavior, production-only bug fixes, parsing, concurrency, permissions, validation, shared utilities, and core flows.

For each candidate, state the regression risk and observable seam. Choose the smallest deterministic test set that would fail if the protected behavior broke, using the test-level guidance in the entrypoint and existing fixtures and conventions. Cosmetic changes and tests that merely restate implementation do not warrant coverage by themselves.

Add tests within the authorized scope. Keep production behavior unchanged; propose a required testability change when it exceeds that scope. When practical, prove sensitivity with a controlled failure, then restore the implementation.

Run the affected test targets and relevant repository checks. Resolve introduced failures. Record pre-existing failures, flakes, and missing runtime prerequisites separately; do not present an unexecuted test as verified.

Return the behavior protected, changed test paths, why the tests reduce regression risk, and actual check results. Create a PR only when the task authorizes it, with this evidence in its description.
