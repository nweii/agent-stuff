// ABOUTME: Example of a Raycast Detail view with markdown content and metadata panel.
// ABOUTME: Shows how to display rich content with structured metadata on the right side.

import { Detail } from "@raycast/api";

// Define markdown separately to prevent unwanted indentation
const markdown = `
# Pikachu

![Pikachu](https://assets.pokemon.com/assets/cms2/img/pokedex/full/025.png)

Pikachu that can generate powerful electricity have cheek sacs that are extra soft and super stretchy.

## Evolution Line

1. **Pichu** (Baby)
2. **Pikachu** (Base)
3. **Raichu** (Final)

## Fun Facts

- Pikachu is the mascot of the Pokémon franchise
- Its name comes from the Japanese words "pika" (sparkle) and "chu" (squeak)
- First appeared in Pokémon Red and Blue (1996)

\`\`\`
Type: Electric
Generation: I
National Dex: #025
\`\`\`
`;

export default function Command() {
  return (
    <Detail
      markdown={markdown}
      navigationTitle="Pikachu"
      metadata={
        <Detail.Metadata>
          <Detail.Metadata.Label title="National Dex" text="#025" />
          <Detail.Metadata.Label title="Height" text="1' 04&quot;" />
          <Detail.Metadata.Label title="Weight" text="13.2 lbs" />

          <Detail.Metadata.Separator />

          <Detail.Metadata.TagList title="Type">
            <Detail.Metadata.TagList.Item text="Electric" color="#F7D02C" />
          </Detail.Metadata.TagList>

          <Detail.Metadata.TagList title="Abilities">
            <Detail.Metadata.TagList.Item text="Static" color="#A8A878" />
            <Detail.Metadata.TagList.Item text="Lightning Rod" color="#F8D030" />
          </Detail.Metadata.TagList>

          <Detail.Metadata.Separator />

          <Detail.Metadata.Label title="Base Experience" text="112" />
          <Detail.Metadata.Label title="Catch Rate" text="190" />
          <Detail.Metadata.Label title="Growth Rate" text="Medium Fast" />

          <Detail.Metadata.Separator />

          <Detail.Metadata.Link
            title="Pokémon.com"
            target="https://www.pokemon.com/us/pokedex/pikachu"
            text="View on Pokémon.com"
          />

          <Detail.Metadata.Link
            title="Bulbapedia"
            target="https://bulbapedia.bulbagarden.net/wiki/Pikachu"
            text="View on Bulbapedia"
          />
        </Detail.Metadata>
      }
    />
  );
}
