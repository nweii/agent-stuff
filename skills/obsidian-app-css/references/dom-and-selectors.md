# DOM and selectors

Use this map to orient inspection, not as a contract. Confirm exact descendants in the running version before relying on them.

## Practical hierarchy

```text
body.obsidian-app.<platform>.<appearance>
└── .app-container
    └── .horizontal-main-container
        └── .workspace
            └── .workspace-split
                ├── .workspace-split.mod-sidedock
                └── .workspace-split.mod-root
                    └── .workspace-tabs
                        └── .workspace-tab-container
                            └── .workspace-leaf
                                └── .workspace-leaf-content[data-type="…"]
                                    ├── .view-header
                                    └── .view-content
```

Sidebars, split direction, stacked tabs, pop-outs, mobile drawers, Settings, and plugins introduce alternate branches. Prefer the nearest stable class or attribute rather than encoding the entire path.

## Markdown views

Editing mode commonly contains:

```text
.workspace-leaf-content[data-type="markdown"][data-mode="source"]
└── .view-content
    └── .markdown-source-view
        └── .cm-editor
            └── .cm-scroller
                └── .cm-sizer
                    └── .cm-content
                        └── .cm-line
```

Reading mode commonly contains `.markdown-preview-view` and `.markdown-preview-sizer`. Live Preview mixes Obsidian and CodeMirror classes; target semantic variables or the shallowest class that distinguishes the behavior.

CodeMirror classes are implementation details. Use them for editor-only behavior when necessary, and verify after Obsidian or installer updates.

## Body and platform classes

Common classes include:

- `.theme-light`, `.theme-dark`
- `.mod-macos`, `.mod-windows`, `.mod-linux`
- `.is-mobile`, `.is-phone`, `.is-tablet`, `.is-ios`, `.is-android`
- `.is-translucent`, `.is-frameless`, `.is-hidden-frameless`, `.is-fullscreen`
- `.is-popout-window`

There is no general `.is-desktop`; use `body:not(.is-mobile)`. Platform and appearance classes identify environment, not the selected community theme.

## Selector stability

### Strong

- Documented CSS variables
- Body platform and appearance classes
- `data-type` and `data-mode` on `.workspace-leaf-content`
- A plugin's documented root class

### Conditional

- High-level workspace, view, and component classes
- Theme setting classes and private variables, gated to that theme
- Plugin implementation classes, gated to that plugin root
- Short selectors using `:has()` for an observed state

### Fragile

- Deep descendant chains
- `nth-child` and `nth-last-child`
- Generated or transient classes
- CodeMirror line-decoration internals
- Selectors inferred from one theme's compiled CSS without live DOM confirmation

Fragile selectors need a comment naming what structural assumption they depend on.

## Multiple Electron windows

CSS snippets load into Obsidian-managed app windows, but plugin code that injects a style, body class, or variable must target the intended window. For persistent main-workspace UI, derive the document from `app.workspace.containerEl.ownerDocument`; Settings may be a separate active window. Use `activeDocument` only for UI that belongs to the currently focused window.

## Inspecting the cascade

In Electron DevTools:

1. Inspect the rendered element.
2. Read the matched rules and computed value.
3. Follow the winning variable to its declaration.
4. Identify the stylesheet or injected snippet that supplied it.
5. Inspect `<head>` when two snippets have equal specificity and order decides the winner.

The installed app's `app.css`, selected theme's `theme.css`, plugin stylesheet, and enabled snippets are current evidence. Documentation and remembered hierarchies are orientation only.
