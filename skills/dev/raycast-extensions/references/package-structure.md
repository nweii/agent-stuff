# Package Structure Reference

## Extension Manifest (package.json)

### Basic Structure

```json
{
  "$schema": "https://www.raycast.com/schemas/extension.json",
  "name": "my-extension",
  "title": "My Extension",
  "description": "What my extension does",
  "icon": "extension-icon.png",
  "author": "your-username",
  "license": "MIT",
  "commands": [...],
  "preferences": [...],
  "dependencies": {
    "@raycast/api": "^1.0.0",
    "@raycast/utils": "^1.0.0"
  },
  "devDependencies": {
    "@raycast/eslint-config": "^1.0.0",
    "typescript": "^5.0.0"
  }
}
```

---

## Commands

Each command is an entry point to your extension.

```json
{
  "commands": [
    {
      "name": "search",
      "title": "Search Items",
      "subtitle": "My Extension",
      "description": "Search through your items",
      "mode": "view",
      "icon": "search-icon.png"
    }
  ]
}
```

### Command Properties

| Property | Required | Description |
|----------|----------|-------------|
| `name` | Yes | Unique identifier (matches filename in src/) |
| `title` | Yes | Display name in Raycast |
| `description` | Yes | Shown in Store and search |
| `mode` | Yes | `"view"`, `"no-view"`, or `"menu-bar"` |
| `subtitle` | No | Secondary text |
| `icon` | No | Command-specific icon |
| `keywords` | No | Additional search terms |
| `disabledByDefault` | No | User must enable manually |

### Command Modes

| Mode | Description |
|------|-------------|
| `view` | Renders UI (List, Detail, Form, Grid) |
| `no-view` | Background execution, no UI |
| `menu-bar` | Renders MenuBarExtra in status bar |

---

## Arguments

Command arguments for parameterized commands.

```json
{
  "commands": [
    {
      "name": "search",
      "title": "Search",
      "mode": "view",
      "arguments": [
        {
          "name": "query",
          "type": "text",
          "placeholder": "Search term",
          "required": true
        }
      ]
    }
  ]
}
```

### Argument Types

| Type | Value Type | Description |
|------|------------|-------------|
| `text` | string | Free text input |
| `password` | string | Concealed text |
| `dropdown` | string | Select from options |

### Using Arguments

```tsx
interface Arguments {
  query: string;
}

export default function Command(props: LaunchProps<{ arguments: Arguments }>) {
  const { query } = props.arguments;
  return <List searchText={query}>...</List>;
}
```

---

## Preferences

Extension-wide or command-specific settings.

```json
{
  "preferences": [
    {
      "name": "apiKey",
      "type": "password",
      "required": true,
      "title": "API Key",
      "description": "Your API key from the service"
    },
    {
      "name": "defaultView",
      "type": "dropdown",
      "required": false,
      "title": "Default View",
      "description": "Choose starting view",
      "default": "list",
      "data": [
        { "title": "List View", "value": "list" },
        { "title": "Grid View", "value": "grid" }
      ]
    }
  ]
}
```

### Preference Types

| Type | Value | Description |
|------|-------|-------------|
| `textfield` | string | Single-line text |
| `password` | string | Concealed text |
| `checkbox` | boolean | Toggle |
| `dropdown` | string | Select from options |
| `appPicker` | Application | App selection |
| `file` | string | File path |
| `directory` | string | Directory path |

### Accessing Preferences

```tsx
import { getPreferenceValues } from "@raycast/api";

interface Preferences {
  apiKey: string;
  defaultView: "list" | "grid";
}

export default function Command() {
  const { apiKey, defaultView } = getPreferenceValues<Preferences>();
}
```

---

## Icons

Place icons in `assets/` folder.

### Requirements
- PNG format recommended
- Minimum 512x512 pixels
- For dark mode support: `icon.png` and `icon@dark.png`

### Using Icons

```tsx
import { Icon, List } from "@raycast/api";

// Built-in icons
<List.Item icon={Icon.Star} title="Favorite" />

// Custom icons from assets/
<List.Item icon="my-icon.png" title="Custom" />

// With tint color
<List.Item icon={{ source: Icon.Circle, tintColor: Color.Red }} title="Red" />
```

---

## File Structure

```
my-extension/
├── package.json
├── tsconfig.json
├── src/
│   ├── search.tsx        (matches command name)
│   ├── settings.tsx
│   └── utils/
│       └── api.ts
├── assets/
│   ├── extension-icon.png
│   ├── extension-icon@dark.png
│   └── command-icon.png
└── README.md
```
