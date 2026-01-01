# obsidian-cli extended reference

Extended documentation for [obsidian-cli](https://github.com/Yakitrak/obsidian-cli). See [SKILL.md](SKILL.md) for essential commands.

## Daily notes

Opens today's daily note, creating it from template if it doesn't exist:

```bash
obsidian-cli daily
obsidian-cli daily --vault "VaultName"
```

## Print note contents

Output a note's contents to stdout (useful for piping):

```bash
obsidian-cli print "Note"
obsidian-cli print "Folder/Note"
```

## Create/update options

```bash
# Basic create (opens in Obsidian)
obsidian-cli create "Folder/Note" --content "..." --open

# Overwrite existing note
obsidian-cli create "Note" --content "..." --overwrite

# Append to existing note
obsidian-cli create "Note" --content "..." --append
```

## Move/rename options

```bash
# Move and open result
obsidian-cli move "old/path" "new/path" --open

# Specify vault explicitly
obsidian-cli move "old/path" "new/path" --vault "VaultName"
```

## Frontmatter operations

```bash
# Print all frontmatter
obsidian-cli frontmatter "Note" --print

# Edit/create a field
obsidian-cli frontmatter "Note" --edit --key "status" --value "done"

# Delete a field
obsidian-cli frontmatter "Note" --delete --key "draft"
```

Alias: `obsidian-cli fm`

## Editor flag

The `--editor` flag opens notes in your terminal/GUI editor instead of Obsidian. Useful for quick edits or terminal-only environments.

```bash
# Search and open selection in editor
obsidian-cli search --editor
obsidian-cli search-content "query" --editor

# Create and open in editor
obsidian-cli create "Note" --content "..." --open --editor

# Move and open in editor
obsidian-cli move "old" "new" --open --editor
```

Editor is determined by `$EDITOR` environment variable (defaults to `vim`). Supported GUI editors (VSCode, Sublime, etc.) automatically get `--wait` flag.

```bash
# Set preferred editor (add to ~/.zshrc)
export EDITOR="code"  # or "vim", "nano", "subl", etc.
```

## Shell helper

Add to `~/.zshrc` for quick vault navigation:

```bash
obs_cd() {
    local result=$(obsidian-cli print-default --path-only)
    [ -n "$result" ] && cd -- "$result"
}
```

## Vault management

```bash
# Print default vault info
obsidian-cli print-default
obsidian-cli print-default --path-only

# Set default vault (by folder name, not path)
obsidian-cli set-default "Brain"
```

Obsidian stores vault config at `~/Library/Application Support/obsidian/obsidian.json`.

## Installation (reference)

If setting up on a new machine:

```bash
brew tap yakitrak/yakitrak
brew install obsidian-cli
obsidian-cli set-default "Brain"
```
