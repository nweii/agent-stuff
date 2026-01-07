// ABOUTME: Example of a Raycast Grid for displaying image-focused content.
// ABOUTME: Shows column configuration, aspect ratios, and ActionPanel on grid items.

import { ActionPanel, Action, Grid, Color } from "@raycast/api";

interface Photo {
  id: string;
  title: string;
  url: string;
  category: string;
}

const photos: Photo[] = [
  { id: "1", title: "Mountain Landscape", url: "https://picsum.photos/id/10/800/600", category: "Nature" },
  { id: "2", title: "City Skyline", url: "https://picsum.photos/id/20/800/600", category: "Urban" },
  { id: "3", title: "Ocean Sunset", url: "https://picsum.photos/id/30/800/600", category: "Nature" },
  { id: "4", title: "Forest Path", url: "https://picsum.photos/id/40/800/600", category: "Nature" },
  { id: "5", title: "Desert Dunes", url: "https://picsum.photos/id/50/800/600", category: "Nature" },
  { id: "6", title: "Street Scene", url: "https://picsum.photos/id/60/800/600", category: "Urban" },
];

export default function Command() {
  return (
    <Grid
      columns={3}
      aspectRatio="16/9"
      fit={Grid.Fit.Fill}
      inset={Grid.Inset.Medium}
      searchBarPlaceholder="Search photos..."
    >
      <Grid.Section title="Nature" subtitle="Outdoor photography">
        {photos
          .filter((p) => p.category === "Nature")
          .map((photo) => (
            <Grid.Item
              key={photo.id}
              content={photo.url}
              title={photo.title}
              subtitle={photo.category}
              accessory={{ icon: { source: "checkmark.png", tintColor: Color.Green } }}
              actions={
                <ActionPanel>
                  <Action.OpenInBrowser title="View Full Size" url={photo.url} />
                  <Action.CopyToClipboard title="Copy URL" content={photo.url} />
                  <ActionPanel.Section title="Quick Actions">
                    <Action
                      title="Set as Wallpaper"
                      onAction={() => console.log(`Setting ${photo.title} as wallpaper`)}
                    />
                    <Action
                      title="Add to Favorites"
                      onAction={() => console.log(`Added ${photo.title} to favorites`)}
                    />
                  </ActionPanel.Section>
                </ActionPanel>
              }
            />
          ))}
      </Grid.Section>

      <Grid.Section title="Urban" subtitle="City photography">
        {photos
          .filter((p) => p.category === "Urban")
          .map((photo) => (
            <Grid.Item
              key={photo.id}
              content={photo.url}
              title={photo.title}
              subtitle={photo.category}
              actions={
                <ActionPanel>
                  <Action.OpenInBrowser title="View Full Size" url={photo.url} />
                  <Action.CopyToClipboard title="Copy URL" content={photo.url} />
                </ActionPanel>
              }
            />
          ))}
      </Grid.Section>
    </Grid>
  );
}
