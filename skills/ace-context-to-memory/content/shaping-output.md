# Output Structure

## Memory Mode

- **Convert**: `memory/<name>/<rel>/converted/` (markdown + images)
- **Chunk**: `memory/<name>/<rel>/chunked/` (chunked markdown)
- **Organize**: `memory/<name>/chunked/` (hierarchical markdown for Excel story maps)

## Pipeline Mode (single-folder)

- **Convert**: `pipeline/converted/`
- **Chunk**: `pipeline/chunked/`

## Chunk Source Reference

Each chunk includes: `<!-- Source: path | file://url -->` for navigation.
