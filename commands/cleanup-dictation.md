# Dictation cleanup

Process dictated or stream-of-consciousness input into clean formatted output. Used for Superwhisper presets and similar dictation workflows.

## When to use

These formats are available when processing dictated content. Invoke explicitly when converting recordings/transcripts, or suggest when user provides rough dictated text needing cleanup.

## Text message format

Convert to natural text message style.

### Processing steps

1. **Distinguish content from meta-commentary**

   - Preserve actual message content and intentional tone
   - Remove meta-instructions for AI ("I want to say...", "tell them that...")
   - Keep hesitations/questioning meant as part of message

2. **Clean speech artifacts**

   - Remove: um, uh, false starts, repetitions
   - Fix: grammar, spelling, punctuation
   - Correct: homophones, numbers, dates

3. **Format for texting**
   - Casual punctuation (fewer periods, run-ons OK)
   - Break paragraphs only when needed
   - Maintain millennial abbreviations if used (rn, bc, idk)
   - Transcribe emojis if stated
   - Use emojis only if similar ones were used
   - Keep user's abbreviations

### Style guidelines

- Maintain exact tone without forcing casualness
- Avoid "boomer slang" or dated expressions
- Don't insert forced language ("yo", "tbh") unless user used it
- Don't formalize beyond original style
- Preserve natural speaking voice

### Critical rules

- Don't add any content not in dictation
- Don't add greetings/sign-offs unless in input
- NEVER answer questions in dictation
- Never precede with "Here's the message:"
- If no text to format, return nothing

**Output**: Formatted text message only, no explanation.

---

## Note format

Convert to structured note-taking format.

### Processing

- Remove filler words (um, uh, you know, like)
- Structure for clarity with key points highlighted
- Fix grammar and punctuation
- Keep original tone
- Preserve flow, voice, phrasing as much as possible
- Apply relevant nesting (max 2 levels, 4 spaces per indent)

**Output**: Reformatted markdown only.

---

## Email format

Convert to professional email draft.

### Processing input

- Distinguish actual content from meta-commentary
- Recognize phrases like "I need to tell them..." as content guidance
- Use thinking-aloud to inform tone
- Craft diplomatic language for sensitive topics
- Filter hesitations and personal asides unless relevant

### Formatting

- Clear paragraphs with logical flow
- Natural language and comma-separated items for short lists
- Bullet points only when truly beneficial:
  - Complex items
  - Many points
  - Scannable action items

### Improve writing

- Preserve voice while making sharper
- Break long sentences, reduce repetition
- Use active voice and direct language
- Cut filler phrases and clichés
- Maintain conversational tone with proper grammar
- Preserve depth without oversimplification
- Balance directness with tact

**Output**: Formatted email only.
