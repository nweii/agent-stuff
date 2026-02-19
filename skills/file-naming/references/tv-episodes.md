# TV Episode Naming

For TV show files, use standardized Plex/media manager format.

## Convention

- **Format**: `Show Name - sXXeYY - Episode Title.extension`
- **Season/Episode**: Always use two digits and lowercase (e.g., s01e05 instead of S1E5)
- **Clean up**: Remove release group tags, quality markers (1080p, x264), and unnecessary technical metadata

## Process

1. List the files in the target directory or use the provided list
2. Extract the Show Name, Season, and Episode from the existing filenames
3. Propose a preview table: "Original" | "Proposed"
4. Wait for confirmation before executing the rename

If the episode title cannot be determined, use `Show Name - sXXeYY.extension`.
