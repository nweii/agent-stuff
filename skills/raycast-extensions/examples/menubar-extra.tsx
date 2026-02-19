// ABOUTME: Example of a Raycast MenuBarExtra for status bar presence.
// ABOUTME: Shows sections, submenus, and actions for menu bar commands.

import { Icon, MenuBarExtra, open, showHUD, LaunchType } from "@raycast/api";
import { useFetch } from "@raycast/utils";

interface Bookmark {
  id: string;
  name: string;
  url: string;
  category: "work" | "personal" | "reference";
}

// Sample data - in a real extension this would come from storage or API
const bookmarks: Bookmark[] = [
  { id: "1", name: "Raycast", url: "https://raycast.com", category: "work" },
  { id: "2", name: "GitHub", url: "https://github.com", category: "work" },
  { id: "3", name: "Twitter", url: "https://twitter.com", category: "personal" },
  { id: "4", name: "MDN Docs", url: "https://developer.mozilla.org", category: "reference" },
  { id: "5", name: "Stack Overflow", url: "https://stackoverflow.com", category: "reference" },
];

export default function Command() {
  // Optional: fetch data for the menu bar
  const { isLoading } = useFetch("https://api.example.com/status", {
    execute: false, // Don't actually fetch in this example
  });

  const workBookmarks = bookmarks.filter((b) => b.category === "work");
  const personalBookmarks = bookmarks.filter((b) => b.category === "personal");
  const referenceBookmarks = bookmarks.filter((b) => b.category === "reference");

  return (
    <MenuBarExtra
      icon={Icon.Bookmark}
      title={`${bookmarks.length}`} // Optional: show count next to icon
      isLoading={isLoading}
      tooltip="Quick Bookmarks"
    >
      {/* Work Section */}
      <MenuBarExtra.Section title="Work">
        {workBookmarks.map((bookmark) => (
          <MenuBarExtra.Item
            key={bookmark.id}
            icon={Icon.Link}
            title={bookmark.name}
            subtitle={bookmark.url}
            onAction={() => open(bookmark.url)}
          />
        ))}
      </MenuBarExtra.Section>

      {/* Personal Section */}
      <MenuBarExtra.Section title="Personal">
        {personalBookmarks.map((bookmark) => (
          <MenuBarExtra.Item
            key={bookmark.id}
            icon={Icon.Link}
            title={bookmark.name}
            onAction={() => open(bookmark.url)}
          />
        ))}
      </MenuBarExtra.Section>

      {/* Reference as Submenu */}
      <MenuBarExtra.Section>
        <MenuBarExtra.Submenu title="Reference" icon={Icon.Book}>
          {referenceBookmarks.map((bookmark) => (
            <MenuBarExtra.Item
              key={bookmark.id}
              title={bookmark.name}
              onAction={() => open(bookmark.url)}
            />
          ))}
        </MenuBarExtra.Submenu>
      </MenuBarExtra.Section>

      {/* Actions Section */}
      <MenuBarExtra.Section>
        <MenuBarExtra.Item
          icon={Icon.Plus}
          title="Add Bookmark"
          shortcut={{ modifiers: ["cmd"], key: "n" }}
          onAction={async () => {
            // In a real extension, this would open a form
            await showHUD("Opening bookmark form...");
          }}
        />
        <MenuBarExtra.Item
          icon={Icon.Gear}
          title="Settings"
          onAction={async () => {
            await showHUD("Opening settings...");
          }}
        />
      </MenuBarExtra.Section>
    </MenuBarExtra>
  );
}

/*
 * Note: To use MenuBarExtra, configure your command in package.json with:
 *
 * {
 *   "commands": [
 *     {
 *       "name": "menubar-bookmarks",
 *       "title": "Quick Bookmarks",
 *       "description": "Access bookmarks from the menu bar",
 *       "mode": "menu-bar"
 *     }
 *   ]
 * }
 */
