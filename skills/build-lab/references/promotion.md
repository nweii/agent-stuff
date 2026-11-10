# Promoting a subject

Read this when a proposed variant will ship, when a production component comes into a lab, or when a subject renders differently in the lab and in its destination.

## Where a subject's code lives

[GLOSSARY.md](../GLOSSARY.md) defines subject, destination, variant, current, and promote.

Current lives in production, and the lab imports it. A proposed variant lives in the lab folder until the user decides to ship it. The imports show which is which. A decision about current sends values back to production. A decision for a proposed variant sends code.

When the subject has a current, keep it as a variant named `current`. A redesign is judged against what ships, so the user needs to switch between the two.

## How a lab differs from the destination

A lab renders the subject outside its destination, and the two differ in two ways.

- **Deliberate differences** are part of the experiment: forced conditions, fixtures, an isolated stage. The lab's code already shows them.
- **Accidental differences** come from what the subject reads from its surroundings. For instance, the canvas pane is smaller than the window, so `vh`, `vw`, media queries, and `fixed` positioning resolve against the wrong box. Anything else the destination supplies can differ the same way, for example a parent's width, a provider, global styles, or live data.

Find an accidental difference by comparing the subject in the lab and in the destination under the same conditions, such as the same width. Compare when the result could depend on the subject's surroundings. A layout decision usually can, and a color or a duration usually cannot. Tell the user what differs before changing the subject. Fix it in the subject when the subject can stop reading the surroundings that differ. For instance, a subject sized from its container (`cqw`, `cqh`, `@container`) renders the same in the pane and in the window. Fix it in the lab when the lab supplied the wrong surroundings. When neither fix is possible, state the difference in the lab's description.

When a host finds another kind of accidental difference, offer to record it and its fix in the host's agents file, so later labs avoid it.

## Judge in the destination before deciding

The user decides better when they see a variant where it ships. For a change to an existing page, render the destination's surrounding section in the lab with the variant in place. The variant then reads the surroundings it ships into. When the section cannot take the variant without a production change, propose that change, or tell the user the decision is being made outside the destination.

Render the subject alone on a stage when isolation helps the decision, for instance when checking conditions, tuning a component used in many places, or designing something that has no destination yet.

## Promote a proposed variant

1. **Move the variant.** Move its modules from the lab folder into production with history-preserving renames, in place of current when there is one.
2. **Import it back.** Point the lab's `current` variant at the production module. Git history keeps the replaced one. Copy it into the lab as a variant when the user wants to keep comparing against it.
3. **Confirm in the destination.** Open the destination and confirm it shows what the lab showed. Fix or state each accidental difference.
4. **Write the outcome.** Suggest a freeze when the lab's history warrants one ([freezing.md](freezing.md)).

Done when production imports nothing from the lab folder, the lab's `current` variant imports from production, and every accidental difference step 3 found is fixed or stated.

A lab can stay live through several promotions. Suggest a snapshot at each decision.

## Bring a production subject into a lab

Import the subject. A copy stops matching production once production changes, and values tuned on a copy may not suit what ships. When the subject renders only inside its page, one option is to extract the part under study into its own production module and import that. Extraction changes production code, so propose it to the user first.
