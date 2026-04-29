# Manga Page Modes

Use this file when the user's request leaves room for multiple page plans.

## Page Types

- `story_page`: default manga page with scene progression.
- `cover`: single iconic illustration for chapter or volume presentation.
- `splash_page`: one full-page moment, usually an arrival, reveal, or impact.
- `character_intro`: page designed to introduce or reintroduce a character.
- `battle_page`: action-heavy page with combat continuity.
- `dialogue_page`: acting-heavy page with conversation pacing.
- `transition_page`: travel, time skip, location change, or quiet setup.

## Reading Direction

- `right_to_left`: default for manga unless the project says otherwise.
- `left_to_right`: use when the user asks for western comic flow or project consistency.

## Page Formats

- `print_manga_b5`: default page format for manga pages.
- `webtoon_slice`: vertical scrolling layout; use only when requested.
- `square_preview`: social preview or thumbnail.
- `custom`: use the user's explicit dimensions.

## Ink Styles

- `clean_black_white`: default professional manga line art with controlled blacks.
- `screentone`: classic manga tones for depth, mood, and value separation.
- `high_contrast`: strong black fills, dramatic lighting, action emphasis.
- `sketchy_ink`: rougher energetic line work; use only when requested.
- `color_manga`: colored manga/manhwa look; use only when requested.

## Panel Defaults

- quiet story beat: 4-5 panels
- dialogue page: 5-7 panels
- battle page: 3-5 panels with one dominant impact panel
- reveal page: 1-3 panels
- transition page: 3-6 panels

## Layout Hints

- Opening page: use an establishing panel first unless the user wants an immediate cold open.
- Emotional reveal: use a close-up or silent reaction panel.
- Attack setup: wide shot for positions, medium shot for action start, large panel for impact.
- Chase or travel: repeat directional movement consistently across panels.
- Mystery or horror: slow panel rhythm, more negative space, stronger blacks.

## Character Memory Mapping

Map vague phrases to stable memory behavior:

- "same hero as before" -> find the existing hero under `img-memory/assets/main-characters/<slug>/versions/base`
- "new main character" -> create `img-memory/assets/main-characters/<slug>/versions/base`
- "new side character" -> create `img-memory/assets/side-characters/<slug>/versions/base`
- "different outfit" -> create a new `variant` version before page generation
- "injured version" -> create a new `variant` if the injury persists across pages; otherwise record temporary injury state in page metadata
- "older/younger version" -> create a timeline `variant`; do not overwrite the base character
- "transformed / evolved / awakened form" -> create an `evolution` version that preserves visible lineage markers
- "monster evolution line" -> store each stage under `img-memory/assets/monsters/<slug>/versions/<stage-slug>`

## Output Shape

For each final page:

- final page image
- page plan
- prompt used
- metadata JSON
- page memory JSON under `img-memory/pages`

For each new character version:

- character manifest
- version manifest
- portrait-front
- full-body-front
- turnaround-sheet
- expression-sheet
- pose-sheet
