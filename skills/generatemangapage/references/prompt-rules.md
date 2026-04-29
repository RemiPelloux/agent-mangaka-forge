# Manga Prompt Rules

Use this file when writing manga page prompts by hand.

Do not delegate creative prompt writing to a script. The agent owns the page plan, composition, and final image prompt.

## Global Page Rules

Always keep these constraints:

- create one complete manga page unless the user asks for multiple pages
- use clear panel borders and clean gutters
- keep reading direction explicit
- preserve character identity from `img-memory`
- use no text unless the user provides exact wording
- no fake lettering, no labels, no UI, no watermark, no signature
- no random background characters unless the page needs a crowd
- keep action readable from panel to panel
- use intentional camera variety instead of repeating the same shot

## Character Reference Rules

Use these rules whenever a page includes a recurring character:

- Make all relevant memory images visible to built-in image generation first.
- In the prompt, say `use the images just shown as the visual references`.
- Name every character, asset group, and version, then bind each version to visible identity markers.
- Preserve face shape, eye design, hair silhouette, costume, accessories, body proportions, and signature marks.
- Allow only the page-specific changes: pose, expression, camera angle, lighting, damage, sweat, dirt, motion, or temporary props.
- Never merge two characters' features.
- Never change a costume unless the user explicitly requests a costume change; if changed, create a new `variant` version first.
- For evolutions, preserve lineage markers from the base version while making the evolved form visually distinct and repeatable.

## Manga Page Quality Rules

The page must feel professionally staged:

- strong first read at thumbnail size
- clear page focal point
- deliberate panel size hierarchy
- readable silhouettes in every action panel
- consistent character scale within a scene
- backgrounds that support the scene without overpowering characters
- screen tones and black fills used for mood, not random texture
- speed lines and impact effects must follow the action direction
- close-ups must still preserve the character's face identity

## Panel Planning Pattern

Write the page plan before the image prompt:

1. Page purpose: what the page must communicate.
2. Reading direction and panel count.
3. Panel-by-panel beat list.
4. Character asset groups, versions, and identity references used.
5. Text policy.
6. Final page prompt.

## Prompt Pattern

Use this structure for the final image prompt:

```text
Create one finished manga page.
Reading direction: <right_to_left or left_to_right>.
Format: <page size / aspect ratio>.
Style: <ink style, tone, screentone level>.
Use the images just shown as visual references for the characters.
Character consistency rules: <identity markers per character>.
Panel layout: <panel count and hierarchy>.
Panel 1: <camera, characters, action, emotion, background>.
Panel 2: <camera, characters, action, emotion, background>.
...
Text policy: <no text / exact text only / empty speech bubbles>.
Quality rules: clean gutters, professional manga composition, no fake text, no watermark.
```

## Text Policy

Default to `no_text`.

If the user provides exact dialogue:

- include only that exact dialogue
- keep lettering areas clean and readable
- do not invent extra words

If the user asks to add text later:

- generate empty speech bubbles or clean lettering-safe space
- keep final lettering as a separate step when possible

## Page Type Rules

### Story Page

Use balanced panel flow:

- establish location
- show character intent
- advance one clear action or emotional beat
- end with a visual hook when possible

### Battle Page

Use stronger diagonal motion and impact hierarchy:

- one dominant impact panel
- clear attacker and target positions
- visible action path
- consistent injuries and costume damage

### Dialogue Page

Keep acting strong:

- varied close-up and medium shots
- readable expressions
- controlled background detail
- leave clean bubble space if text is requested

### Cover

No panel grid unless requested:

- iconic full-page composition
- title-safe space if needed
- strongest character identity
- clear series tone

## Regeneration Triggers

Regenerate or revise when:

- a character no longer matches `img-memory`
- panel order is ambiguous
- anatomy is broken in a hero shot
- generated text appears unintentionally
- a panel becomes a random illustration instead of the requested story beat
- the same character looks like a different person between panels
