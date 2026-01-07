// ABOUTME: Example of a Raycast List with detail panel showing metadata for selected items.
// ABOUTME: Uses isShowingDetail prop and List.Item.Detail for rich content display.

import { useState } from "react";
import { Action, ActionPanel, List } from "@raycast/api";

interface Pokemon {
  name: string;
  height: number;
  weight: number;
  id: string;
  types: string[];
  abilities: string[];
}

const pokemons: Pokemon[] = [
  {
    name: "Bulbasaur",
    height: 7,
    weight: 69,
    id: "001",
    types: ["Grass", "Poison"],
    abilities: ["Overgrow", "Chlorophyll"],
  },
  {
    name: "Charmander",
    height: 6,
    weight: 85,
    id: "004",
    types: ["Fire"],
    abilities: ["Blaze", "Solar Power"],
  },
  {
    name: "Squirtle",
    height: 5,
    weight: 90,
    id: "007",
    types: ["Water"],
    abilities: ["Torrent", "Rain Dish"],
  },
];

export default function Command() {
  const [showingDetail, setShowingDetail] = useState(true);

  return (
    <List isShowingDetail={showingDetail}>
      {pokemons.map((pokemon) => (
        <List.Item
          key={pokemon.id}
          title={pokemon.name}
          subtitle={`#${pokemon.id}`}
          icon={`https://assets.pokemon.com/assets/cms2/img/pokedex/detail/${pokemon.id}.png`}
          detail={
            <List.Item.Detail
              markdown={`
# ${pokemon.name}

![${pokemon.name}](https://assets.pokemon.com/assets/cms2/img/pokedex/full/${pokemon.id}.png)

A classic Pokémon from Generation 1.
              `}
              metadata={
                <List.Item.Detail.Metadata>
                  <List.Item.Detail.Metadata.Label title="Height" text={`${pokemon.height / 10}m`} />
                  <List.Item.Detail.Metadata.Label title="Weight" text={`${pokemon.weight / 10}kg`} />
                  <List.Item.Detail.Metadata.Separator />
                  <List.Item.Detail.Metadata.TagList title="Types">
                    {pokemon.types.map((type) => (
                      <List.Item.Detail.Metadata.TagList.Item key={type} text={type} />
                    ))}
                  </List.Item.Detail.Metadata.TagList>
                  <List.Item.Detail.Metadata.TagList title="Abilities">
                    {pokemon.abilities.map((ability) => (
                      <List.Item.Detail.Metadata.TagList.Item key={ability} text={ability} />
                    ))}
                  </List.Item.Detail.Metadata.TagList>
                </List.Item.Detail.Metadata>
              }
            />
          }
          actions={
            <ActionPanel>
              <Action
                title={showingDetail ? "Hide Detail" : "Show Detail"}
                onAction={() => setShowingDetail(!showingDetail)}
              />
              <Action.OpenInBrowser
                title="View on Pokémon.com"
                url={`https://www.pokemon.com/us/pokedex/${pokemon.name.toLowerCase()}`}
              />
            </ActionPanel>
          }
        />
      ))}
    </List>
  );
}
