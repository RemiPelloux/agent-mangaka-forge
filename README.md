# Agent Mangaka Forge

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![GitHub repo](https://img.shields.io/badge/GitHub-RemiPelloux%2Fagent--mangaka--forge-black)](https://github.com/RemiPelloux/agent-mangaka-forge)
[![Codex Skill](https://img.shields.io/badge/Codex-skill%20ready-purple)](#install-in-codex)

> A Codex skill for generating manga pages while keeping characters consistent across pages, outfits, variants, and evolutions.

Agent Mangaka Forge is a manga production workflow for AI agents. It helps Codex generate manga pages, covers, chapter scenes, storyboards, and character-consistent panels by maintaining a reusable local visual memory called `img-memory`.

The main rule is simple:

> Do not generate a page with a recurring character until that character version has reference images in `img-memory`.

This prevents the usual AI drift where the same character changes face, hair, costume, body shape, or power-up design between pages.

## Table Of Contents

- [What It Does](#what-it-does)
- [Install In Codex](#install-in-codex)
- [Quick Start](#quick-start)
- [How To Use The Skill](#how-to-use-the-skill)
- [Character Image Memory](#character-image-memory)
- [Versions, Variants, And Evolutions](#versions-variants-and-evolutions)
- [CLI Helper](#cli-helper)
- [Repository Layout](#repository-layout)
- [Troubleshooting](#troubleshooting)
- [SEO Keywords](#seo-keywords)

## What It Does

Agent Mangaka Forge gives Codex a repeatable workflow for manga generation:

- Generate polished manga pages with panel flow, gutters, camera staging, and readable action.
- Keep recurring characters consistent with portrait, full-body, turnaround, expression, and pose references.
- Create missing character reference sheets before generating the final page.
- Store main characters, side characters, monsters, locations, and props in organized asset folders.
- Support `base`, `variant`, and `evolution` versions for each character.
- Preserve evolved forms, awakened forms, monster stages, costumes, injuries, and timeline versions.
- Record page metadata so future pages can keep visual and story continuity.
- Avoid fake text by default unless the user provides exact dialogue.

## Install In Codex

### 1. Clone The Repository

```bash
git clone https://github.com/RemiPelloux/agent-mangaka-forge.git
cd agent-mangaka-forge
```

### 2. Copy The Skill Into Codex

Codex loads skills from `~/.codex/skills`.

```bash
mkdir -p ~/.codex/skills
cp -R ./skills/generatemangapage ~/.codex/skills/
```

### 3. Restart Codex

Close the current Codex session and start a new one. Skills are loaded when the session starts.

### 4. Verify The Skill Is Available

In a new Codex session, ask:

```text
Use $generatemangapage to explain what this skill does.
```

If Codex recognizes the skill, installation is complete.

### 5. Optional: Install The Helper CLI In Your Project

The helper script uses only the Python standard library. No package install is required.

You can run it directly from the repository:

```bash
python3 ./skills/generatemangapage/scripts/manage_img_memory.py --help
```

Or copy the whole repository into a manga project and run the helper there.

## Codex Install Commands

Use this full copy-paste install block on macOS or Linux:

```bash
git clone https://github.com/RemiPelloux/agent-mangaka-forge.git
cd agent-mangaka-forge
mkdir -p ~/.codex/skills
rm -rf ~/.codex/skills/generatemangapage
cp -R ./skills/generatemangapage ~/.codex/skills/
python3 ./skills/generatemangapage/scripts/manage_img_memory.py --help
```

Then restart Codex.

Windows PowerShell:

```powershell
git clone https://github.com/RemiPelloux/agent-mangaka-forge.git
Set-Location agent-mangaka-forge
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.codex\skills" | Out-Null
Remove-Item -Recurse -Force "$env:USERPROFILE\.codex\skills\generatemangapage" -ErrorAction SilentlyContinue
Copy-Item -Recurse -Force ".\skills\generatemangapage" "$env:USERPROFILE\.codex\skills\"
python .\skills\generatemangapage\scripts\manage_img_memory.py --help
```

Then restart Codex.

## Update An Existing Codex Install

If you already installed the skill and want the latest version:

```bash
cd agent-mangaka-forge
git pull
rm -rf ~/.codex/skills/generatemangapage
cp -R ./skills/generatemangapage ~/.codex/skills/
```

Restart Codex after updating.

## Quick Start

Initialize image memory for a manga project:

```bash
python3 ./skills/generatemangapage/scripts/manage_img_memory.py init --project "Dungeonia Manga"
```

Create the base version of a main character:

```bash
python3 ./skills/generatemangapage/scripts/manage_img_memory.py ensure-character \
  --name "Aiko" \
  --group main-characters \
  --description "young dungeon mangaka heroine with an ink-stained jacket" \
  --identity-markers "short black bob haircut, round determined eyes, ink-stained jacket"
```

Check which required reference images are missing:

```bash
python3 ./skills/generatemangapage/scripts/manage_img_memory.py missing \
  --characters "Aiko" \
  --group main-characters \
  --version base
```

Ask Codex to create the missing references, then generate a page:

```text
Use $generatemangapage to create a right-to-left black-and-white manga page.

Project: Dungeonia Manga.
Page beat: Aiko discovers the sealed dungeon gate.
Characters: Aiko, main-characters, version base.
Tone: dark fantasy shonen.
Panel count: 5.
Text policy: no text.

Before generating the final page, inspect img-memory.
If Aiko is missing any required reference image, generate those references first.
Then use the visible img-memory references to generate the final manga page.
```

## How To Use The Skill

Use the skill by mentioning `$generatemangapage` in Codex.

Basic page prompt:

```text
Use $generatemangapage to generate page 1 of my manga.
Characters: Aiko and Ryu.
Asset group: main-characters.
Version: base.
Scene: they enter a ruined dungeon library.
Style: black-and-white manga, clean line art, screentone shadows.
Reading direction: right-to-left.
No text.
```

Battle page prompt:

```text
Use $generatemangapage for a battle page.
Characters:
- Aiko, main-characters, version awakened-ink-form
- Obsidian Wyrm, monsters, version elder-stage

Page beat: Aiko blocks the monster's attack with an ink shield.
Panel count: 4.
Tone: high-contrast dark fantasy shonen.
Text policy: no text.
Use existing img-memory references. Generate missing version references before the page if needed.
```

Dialogue page prompt:

```text
Use $generatemangapage to create a dialogue page.
Characters: Aiko and Ryu, main-characters, version base.
Scene: the campfire before entering the dungeon.
Panel count: 6.
Text policy: lettering placeholders only.
Leave clean speech bubble space, but do not invent dialogue.
```

## Character Image Memory

`img-memory` is the local visual memory used to keep characters consistent.

Recommended structure:

```text
img-memory/
  manifest.json
  assets/
    main-characters/
      aiko/
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

Each recurring character version should have:

- `portrait-front.png`: face, eyes, hair, and expression baseline.
- `full-body-front.png`: body proportions, costume, symbols, and accessories.
- `turnaround-sheet.png`: front, side, back, and three-quarter views.
- `expression-sheet.png`: stable face across multiple expressions.
- `pose-sheet.png`: stable body and costume across action poses.

The skill should stop and generate missing references before making a final manga page.

## Asset Groups

Use asset groups to keep the memory library readable:

- `main-characters`: protagonists, rivals, major antagonists, and core cast.
- `side-characters`: villagers, merchants, guards, arc companions, and supporting roles.
- `monsters`: recurring creatures, bosses, summons, pets, and monster evolution lines.
- `locations`: recurring places that need stable architecture, layout, or mood.
- `props`: weapons, artifacts, vehicles, relics, and other recurring objects.

Custom groups are allowed, but keep names stable and slug-like.

## Versions, Variants, And Evolutions

Every recurring character or asset lives inside a version folder.

Use `base` for the original design:

```text
img-memory/assets/main-characters/aiko/versions/base/
```

Create a new version for every persistent visual change:

- costume change
- armor upgrade
- weapon set
- injury or scar state
- older or younger timeline version
- disguise
- awakened form
- transformed state
- monster evolution stage

Version types:

- `base`: original canonical design.
- `variant`: same character with a persistent costume, injury, age, disguise, or equipment change.
- `evolution`: transformed, powered-up, or evolved form.

Important rule:

> Never overwrite `base`. If the design can appear again later, create a new version.

Example evolution:

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

An evolution must preserve lineage markers from the base design. The reader should still recognize the character.

## CLI Helper

The helper manages metadata and folder structure. It does not generate images.

Show all commands:

```bash
python3 ./skills/generatemangapage/scripts/manage_img_memory.py --help
```

Initialize memory:

```bash
python3 ./skills/generatemangapage/scripts/manage_img_memory.py init --project "Dungeonia Manga"
```

Create or update a character version:

```bash
python3 ./skills/generatemangapage/scripts/manage_img_memory.py ensure-character \
  --name "Aiko" \
  --group main-characters \
  --version base \
  --version-type base \
  --description "young dungeon mangaka heroine" \
  --identity-markers "short black bob haircut, round determined eyes, ink-stained jacket"
```

Register a generated reference image:

```bash
python3 ./skills/generatemangapage/scripts/manage_img_memory.py register-image \
  --name "Aiko" \
  --group main-characters \
  --version base \
  --kind portrait-front.png \
  --image ./generated/aiko-portrait.png
```

Check missing references:

```bash
python3 ./skills/generatemangapage/scripts/manage_img_memory.py missing \
  --characters "Aiko,Ryu" \
  --group main-characters \
  --version base
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
      side-characters/
      monsters/
      locations/
      props/
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

## Troubleshooting

### Codex does not find `$generatemangapage`

Check that the skill exists here:

```text
~/.codex/skills/generatemangapage/SKILL.md
```

Then restart Codex.

### The helper script fails

Use Python 3:

```bash
python3 ./skills/generatemangapage/scripts/manage_img_memory.py --help
```

No external Python dependency is required.

### A character changes design between pages

Make sure the page prompt names the exact asset group and version:

```text
Aiko, main-characters, version awakened-ink-form
```

Also make sure the reference images are visible to image generation before asking for the final page.

### A costume or power-up overwrote the base design

Do not overwrite `versions/base`. Create a new version:

```text
versions/dungeon-armor/
versions/awakened-ink-form/
versions/injured-after-boss-fight/
```

## SEO Keywords

AI manga generator, manga page generator, AI comic generator, manga storyboard generator, character consistency, image memory, Codex skill, Cursor skill, generative AI workflow, manga character evolution, manga character variants, AI manga production pipeline.

## License

MIT. See [LICENSE](./LICENSE).
