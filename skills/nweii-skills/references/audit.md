# Audit a skill collection

Use this branch for a requested collection audit. Follow the source-ownership rules in the entrypoint and [installation.md](installation.md) before recommending installation commands.

## Inventory and ownership

Identify the requested source library or installed collection. Include standalone skills and plugin members, resolve links, and record name, canonical path, installation source, author, audience, description, and actual procedure. Read supporting files when the entrypoint alone cannot establish scope.

Classify Nathan-authored skills by recorded authorship and retained adaptations by their provenance. `metadata.internal: true` describes audience; it does not establish authorship. Unknown ownership stays unknown until checked. Installed paths are downstream even when Nathan authored the skill.

Preserve upstream installation chains. Recommend keeping or removing an upstream skill, or creating an explicitly attributed adaptation in owned source when justified. A retained vendor copy follows its recorded refresh and adaptation policy.

## Compare contested procedures

Cluster same-function alternatives, subsets, toolchain duplicates, and complementary specializations. A shared topic alone does not justify consolidation.

For each contested pair, read both complete procedures and relevant supporting files. Compare trigger scope, unique capabilities, prerequisites, approval boundaries, scripts, tests, examples, and edge cases. Identify what removal would lose and what a merge would need to preserve. Use concrete passages as evidence. Compare directly; independent comparisons can be delegated when the environment and task instructions allow it.

Assign an evidenced disposition to each member:

- Keep: distinct purpose or complementary procedure.
- Remove as redundant: another skill covers its useful scope; name any loss.
- Bench as unused: user or session evidence supports disuse; confirm before removal.
- Consolidate into owned source: preserve named capabilities and attribution before retiring the source.
- Investigate: insufficient evidence to choose.

Description quality is routing evidence, not proof of runtime quality or actual use. Mark uncertain usage and unavailable dependencies explicitly.

## Return a reviewable plan

Report the inventory count and ownership breakdown, contested clusters, dispositions, exact source paths, and unresolved questions. For each proposed consolidation, name the receiving skill, unique material to preserve, dependency effects, and public-export boundary.

Derive concrete `bunx skills` actions from the current CLI and the intended client and scope. Include required internal discovery flags where applicable. Distinguish source edits, removal of an installed copy, plugin packaging, and upstream publishing. Each proposed action must identify its target and loss or benefit.

The audit is complete when every in-scope member has a disposition or evidenced uncertainty and every proposed action has a concrete target. Apply only actions Nathan has authorized.
