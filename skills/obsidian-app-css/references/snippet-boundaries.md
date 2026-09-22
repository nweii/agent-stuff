# Snippet boundaries

Use one file per independently switchable compatibility unit. The unit may contain several selectors and declarations when they implement one behavior; it should split when neighboring rules have different activation decisions, dependencies, or test matrices.

Ask:

> Would someone plausibly disable this behavior without wanting to disable the neighboring behavior?

If yes, split. If the rules must change together to remain correct, keep them together.

## Durable units

These rules form one behavior and belong together:

- fixed note-header positioning, its height, and the matching content offset;
- checkbox sizing, borders, and completed-item color;
- every declaration needed to implement one palette.

These rules have different compatibility boundaries and should be separate:

- heading typography and tabular figures;
- Properties layout and Bases presentation;
- a shared hover variable and a positional source-header button selector;
- core sidebar drag regions and a community plugin's drag regions.

## Example collection

A local override collection might use:

```text
Core - Components - Bases
Core - Components - Overlays
Core - Components - Properties
Core - Interaction - Hover states
Core - Markdown - Checklists
Core - Markdown - Code blocks
Core - Markdown - Spacing
Core - Typography - Headings
Core - Typography - Tabular numbers
Core - Workspace - Drag regions
Core - Workspace - Note and tab header
Plugin - Vertical Tabs - Drag region
```

The first segments create alphabetical groups. The last segment names the independent toggle. `Core` means the snippet targets Obsidian's core interface; it does not promise compatibility with every theme.

## Failure modes

Avoid aesthetic catch-alls such as `Tweaks`, `Interface polish`, or `Miscellaneous`. They describe why someone likes the rules rather than what must be activated and tested together.

Avoid the opposite extreme of one file per selector. That fragments a single behavior and lets required companion rules drift apart. Atomicity belongs at the activation seam, not the declaration.
