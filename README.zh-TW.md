# Agent Mangaka Forge

> 使用角色圖像記憶生成連貫、穩定、可演化的漫畫頁面。

Agent Mangaka Forge 是 Codex-first 的漫畫頁面生成技能包。核心規則很簡單：只要頁面中有重複登場角色，就必須先建立 `img-memory`，再用這些角色參考圖生成頁面。

## 可生成內容

- 漫畫頁、章節頁、封面與分鏡頁。
- 缺失角色的正面肖像、全身設定、轉面表情、姿勢表。
- 主角、配角、怪物、場景、道具等分類資產記憶。
- 角色服裝變體、受傷狀態、覺醒形態、怪物進化階段。
- 每頁的生成提示與生產 metadata。

## 圖像記憶結構

```text
img-memory/
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

`base` 是角色的原始設計。當角色換裝、受傷、成長、覺醒、變身或進化時，不要覆蓋 `base`，必須建立新的 version。

## 使用方式

```bash
python3 ./skills/generatemangapage/scripts/manage_img_memory.py init --project "Dungeonia Manga"
python3 ./skills/generatemangapage/scripts/manage_img_memory.py ensure-character \
  --name "Aiko" \
  --group main-characters \
  --description "young dungeon mangaka heroine" \
  --identity-markers "short black bob haircut, round determined eyes, ink-stained jacket"
```

建立進化版本：

```bash
python3 ./skills/generatemangapage/scripts/manage_img_memory.py ensure-character \
  --name "Aiko" \
  --group main-characters \
  --version awakened-ink-form \
  --version-type evolution \
  --description "Aiko after awakening ink-dungeon powers" \
  --version-description "same face and haircut, darker ink aura, evolved jacket markings"
```

生成頁面前，agent 必須確認每個角色的資產分類、version 與參考圖是否完整。若缺少角色 sprite 或設定圖，必須先生成並登記，再用它們作為可見參考圖生成漫畫頁。
