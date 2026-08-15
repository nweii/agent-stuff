# Variant comparison

Read this when one lab contains multiple structural or interaction directions that benefit from rapid, full-size comparison. Skip it when the differences are only control values.

## Choose the comparison layer

Use the control panel's presets when every direction shares one implementation and differs only in parameter values. Use a variant picker when directions change layout, component structure, motion system, or interaction model. Keep each decision in one layer so the same choice never appears in both the picker and the control panel.

## Picker contract

- Keep the set small: two to five named directions, each with a stated axis such as layout, density, personality, motion, or interaction.
- Render one variant at full size in realistic context. Side-by-side thumbnails distort the spacing and scale being judged.
- Switch the rendered variant instantly. The picker may animate its own active indicator, with a reduced-motion fallback, but the comparison itself stays immediate.
- Store the selected direction in a stable named `?v=<name>` value so reloads and shared links preserve it.
- Use native buttons with a clear current state, hover and focus-visible treatment, and number or arrow-key access that ignores editable controls and modified keypresses.
- Keep the picker visually quiet, floating above the canvas without covering the work. Move it to another edge when its normal position conflicts with the experiment.
- Add replay only when motion needs to be retriggered for a fair comparison.

Retain variants by default after a direction is accepted so later comparisons remain possible. Follow the user's or host's cleanup preference when it differs, and record the accepted direction in the lab's outcome metadata.

## Verification

Done when every named variant is reachable by pointer and keyboard, exactly one is current, a copied variant URL survives reload, the picker does not cover the work at narrow or wide widths, and switching produces no console errors.
