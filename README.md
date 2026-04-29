# Agent Mangaka Forge

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![GitHub repo](https://img.shields.io/badge/GitHub-RemiPelloux%2Fagent--mangaka--forge-black)](https://github.com/RemiPelloux/agent-mangaka-forge)
[![AI Manga Workflow](https://img.shields.io/badge/AI%20Manga-character%20consistency-purple)](#character-image-memory)

> AI manga page generation skill pack with persistent character image memory.

Agent Mangaka Forge helps AI coding agents generate manga pages, chapter pages, covers, and storyboard pages while keeping recurring characters visually consistent. It adds a strict `img-memory` workflow: missing character reference sheets are generated first, saved locally, and reused as visual references before each page generation.

Keywords: AI manga generator, manga page generator, manga character consistency, image memory, AI comic generator, manga storyboard, Cursor skills, Codex skills, generative art workflow.
Also supports character evolution, transformation versions, costume variations, monster evolution lines, and organized manga asset libraries.

## Why This Exists

Most AI image workflows can create a strong single manga panel, but they drift across pages. Faces change, costumes mutate, and the same hero becomes a different character after a few generations.

Agent Mangaka Forge fixes that at the workflow level:

- Every recurring character gets a stable `img-memory` folder.
- The agent blocks page generation until required character references exist.
- Page prompts explicitly bind visible reference images to named characters.
- Page metadata records which character images were used for continuity.

## Features

- Generate manga pages with professional panel flow, gutters, camera staging, and readable action.
- Preserve character identity across pages using portrait, full-body, turnaround, expression, and pose references.
- Create missing character reference sheets automatically before final page generation.
- Organize character memory by asset group, version, variant, and evolution stage.
- Support story pages, battle pages, dialogue pages, covers, splash pages, character intros, and transitions.
- Enforce text safety: no fake lettering unless the user provides exact dialogue or asks for placeholders.
- Store continuity metadata for pages, characters, costumes, variants, injuries, and scene state.
- Ship a dependency-free Python helper for validating and registering `img-memory`.

## Repository Layout

```text
agent-mangaka-forge/
  README.md
  README.zh-TW.md
  LICENSE
  requirements.txt
  img-memory/
    README.md
    assets/
      main-characters/
    pages/
  skills/
    generatemangapage/
      SKILL.md
      agents/
        openai.yaml
      references/
        img-memory-contract.md
        modes.md
        prompt-rules.md
      scripts/
        manage_img_memory.py
```

## Install

### Option 1: Clone The Repository

```bash
git clone https://github.com/RemiPelloux/agent-mangaka-forge.git
cd agent-mangaka-forge
```

No Python package installation is required for the helper script. It uses only the Python standard library.

### Option 2: Install The Skill For Codex

```bash
mkdir -p ~/.codex/skills
cp -R ./skills/generatemangapage ~/.codex/skills/
```

Restart your Codex session after copying the skill.

### Option 3: Use In Cursor Or Another Agent Workspace

Keep the repository in your project and reference the skill directly:

```text
Use $generatemangapage to create page 1 of my manga.
Characters: Aiko, Ryu.
If any character is missing from img-memory, generate their reference sprites first.
Then generate the final manga page using the stored references.
```

## Quick Start

Initialize image memory:

```bash
python3 ./skills/generatemangapage/scripts/manage_img_memory.py init --project "Dungeonia Manga"
```

Create or refresh a character manifest:

```bash
python3 ./skills/generatemangapage/scripts/manage_img_memory.py ensure-character \
  --name "Aiko" \
  --group main-characters \
  --description "young dungeon mangaka heroine with an ink-stained jacket" \
  --identity-markers "short black bob haircut, round determined eyes, ink-stained jacket"
```

Create an evolution or variation without overwriting the base design:

```bash
python3 ./skills/generatemangapage/scripts/manage_img_memory.py ensure-character \
  --name "Aiko" \
  --group main-characters \
  --version awakened-ink-form \
  --version-type evolution \
  --description "Aiko after awakening ink-dungeon powers" \
  --version-description "same face and haircut, darker ink aura, evolved jacket markings, sharper battle silhouette" \
  --identity-markers "short black bob haircut, round determined eyes, ink-stained jacket, black ink aura"
```

Check missing reference images:

```bash
python3 ./skills/generatemangapage/scripts/manage_img_memory.py missing --characters "Aiko,Ryu"
```

Ask the agent to generate a page:

```text
Use $generatemangapage to create a right-to-left black-and-white manga page.
Page beat: Aiko and Ryu discover the sealed dungeon gate.
Tone: dark fantasy shonen.
Panel count: 5.
No text.
Generate missing character memory first, then use img-memory references for the final page.
```

## Character Image Memory

`img-memory` is the source of truth for recurring character visuals:

```text
img-memory/
  manifest.json
  assets/
    main-characters/
      <character-slug>/
        manifest.json
        versions/
          base/
            manifest.json
            portrait-front.png
            full-body-front.png
            turnaround-sheet.png
            expression-sheet.png
            pose-sheet.png
          awakened-ink-form/
            manifest.json
            portrait-front.png
            full-body-front.png
            turnaround-sheet.png
            expression-sheet.png
            pose-sheet.png
    side-characters/
    monsters/
    locations/
    props/
  pages/
    page-001.json
```

Use asset groups to keep the project clean:

- `main-characters`: heroes, rivals, long-running protagonists, and major antagonists.
- `side-characters`: villagers, merchants, one-arc companions, guards, and supporting roles.
- `monsters`: recurring creatures, bosses, summons, and transformed enemies.
- `locations`: important places that need repeated visual continuity.
- `props`: signature weapons, artifacts, vehicles, relics, and recurring items.

Each character can have multiple versions:

```text
versions/
  base/
  school-uniform/
  dungeon-armor/
  awakened-ink-form/
  injured-after-boss-fight/
```

Versions can be `base`, `variant`, or `evolution`. Never overwrite `base` when the story introduces a new outfit, injury state, transformation, age, power-up, or evolved form.

Legacy flat folders are intentionally avoided:

```text
img-memory/
  assets/
    <asset-group>/
      <character-slug>/
        versions/
          <version-slug>/
```

Before generating a page, the skill must:

1. Identify every recurring character in the page request.
2. Identify the correct asset group and version for each character.
3. Check whether each selected version has a complete `img-memory` folder.
4. Generate missing character reference sprites or sheets first.
5. Show the relevant memory images to image generation.
6. Generate the final manga page from those visible references.
7. Save page metadata under `img-memory/pages`.

## Required Character References

Each recurring character version should have:

- `portrait-front.png`: face, eyes, hair, and expression baseline.
- `full-body-front.png`: body proportions, costume, symbols, and accessories.
- `turnaround-sheet.png`: front, side, back, and three-quarter views.
- `expression-sheet.png`: stable face across multiple expressions.
- `pose-sheet.png`: stable body and costume across action poses.

If any required image is missing, the skill must stop page generation and create the missing memory asset first.

## Evolutions And Variations

Character evolution is first-class. Use a new version when a character changes in a way that must remain stable later:

- new costume or armor
- power-up or transformed state
- monster evolution stage
- older or younger timeline version
- injury or scar state that lasts across pages
- alternate-world design
- temporary disguise that appears more than once

An evolved version must preserve lineage markers from the base version. The face, hair family, symbolic marks, proportions, or signature accessories should make it obvious that the evolved form belongs to the same character.

Example evolution structure:

```text
img-memory/assets/main-characters/aiko/
  manifest.json
  versions/
    base/
      manifest.json
      portrait-front.png
      full-body-front.png
      turnaround-sheet.png
      expression-sheet.png
      pose-sheet.png
    awakened-ink-form/
      manifest.json
      portrait-front.png
      full-body-front.png
      turnaround-sheet.png
      expression-sheet.png
      pose-sheet.png
```

## CLI Helper

The helper manages metadata only. It does not call an image API and does not generate artwork.

```bash
python3 ./skills/generatemangapage/scripts/manage_img_memory.py --help
```

Available commands:

- `init`: create the `img-memory` folder structure.
- `ensure-character`: create or refresh a character version manifest.
- `register-image`: copy a generated reference image into a character version memory slot.
- `missing`: report missing character version reference images.
- `record-page`: record page continuity metadata.

Register a generated reference image:

```bash
python3 ./skills/generatemangapage/scripts/manage_img_memory.py register-image \
  --name "Aiko" \
  --group main-characters \
  --version base \
  --kind portrait-front.png \
  --image ./generated/aiko-portrait.png
```

Record a generated page:

```bash
python3 ./skills/generatemangapage/scripts/manage_img_memory.py record-page \
  --page-id page-001 \
  --characters "Aiko,Ryu" \
  --group main-characters \
  --version base \
  --scene-state "Aiko and Ryu discover the sealed dungeon gate" \
  --output-image outputs/manga-pages/chapter-001/page-001.png
```

## Page Generation Rules

The skill enforces these production rules:

- Use one finished manga page per generation unless the user asks for a batch.
- Preserve character identity: face shape, eyes, hair silhouette, costume, accessories, body proportions, and signature marks.
- Keep panel order readable for the selected reading direction.
- Use clean gutters, deliberate camera staging, and a clear focal hierarchy.
- Do not invent dialogue. Use no text by default.
- Regenerate if a character is visually redesigned between panels or pages.

## GitHub Topics

Recommended public repository topics:

```text
ai-manga, manga-generator, comic-generator, character-consistency, image-memory, ai-art, generative-ai, cursor-skills, codex-skills, manga-workflow, character-evolution
```

## SEO Description

Agent Mangaka Forge is an AI manga page generation workflow for Cursor, Codex, and agentic image generation systems. It focuses on consistent manga characters across pages by maintaining reusable image memory for portraits, full-body references, turnarounds, expressions, poses, character evolutions, costume variations, monster evolution lines, and page continuity metadata.

## License

MIT. See [LICENSE](./LICENSE).
