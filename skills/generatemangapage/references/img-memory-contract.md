# Img-Memory Contract

`img-memory` is the source of truth for recurring manga visuals.

The agent must create or update this structure before generating pages with recurring characters, monsters, locations, or props.

## Root Structure

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
          <variant-or-evolution-slug>/
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

## Asset Groups

Use asset groups to avoid a flat, unmaintainable memory library:

- `main-characters`: protagonists, rivals, major antagonists, and recurring core cast.
- `side-characters`: supporting characters, villagers, merchants, guards, and one-arc companions.
- `monsters`: recurring creatures, bosses, summons, pets, and monster evolution lines.
- `locations`: recurring places that need stable architecture or layout.
- `props`: signature weapons, relics, vehicles, artifacts, and recurring objects.

Custom groups are allowed when a project needs them, but keep names stable and slug-like.

## Versions, Variants, And Evolutions

Every recurring character or asset lives under `versions/<version-slug>/`.

Use `base` for the original stable design. Create a new version for every persistent visual state:

- alternate costume
- armor upgrade
- weapon set
- injury state
- older or younger timeline version
- transformed state
- monster evolution stage
- disguise
- awakened power form

Allowed version types:

- `base`: the original canonical design.
- `variant`: same character with a persistent costume, injury, age, disguise, or equipment change.
- `evolution`: a transformed, powered-up, or evolved form that must preserve visible lineage markers.

Do not overwrite `base`. A new design that may reappear later must be saved as its own version.

## Required Character Version Images

Every recurring character version needs:

- `portrait-front.png`: stable face, eyes, hair, and expression baseline.
- `full-body-front.png`: height, body proportions, costume, accessories.
- `turnaround-sheet.png`: front, side, back, and three-quarter views.
- `expression-sheet.png`: stable face across multiple expressions.
- `pose-sheet.png`: stable body and costume across action poses.

## Character Manifest

Each character folder must include a character-level `manifest.json`:

```json
{
  "name": "Aiko",
  "slug": "aiko",
  "asset_group": "main-characters",
  "description": "young dungeon mangaka heroine",
  "identity_markers": [
    "short black bob haircut",
    "round determined eyes",
    "ink-stained jacket"
  ],
  "versions": {
    "base": {
      "version_type": "base",
      "path": "assets/main-characters/aiko/versions/base",
      "description": "young dungeon mangaka heroine"
    },
    "awakened-ink-form": {
      "version_type": "evolution",
      "path": "assets/main-characters/aiko/versions/awakened-ink-form",
      "description": "same character after awakening ink-dungeon powers"
    }
  },
  "notes": []
}
```

Each version folder must include a version-level `manifest.json`:

```json
{
  "name": "Aiko",
  "character_slug": "aiko",
  "asset_group": "main-characters",
  "version": "awakened-ink-form",
  "version_type": "evolution",
  "description": "same face and haircut, darker ink aura, evolved jacket markings",
  "identity_markers": [
    "short black bob haircut",
    "round determined eyes",
    "ink-stained jacket",
    "black ink aura"
  ],
  "inherits_from": "base",
  "required_images": {
    "portrait-front.png": "present",
    "full-body-front.png": "present",
    "turnaround-sheet.png": "present",
    "expression-sheet.png": "present",
    "pose-sheet.png": "present"
  }
}
```

## Missing Memory Rule

If any required image is missing for the selected version:

1. Stop page generation.
2. Generate the missing version reference sheet with built-in image generation.
3. Save the image in `img-memory/assets/<asset-group>/<character-slug>/versions/<version-slug>/`.
4. Register it in the version manifest.
5. Make it visible before generating the manga page.

## Evolution Rule

Evolutions must be visually new but still traceable to the base design.

Preserve at least two lineage markers, such as:

- face shape or eye design
- hair silhouette or horn shape
- signature symbol, scar, accessory, or weapon
- body proportion family
- costume motif or material language

The evolved version should have its own full reference set. Do not rely on only the base reference for an evolved page.

## Page Memory

Each generated page should record:

```json
{
  "page_id": "page-001",
  "characters": [
    {
      "asset_group": "main-characters",
      "character": "aiko",
      "version": "awakened-ink-form"
    }
  ],
  "memory_images_used": [
    "assets/main-characters/aiko/versions/awakened-ink-form/portrait-front.png",
    "assets/main-characters/aiko/versions/awakened-ink-form/full-body-front.png"
  ],
  "scene_state": "Aiko enters the dungeon gate after awakening",
  "output_image": "outputs/manga-pages/chapter-001/page-001.png"
}
```

This page record lets future pages preserve injuries, props, costumes, evolutions, and story continuity.
