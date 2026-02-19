# Hooks & Utilities Reference

## Data Fetching

### useFetch

Fetch data with stale-while-revalidate caching.

```tsx
import { List } from "@raycast/api";
import { useFetch } from "@raycast/utils";

interface Post { id: number; title: string; }

export default function Command() {
  const { data, error, isLoading, revalidate } = useFetch<Post[]>(
    "https://api.example.com/posts"
  );

  return (
    <List isLoading={isLoading}>
      {data?.map((post) => <List.Item key={post.id} title={post.title} />)}
    </List>
  );
}
```

#### Pagination

```tsx
const { data, pagination } = useFetch(
  (options) => `https://api.example.com/posts?page=${options.page + 1}`,
  {
    mapResult(result) {
      return { data: result.posts, hasMore: result.page < result.totalPages };
    },
    keepPreviousData: true,
  }
);

return <List pagination={pagination}>...</List>;
```

### usePromise

For non-fetch async operations.

```tsx
import { usePromise } from "@raycast/utils";

const { data, isLoading } = usePromise(async () => {
  return await someAsyncOperation();
});
```

---

## Storage

### LocalStorage

Persistent encrypted key-value store.

```tsx
import { LocalStorage } from "@raycast/api";

// Set
await LocalStorage.setItem("key", "value");

// Get
const value = await LocalStorage.getItem<string>("key");

// Remove
await LocalStorage.removeItem("key");

// All items
const all = await LocalStorage.allItems();
```

### Cache

Simple caching with optional TTL.

```tsx
import { Cache } from "@raycast/api";

const cache = new Cache();

// Set with TTL (seconds)
cache.set("key", JSON.stringify(data), { ttl: 3600 });

// Get
const cached = cache.get("key");
if (cached) {
  const data = JSON.parse(cached);
}

// Check
cache.has("key");

// Remove
cache.remove("key");
```

---

## Clipboard

```tsx
import { Clipboard, showHUD } from "@raycast/api";

// Copy text
await Clipboard.copy("Hello World");

// Copy file
await Clipboard.copy({ file: "/path/to/file.pdf" });

// Copy concealed (password)
await Clipboard.copy("secret", { concealed: true });

// Read
const { text } = await Clipboard.read();

// Paste
await Clipboard.paste("Text to paste");
```

---

## Notifications

### showToast

```tsx
import { showToast, Toast } from "@raycast/api";

// Success
await showToast({ style: Toast.Style.Success, title: "Done!" });

// Failure
await showToast({
  style: Toast.Style.Failure,
  title: "Error",
  message: "Something went wrong",
});

// Animated (for long operations)
const toast = await showToast({ style: Toast.Style.Animated, title: "Loading..." });
// ... do work ...
toast.style = Toast.Style.Success;
toast.title = "Complete!";
```

### showHUD

Quick feedback overlay.

```tsx
import { showHUD } from "@raycast/api";

await showHUD("Copied to clipboard");
```

---

## System Integration

### runAppleScript

Execute AppleScript or JavaScript for Automation.

```tsx
import { runAppleScript } from "@raycast/utils";

// AppleScript
const result = await runAppleScript('tell application "Finder" to get name of front window');

// JavaScript for Automation
const result = await runAppleScript(
  'Application("System Events").processes.length',
  { language: "JavaScript" }
);

// With arguments
await runAppleScript('on run argv\n  return item 1 of argv\nend run', ["arg1"]);
```

### open

Open URLs, files, or apps.

```tsx
import { open } from "@raycast/api";

await open("https://raycast.com");
await open("/path/to/file.pdf");
await open("raycast://extensions/..."); // Deep links
```

### getSelectedFinderItems

Get files selected in Finder.

```tsx
import { getSelectedFinderItems } from "@raycast/api";

const items = await getSelectedFinderItems();
items.forEach((item) => console.log(item.path));
```

---

## OAuth

Built-in OAuth support for third-party services.

```tsx
import { OAuth } from "@raycast/api";

const client = new OAuth.PKCEClient({
  redirectMethod: OAuth.RedirectMethod.Web,
  providerName: "GitHub",
  providerIcon: "github-icon.png",
  description: "Connect your GitHub account",
});

// Check for existing tokens
const tokenSet = await client.getTokens();

// If no tokens, start authorization
if (!tokenSet) {
  const authRequest = await client.authorizationRequest({
    endpoint: "https://github.com/login/oauth/authorize",
    clientId: "YOUR_CLIENT_ID",
    scope: "repo user",
  });
  
  const { authorizationCode } = await client.authorize(authRequest);
  // Exchange code for tokens...
}
```

---

## Navigation

### useNavigation

```tsx
import { useNavigation, Detail, List, Action, ActionPanel } from "@raycast/api";

function ListView() {
  const { push, pop } = useNavigation();
  
  return (
    <List>
      <List.Item
        title="Show Details"
        actions={
          <ActionPanel>
            <Action title="Open" onAction={() => push(<DetailView />)} />
          </ActionPanel>
        }
      />
    </List>
  );
}
```

### launchCommand

Launch other commands.

```tsx
import { launchCommand, LaunchType } from "@raycast/api";

await launchCommand({
  name: "other-command",
  type: LaunchType.UserInitiated,
  arguments: { query: "test" },
});
```
