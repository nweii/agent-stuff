---
alwaysApply: false
title: rollup-periodic-summary
description: Generate rollup summaries for periodic notes (weekly/quarterly/yearly) by synthesizing child note descriptions
---

# Periodic note rollup summary

When asked to generate a summary for a periodic note (weekly, quarterly, or yearly), follow this workflow:

## Process

1. **Identify the note hierarchy**

   - Determine which periodic level you're summarizing (e.g., quarterly from weeklies, weekly from dailies)
   - Locate all related child notes referenced in the `related` frontmatter property

2. **Extract child descriptions**

   - Read the `description` property from each child note's frontmatter
   - These summaries usually crystallize the period's essence. However, if a description is missing, feels too vague, or if a specific day/week seems particularly significant, you are encouraged to read the original note content or sub-referenced notes to gain a more complete understanding.

3. **Scan parent note content**

   - Check if the parent note has any "Notes" or remarks sections that add context the children don't capture
   - Look for emergent patterns, meta-reflections, or threads that span multiple children
   - Don't treat these as equally weighted to the children—they're supplementary unless particularly revealing

4. **Synthesize without imposing narrative**

   - Combine child descriptions to surface what _actually_ happened across the period, not what makes a good story
   - Identify real tensions, recurring patterns, or unresolved threads
   - Avoid artificial arcs, redemption narratives, or forced thematic coherence
   - Keep it concise: aim for 2-4 sentences for weekly rollups, 3-5 for quarterly/yearly

5. **Update frontmatter**
   - Add or update the `description` property in the parent note's YAML
   - Use double quotes; preserve all other formatting
   - Only modify the description property

## Style guidelines

- Use semicolons and dashes to separate ideas rather than connective adverbs
- Prioritize concrete details and specific proper nouns that help memory recall
- Include ambiguity or unresolved tensions if they characterize the period
- Don't hedge or soften—be direct about what the period actually contained
