---
name: people-notes
description: "Use for person-centered work in Nathan's Brain vault: prepare context from a profile and linked records, create a canonical person note, or reconcile an existing one."
compatibility: Designed for use with the Brain Obsidian vault.
metadata:
  author: nweii
  version: "0.1.0"
  internal: true
---

# People notes

Prepare task-specific context from person notes and their linked records. Create or maintain a note only when the task calls for a vault change.

## 1. Choose the branch

Read the vault's `AGENTS.md`, then choose one branch from the user's task:

- **Use** — prepare context for work involving a person. This is the read-only default.
- **Create** — make a canonical person note when the user asks for one or the agreed vault task requires it.
- **Maintain** — reconcile an existing person note with newer evidence or requested corrections.

Link cleanup supports create and maintain; it is not a separate branch. A passing reference does not authorize note creation.

This step is complete when one branch is selected and the permitted read/write scope is clear.

## 2. Resolve the person

Search `04-Entities/` case-insensitively by canonical title and aliases. Treat body mentions and linked records as identity clues; a canonical note exists only when its title or aliases resolve the person.

Use relationship, organization, location, and source context to distinguish name variants or collisions. When two people share a full name, use a stable title qualifier such as `Jordan Lee (Design)` and display links such as `[[Jordan Lee (Design)|Jordan Lee]]`.

This step is complete when one canonical note is identified, absence is confirmed, or unresolved candidates are reported.

## 3. Gather evidence

Start with the current conversation, the person note, and the records surfaced by `![[Related.base#Person]]`. Read the recent records relevant to the task rather than dumping every backlink.

Reach beyond the vault only when the task needs more context or a freshness check. Granola meetings, Gmail threads, and verified public profiles are optional evidence sources. Continue with available evidence and report unavailable sources.

Track what each source establishes, its date, and any uncertainty. Treat Nathan's uncertainty as data; qualify or omit claims rather than resolving them by inference.

This step is complete when every task-relevant accessible source has been considered and remaining gaps or conflicts are explicit.

## 4A. Use the person note

Prepare only the context the current task needs:

- who the person is and the durable relationship context;
- the records most relevant to the current task;
- evidence newer than the profile's `last` date;
- uncertainties, conflicting evidence, and material freshness limits.

Keep the result compact and source-linked. Remain read-only unless the task also authorizes create or maintain.

This branch is complete when the current task can proceed from the prepared context or the missing information that prevents it is named.

## 4B. Create a person note

Read `99-Admin/Templates/Person template.md` and render its Templater values. Save the canonical note to `04-Entities/[Canonical title].md`.

Fill only supported fields. Use the metadata rules below, add at most a short ownerless paragraph of durable relationship context, and preserve `![[Related.base#Person]]` at the end. Leave unsupported fields or body content empty.

If the source note being worked on clearly refers to this person, add or preserve its person link. Offer broader link cleanup instead of sweeping the vault.

This branch is complete when there is one canonical note, every populated claim is supported, uncertainty is preserved, the related-note embed remains, and any unresolved collision or unavailable source is reported.

## 4C. Maintain a person note

Compare the profile against the gathered evidence. Reconcile instead of only adding: correct stale claims, remove duplication, preserve useful stable context, and replace raw research with concise supported context when it falls within the requested scope.

Advance `last` only when the note's substantive identity and relationship context was freshly confirmed. Record ordinary interactions in their owning notes; wording edits and link cleanup update `modified` only.

Notice clear unlinked mentions in records already under review. Add the current source link when unambiguous and in scope; otherwise report candidate cleanup targets. Broad link cleanup requires an explicit request.

This branch is complete when every changed claim is supported, stale or conflicting claims in scope are resolved or qualified, metadata follows the rules below, and the profile remains a concise layer over its linked records.

## Metadata rules

### Aliases

Aliases resolve identity; display links control wording.

- Use the person's current preferred full name as the canonical title.
- Add attested full-name variants such as `Elizabeth Smith` / `Liz Smith` or `Matthew Lee` / `Matt Lee`.
- Use `[[Lucille Chen|Lucy]]` for natural prose instead of automatically adding a bare first-name alias.
- Add a bare first name only when Nathan consistently uses it as the person's identity and a vault-wide title/alias search shows no plausible collision. Recheck collisions during maintenance.
- Add handles, alternate spellings, transliterations, initials, shortened surnames, diacritic-free forms, or former names only when Nathan or a source uses them to identify the person.
- Put social-profile slugs in `urls`; derive aliases only from attested usage.
- Treat honorifics and roles as context unless Nathan regularly uses the phrase as the person's name.
- Give brands, publications, and public personas their own entity note when they have an independent identity.
- Never give two notes the same undisambiguated full-name alias. Report aliases skipped because of collisions.

### Description and body

The description answers who the person is and why they are notable in this vault. Prefer durable relevance over an unqualified current job title. Keep it plain, compact, and ownerless: `High-school acquaintance who...` or `Worked together on...`.

The body holds only durable context needed to interpret linked records. Meetings, messages, projects, events, and relationship history remain in their owning notes and link back here. Summarize source material into concise supported context.

### Freshness

`last` is the date on which the profile's substantive identity and relationship context was last confirmed by Nathan or sufficiently current evidence.

- Use `YYYY-MM-DD`.
- Use the date the evidence establishes.
- Leave `last` blank or unchanged when freshness cannot be established.
- Advance it after substantive profile review; a recent interaction or backlink alone updates the linked history.

### Related entities, tags, and contact data

`related` contains existing entity notes with stable associations. A one-time introduction or incidental co-mention is insufficient.

Keep the template's default tag. Search analogous notes and tag prevalence before adding relationship, cohort, role, field, or personal-curation tags. Reuse exact established forms from the vault; keep the taxonomy in the vault rather than duplicating it here, and let Nathan's context establish personal classifications.

Add verified profile URLs. Add email or other contact properties only when useful to the task and consistent with the existing note.

## Report

For read-only use, name the person note and the evidence boundary. For changes, report the note created or maintained, the substantive fields changed, the `last` date used or preserved, and any unresolved ambiguity or optional link-cleanup candidates.
