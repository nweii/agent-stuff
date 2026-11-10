# DialKit

Read this when wiring a lab's controls. [DialKit](https://github.com/joshpuckett/dialkit) is the default control panel for labs. It has adapters for React, Solid, Svelte, Vue, and plain JavaScript.

This file says what each DialKit feature is for in a lab. DialKit changes often, so read the installed version's README and `docs/reference.md` for exact names and options before writing code. On a host that uses another panel library, map these uses onto that library.

## How the user works with the panel

The user moves controls, saves versions to compare, and presses **Copy** to hand the result to an agent. Build each lab for that loop. The panel's own choices belong to the user. For instance, the user decides where it sits and whether it remembers values.

| In a lab, the user wants to | DialKit feature |
| --- | --- |
| Tune values | A panel defined with `useDialKit` or `createDialKit` |
| Keep the panel off the subject | The root's `mode`: a floating panel the user can drag and collapse, or an inline panel that fills a container |
| Compare sets of values | **Save version**, the version thumbnails, and the all-versions grid |
| Hand accepted values to an agent | **Copy**, which puts the values and an instruction on the clipboard |
| Replay or reset | Action controls with `onAction` |
| Tune animation timing | A timeline and its dock, with play, pause, replay, and scrubbing |
| Adjust a value while looking at the subject | Shortcuts assigned per control |
| Reopen a lab where they left it | `persist` with a stable `id` |

## Use what DialKit has

Use a DialKit feature where one covers the need, so the user works the same panel in every lab.

- **Comparing values.** Saved versions cover directions that differ only in values. Add a variant picker ([variant-comparison.md](variant-comparison.md)) when directions differ in structure.
- **Playback.** A lab tuned through a timeline uses the dock's transport. A lab with another animation loop exposes replay as an action control.
- **Accepting values.** The user presses **Copy** and pastes the result to the agent, who applies it to the production source.
- **One panel for many copies.** A conditions board ([canvases.md](canvases.md)) reads one panel's values and passes them to every entry.
- **Driving the panel from the lab.** A picker or toggle that must change panel values uses the controller.

## Starting points

- Define each panel's config from the defaults the production module exports.
- Order controls in the sequence someone tunes the result, and start secondary folders collapsed.
- Float the panel on a stage or full bleed lab. Mount it inline in a docked container beside a board.
- Leave `persist` off, so a lab opens on production's values. Turn it on when the user wants a lab to reopen where they left it.

## Failures that show no error

- **Framework adapters hide the panel in production builds.** A lab served from the deployed site then has no controls. Set `productionEnabled` on the root for the lab section.
- **A subject bound to a timeline's sampled values depends on DialKit.** Write the subject's production animation code before promoting it ([promotion.md](promotion.md)).
