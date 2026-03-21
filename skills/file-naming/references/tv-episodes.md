# TV Episode Naming

For TV show files, use standardized Plex/media manager format.

## Convention

- **Format**: `Show Name - sXXeYY - Episode Title.extension`
- **Season/Episode**: Always use two digits and lowercase (e.g., s01e05 instead of S1E5)
- **Clean up**: Remove release group tags, quality markers (1080p, x264), and unnecessary technical metadata

## Finding episode titles

Look up titles in this order:
1. Wikipedia ("[Show]" or "List of [Show] episodes")
2. TheTVDB
3. IMDb

If sources conflict, prefer TheTVDB as it's the standard Plex metadata source.

If a show's episodes are confirmed to have no titles across all sources, use `Show Name - sXXeYY.extension` and note this to the user.

If titles are ambiguous or sources are inconsistent, ask the user before proceeding.

## Specials and extras

Plex convention for specials is `s00eXX` (season 00).

Before assuming specials are missing, ask the user whether they have those files — don't silently skip them or treat their absence as an error.

## Process

1. List the files in the target directory or use the provided list
2. Extract the Show Name, Season, and Episode from the existing filenames
3. Look up episode titles using the sources above; ask the user if titles can't be confidently determined
4. Follow the general rename process in SKILL.md from here
