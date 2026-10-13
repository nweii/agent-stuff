# Process a meeting

Use this branch when importing and processing a meeting end to end, auditing and enriching an existing meeting, or resuming after a transcript paste or correction review. Apply the procedures in this conversation; separate agents, model selections, and provider-specific tools are unnecessary.

## 1. Inspect saved state

Identify the meeting, destination, and linked transcript note. Read both notes before writing. Find the actual transcript under `## Transcript`; substantive content means dialogue or several meaningful paragraphs, not the staging instruction or an audit section.

State the phase briefly:

- **Import needed:** one or both notes are missing. Use the main skill's import steps to complete the pair. Re-read the transcript after saving; a successful tool call alone does not establish that it landed.
- **Waiting for transcript:** the pair exists, but the transcript is empty or contains only its placeholder. Offer its title, path, and Obsidian URI, and explain where to paste the Granola transcript. Open it when local note-opening tools are available. Return here until content exists.
- **Ready to process:** the pair and transcript exist. Continue below without reimporting.
- **Awaiting review or completed:** saved transcription notes already exist. Reconcile their statuses and any enrichment with the current transcript and user feedback; resume pending work rather than generating duplicate flags or additions.

If a note's structure is unexpected or a required write cannot be verified, report that step and preserve its contents. Ask only for the input needed to continue.

## 2. Audit and retain the evidence

Read `audit-transcription`'s full instructions from the available bundle or skill source. Follow its whole-transcript reading, documented-domain context, and confidence tiers. The first pass flags possible errors; confirmed corrections require the user's review.

Save the findings above `## Transcript` in a `## Transcription notes` section. Each entry records the exact source span, proposed correction or interpretation, confidence and reason, and status (pending, confirmed, rejected, or applied). Preserve unrecoverable text without reconstructing it. Record that the source is auto-transcribed when it is.

Reuse the existing section on resume. Preserve prior decisions and applied-change history; revise only pending findings affected by new evidence. Keep user-authored content intact. When no flags exist, report that result without adding an empty section.

Re-read the saved audit before continuing. The pass is complete when every flagged span is recoverable from the transcript note and its review state is explicit.

## 3. Prepare enrichment and obtain review

Read `enrich-from-transcript`'s full instructions from the available bundle or skill source. Apply its enrichment dimensions to the meeting note, preserving existing substance and authorship. Audit proposals are hypotheses: use them to identify uncertain passages, not as confirmed quotations or facts. Exact phrases must be grounded in reliable transcript text; defer any interpretation whose meaning depends on an unconfirmed repair.

Show the proposed meeting-note additions and the pending audit findings together. Ask for the user's corrections or confirmation of the specific proposals. Follow previously supplied approvals; confirm only the remaining interpretive choices. Do not infer the user's personal impressions from the transcript.

Keep the durable audit pending if the user stops before review. Enrichment is prepared for review, not reported as saved. After review, record accepted and rejected findings and apply only approved enrichment.

## 4. Apply confirmed corrections

Apply approved vocabulary repairs context-sensitively to the flagged transcript spans. Preserve dialogue order, structure, speaker attribution, and unrecoverable passages. For a confirmed interpretation of a garbled clause, follow the audit procedure's callout format and retain the original text beneath it rather than replacing the dialogue.

Keep the transcription notes as the record of the original spans, decisions, and applied changes. Directly under `## Transcript`, add one italic provenance line stating that confirmed corrections are recorded in `## Transcription notes` and unrecoverable spans remain as transcribed. Add it only after actual corrections; reuse it on later passes.

Re-read both notes. Verify each approved change, preserved raw passages, provenance, links, and absence of duplicated enrichment. Keep any pending findings visible for a later session.

## Return

Give the meeting and transcript links, number of audit flags, whether corrections and enrichment are saved or awaiting review, and the next concrete input if processing remains incomplete. Completion means requested and approved changes are saved and read back; an empty transcript or pending review remains an explicit resumable state.
