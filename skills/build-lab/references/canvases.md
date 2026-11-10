# Canvases

The **canvas** is the frame a lab renders inside: its inset, background, control-panel position, and title placement. A host has a few canvas layouts and every lab uses one, so labs look alike.

In production a subject renders in the window. In a lab it renders in the canvas pane, which is smaller. The canvas module is where a host fixes the differences this causes in every lab ([promotion.md](promotion.md)). For instance, a pane that is a size container and the containing block for fixed children lets a subject sized from its container render as it does in its destination.

## Layouts

Start the canvas module with three layouts, sized from the host's tokens:

- **Stage**: one subject, centered, at full size. The default.
- **Board**: several items on one grid, all visible at once, with one gap and one label style. The items are several subjects that share controls, or one subject's cases.
- **Full bleed**: the lab fills the pane and sets its own inset and background.

Start the control panel where it covers nothing the user is judging. A panel usually floats over a stage or full bleed lab and docks beside a board, where a floating panel would cover grid items. The user can move it from there. A variant picker ([variant-comparison.md](variant-comparison.md)) can sit over any layout, because it swaps what the lab renders.

When no layout fits a lab, add one to the canvas module so later labs can use it. Keep the module outside the shell, so a lab can import it without importing the shell.

## Cases board

A stage lab can give the user a switch to a board of its subject's cases. Both views read the same control values, so one control change updates every case. Put the switch's state in the URL, like the variant name, so a reload or a shared link keeps the view.

1. **List the cases.** Pick the conditions that could change the decision. For instance, a button's interaction states, a card with a long title and with none, or a layout at phone width. Show the user the list, because they know which cases worry them. Done when the user has seen it.
2. **Force each case.** For a state, prefer the component's own controlled props or `data-*` attributes. An interaction pseudo-class such as hover has no prop, so hold it another way. For instance, duplicate each same-origin CSS rule that uses it with an attribute selector the entry sets. For a theme, set the theme's class or attribute on the entry. For a width, give the entry a container of that width. Done when every entry shows its case without input.
3. **Label each entry** with its case. For a state, add the source file and line that renders it, so the user can find its code.

The board follows [Raphael Salaja's `lab.js`](https://github.com/raphaelsalaja/skills/tree/main/skills/lab), which shows every state of a component as a web component with its own grid and sliders. In a lab, build it with the board layout and the lab's panel.

## Verification

Done when every live lab uses a layout, each layout holds the shell's title line and inset at wide and narrow widths, and a cases board shows every listed case while a control change updates all of them.
