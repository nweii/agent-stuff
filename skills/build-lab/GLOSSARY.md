# Glossary

The terms this skill and a host's lab section use. Each has one meaning.

- **Lab**: a page in a website where the user decides something about a subject by watching it run and changing it.
- **Lab section**: the part of the site that holds the labs, with the shell and sidebar around them.
- **Subject**: what a lab is deciding about, such as a component, a page section, a motion, or a scale of values.
- **Destination**: the production page or component where the subject ships.
- **Variant**: one structural direction for the subject. Variants differ in layout, structure, motion system, or interaction, and the user switches between them.
- **Current**: the variant production ships. A subject that has not shipped has no current.
- **Proposed variant**: a variant production does not ship.
- **Values**: what the control panel's controls are set to. A saved version is a set of values the user kept to compare.
- **Case**: a condition the subject is shown under, such as an interaction state, a theme, a content extreme, or a width.
- **Canvas**: the frame a lab renders inside.
- **Layout**: one of the canvas's arrangements. A host starts with stage, board, and full bleed.
- **Control panel**: the controls a lab shows for changing values.
- **Decision**: what the user chose in a lab. It can be a variant, a set of values, both, or to change nothing.
- **Outcome**: the written record of a decision, kept in the lab's metadata.
- **Promote**: put a proposed variant into production, in place of current when there is one.
- **Live**: a lab that runs on the site's present code.
- **Frozen**: a lab whose code is removed and whose outcome and captures remain at its URL.
- **State**: whether a lab is live or frozen. A component's hover or disabled state is a case.

[references/freezing.md](references/freezing.md) defines record, capture, snapshot, visit, and thaw.
