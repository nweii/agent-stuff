# Repo docs audit checklist

Check each item against every changed section. Rewrite toward the rule in `SKILL.md`; when a cut leaves a gap, fill it with the specific fact the flagged phrase stood in for. Items marked *(suggestion)* are recommendations to raise with the owner, not defects to fix.

## Reader and placement

- The opening states what the project is and what the reader gets before any mechanism or term of art.
- Every section applies to this project and its users, and sits in the document that owns it.
- Each fact has one canonical home; other docs link to it.
- No personal domains, IDs, or private references, and examples use fictional data.
- Each content section would stay correct if read in isolation or if someone else maintained the project; maintainer names, support links, credits, and build notes sit in meta sections.
- Examples are framed as examples, not as the whole feature.
- Optional paths read as optional; nothing assumes what the reader wants, owns, or has already bought.
- Each step that creates an account, token, or setting says what it is and why the project needs it.

## Claims

- Every claim traces to code, config, or a command run.
- Every echo of a changed fact (site, storefront, in-app help, `AGENTS.md`) agrees.
- Comparisons with paid, free, or rival options, and alternate install paths, state each side's real cost.
- No claim implies a model the software does not follow.
- Headings, feature lead-ins, and openings carry only details that are decision-relevant and stable; useful details that change often sit in a table, docs page, or release notes.
- Privacy and network statements name each external service and why it is contacted.
- Any directory-required disclosures (such as Obsidian's plugin policy) are present.

## Durability

- Time-bound facts are limited to minimum requirements, one adoption-relevant maturity line, reader-protecting warnings that still apply, and dated platform facts.
- No release dates, "what's new" sections, listing status, renames, retired parts, or obsolete plans.

## Prose

- Sentences run in forward order and read aloud like a person talking.
- No sales flourishes, quips, personified software, or steering ("use this if…").
- No colon lead-ins, em-dash lists, or "not X, but Y" constructions.
- No roadmap sentences ("Choose one of the methods below").
- No restatement of the opening in later sections.
- No unneeded qualifiers or statements of the obvious.
- Back-references point to something the reader has already seen, in words that name it.
- One term per concept across every doc.

## Format

- The repo's own conventions are followed; defaults fill only what they leave open.
- *(suggestion)* A README shows the project working near the top (an image with alt text, or a code block with real output). When it doesn't, name the shot that would help most.
- Each heading lets a scanning reader predict the section: a direct label for reference and procedures, a succinct summary for a section that makes one point, common signposts as readers expect them; sentence case; no one-item sections.
- Troubleshooting entries quote the literal error or dialog the reader sees.
- Paragraphs wrap naturally, with no hard line breaks.
- Badges are functional and self-updating.
- License is the last section of a README.
