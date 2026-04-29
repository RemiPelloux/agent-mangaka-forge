# Img-Memory

This folder stores recurring manga visual references.

Do not delete asset folders between page generations. The `generatemangapage` skill uses this memory to preserve faces, hair, costumes, body proportions, transformations, evolutions, locations, props, and visual continuity across pages.

Expected structure:

```text
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

Use a new version folder for every persistent costume, injury, transformation, monster evolution, age state, or alternate-world design. Never overwrite `versions/base`.
