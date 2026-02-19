// ABOUTME: Example of a Raycast List with ActionPanel including sections and submenus.
// ABOUTME: Demonstrates common action patterns: open URL, copy, and custom actions.

import { Action, ActionPanel, Color, Icon, List } from "@raycast/api";

export default function Command() {
  return (
    <List navigationTitle="Open Pull Requests">
      <List.Item
        title="Docs: Update API Reference"
        subtitle="#1"
        icon={Icon.Document}
        accessories={[{ tag: { value: "docs", color: Color.Blue } }]}
        actions={
          <ActionPanel title="#1 in raycast/extensions">
            {/* Primary action (Enter key) */}
            <Action.OpenInBrowser url="https://github.com/raycast/extensions/pull/1" />

            {/* Secondary action (Cmd+Enter) */}
            <Action.CopyToClipboard
              title="Copy Pull Request URL"
              content="https://github.com/raycast/extensions/pull/1"
            />

            {/* Grouped actions in a section */}
            <ActionPanel.Section title="Copy">
              <Action.CopyToClipboard title="Copy PR Number" content="#1" />
              <Action.CopyToClipboard title="Copy PR Title" content="Docs: Update API Reference" />
            </ActionPanel.Section>

            {/* Submenu for nested actions */}
            <ActionPanel.Submenu title="Add Label" icon={Icon.Tag}>
              <Action
                icon={{ source: Icon.Circle, tintColor: Color.Red }}
                title="Bug"
                onAction={() => console.log("Add bug label")}
              />
              <Action
                icon={{ source: Icon.Circle, tintColor: Color.Yellow }}
                title="Enhancement"
                onAction={() => console.log("Add enhancement label")}
              />
              <Action
                icon={{ source: Icon.Circle, tintColor: Color.Blue }}
                title="Help Wanted"
                onAction={() => console.log("Add help wanted label")}
              />
            </ActionPanel.Submenu>

            {/* Danger zone section */}
            <ActionPanel.Section title="Danger Zone">
              <Action
                title="Close Pull Request"
                icon={Icon.XMarkCircle}
                style={Action.Style.Destructive}
                onAction={() => console.log("Close PR #1")}
              />
            </ActionPanel.Section>
          </ActionPanel>
        }
      />
    </List>
  );
}
