# UI Components Reference

## List

The de-facto interface for presenting similar data (to-dos, files, search results).

### Key Props

| Prop | Type | Description |
|------|------|-------------|
| `isLoading` | boolean | Show loading indicator |
| `filtering` | boolean | Enable/disable built-in filtering |
| `onSearchTextChange` | (text) => void | Custom search handling |
| `searchBarPlaceholder` | string | Placeholder text |
| `isShowingDetail` | boolean | Show detail panel on right side |

### Example

```tsx
import { List } from "@raycast/api";

export default function Command() {
  return (
    <List isLoading={false} searchBarPlaceholder="Search items...">
      <List.Section title="Recent">
        <List.Item title="Item 1" subtitle="Description" />
        <List.Item title="Item 2" accessories={[{ text: "Tag" }]} />
      </List.Section>
    </List>
  );
}
```

### List.Item Props

| Prop | Description |
|------|-------------|
| `title` | Main text |
| `subtitle` | Secondary text |
| `icon` | Icon or image |
| `accessories` | Right-side badges/tags |
| `actions` | ActionPanel for this item |
| `detail` | Detail view (when `isShowingDetail` is true) |

---

## Detail

Renders markdown content with optional metadata panel.

### Key Props

| Prop | Type | Description |
|------|------|-------------|
| `markdown` | string | CommonMark content |
| `metadata` | Detail.Metadata | Structured data panel |
| `isLoading` | boolean | Loading state |
| `actions` | ActionPanel | Available actions |

### Example

```tsx
import { Detail } from "@raycast/api";

const markdown = `
# Title
![Image](https://example.com/image.png)
Some content here.
`;

export default function Command() {
  return (
    <Detail
      markdown={markdown}
      metadata={
        <Detail.Metadata>
          <Detail.Metadata.Label title="Status" text="Active" />
          <Detail.Metadata.TagList title="Tags">
            <Detail.Metadata.TagList.Item text="Important" color="#ff0000" />
          </Detail.Metadata.TagList>
          <Detail.Metadata.Separator />
          <Detail.Metadata.Link title="Website" target="https://raycast.com" text="Raycast" />
        </Detail.Metadata>
      }
    />
  );
}
```

---

## Form

Collect user input with validation and state management.

### Key Props

| Prop | Type | Description |
|------|------|-------------|
| `actions` | ActionPanel | Submit and other actions |
| `enableDrafts` | boolean | Persist form values |
| `isLoading` | boolean | Loading state |

### Form Elements

| Element | Purpose |
|---------|---------|
| `Form.TextField` | Single-line text |
| `Form.TextArea` | Multi-line text |
| `Form.PasswordField` | Concealed input |
| `Form.Checkbox` | Boolean toggle |
| `Form.DatePicker` | Date/time selection |
| `Form.Dropdown` | Select from options |
| `Form.TagPicker` | Multi-select tags |
| `Form.FilePicker` | File selection |
| `Form.Separator` | Visual separator |

### Example with useForm

```tsx
import { Action, ActionPanel, Form, showToast, Toast } from "@raycast/api";
import { useForm, FormValidation } from "@raycast/utils";

interface FormValues {
  name: string;
  email: string;
}

export default function Command() {
  const { handleSubmit, itemProps } = useForm<FormValues>({
    onSubmit(values) {
      showToast({ style: Toast.Style.Success, title: "Submitted!", message: values.name });
    },
    validation: {
      name: FormValidation.Required,
      email: (value) => {
        if (!value?.includes("@")) return "Invalid email";
      },
    },
  });

  return (
    <Form actions={<ActionPanel><Action.SubmitForm onSubmit={handleSubmit} /></ActionPanel>}>
      <Form.TextField title="Name" placeholder="Your name" {...itemProps.name} />
      <Form.TextField title="Email" placeholder="you@example.com" {...itemProps.email} />
    </Form>
  );
}
```

---

## Grid

Image-focused layouts, alternative to List.

### Key Props

| Prop | Type | Description |
|------|------|-------------|
| `columns` | number | Column count (1-8) |
| `aspectRatio` | string | "1", "3/2", "16/9", etc. |
| `fit` | Grid.Fit | How images fill cells |
| `inset` | Grid.Inset | Padding around items |

### Example

```tsx
import { Grid, ActionPanel, Action } from "@raycast/api";

export default function Command() {
  return (
    <Grid columns={4} aspectRatio="16/9">
      <Grid.Item
        content="https://example.com/image.jpg"
        title="Photo 1"
        actions={
          <ActionPanel>
            <Action.OpenInBrowser url="https://example.com/image.jpg" />
          </ActionPanel>
        }
      />
    </Grid>
  );
}
```

---

## ActionPanel

Actions the user can perform. First action = primary (⏎), second = secondary (⌘⏎).

### Structure

```tsx
<ActionPanel title="Actions">
  <ActionPanel.Section title="Main">
    <Action title="Primary" onAction={() => {}} />
    <Action.OpenInBrowser url="..." />
  </ActionPanel.Section>
  <ActionPanel.Section title="Copy">
    <Action.CopyToClipboard content="..." />
  </ActionPanel.Section>
  <ActionPanel.Submenu title="More">
    <Action title="Nested" onAction={() => {}} />
  </ActionPanel.Submenu>
</ActionPanel>
```

### Common Actions

| Action | Purpose |
|--------|---------|
| `Action` | Custom action with onAction |
| `Action.OpenInBrowser` | Open URL |
| `Action.CopyToClipboard` | Copy content |
| `Action.Paste` | Paste content |
| `Action.Push` | Navigate to new view |
| `Action.SubmitForm` | Submit form |
| `Action.ShowInFinder` | Reveal file |
| `Action.Trash` | Move to trash |

---

## MenuBarExtra

Status bar applications with dropdown menus.

### Key Props

| Prop | Type | Description |
|------|------|-------------|
| `icon` | Image.ImageLike | Menu bar icon |
| `title` | string | Optional text next to icon |
| `isLoading` | boolean | Show loading indicator |

### Example

```tsx
import { Icon, MenuBarExtra, open } from "@raycast/api";

export default function Command() {
  return (
    <MenuBarExtra icon={Icon.Bookmark} title="Bookmarks">
      <MenuBarExtra.Section title="Favorites">
        <MenuBarExtra.Item
          title="Raycast"
          onAction={() => open("https://raycast.com")}
        />
      </MenuBarExtra.Section>
      <MenuBarExtra.Submenu title="More">
        <MenuBarExtra.Item title="Settings" onAction={() => {}} />
      </MenuBarExtra.Submenu>
    </MenuBarExtra>
  );
}
```

> [!NOTE]
> MenuBarExtra requires `mode: "menu-bar"` in package.json command config.
