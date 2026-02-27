# Changelog

All notable changes to one-file-quiz are documented here.

---

## [1.2.1] – 2026-02-27

### UI polish

- **q-meta restructured** – left: star, center: correct answer count, right: `#N` question number (cyan)
- **Hints row** – key name centered above description for each shortcut; layout no longer breaks with longer UI strings
- **`qOrigNum` label removed** – topic/number info was redundant with Topics dropdown and index

---

## [1.2.0] – 2026-02-27

### Features

- **Favourites system** – star icon on each question (meta line, left) and in the index; click to add/remove; persisted in localStorage (`storageKey_favorites`)
- **Favourites mode** – new mode button to quiz only favourited questions
- **Index: favourite column** – star column far left, clickable; sorts favourites to top
- **Index: sortable columns** – all columns sortable: `★`, `#`, Question, Topic, Score
- **Score column: 4 states** – good (green), bad (orange), 50/50 (grey), unanswered (dash)
- **Keyboard: 1–0 for up to 10 answers** – `0` selects answer 10
- **Keyboard: Space = Check / Next** – replaces Enter for confirm/advance
- **Keyboard: Enter = toggle favourite** – works at any time outside the index
- **Language support** – `"lang"` field in JSON (`"de"` or `"en"`); generator replaces all UI placeholders at build time; no runtime switching, no mixed-language output
- **CSS variable `--fav`** – `#f0b429` (gold) for favourite accents

### UI polish

- **Mode bar** – 4-zone layout: `[Index] [current mode] [▾ Mode menu] [Topics]`
- **Mode menu** – dropdown with question counts per mode; active dropdown button turns cyan; Mistakes entry highlighted orange
- **Mistakes count** – live count in dropdown (all questions that are not net-positive)
- **Favourites count** – updates live in dropdown when toggling stars anywhere
- **Index info row** – 2-cell layout: question count left, generated date right
- **Index header** – separator line below column headers matching row spacing
- **Index: score sort** – click 1 = negatives first, click 2 = positives first
- **Consistent hover system** – PDF/Clear history: fill on hover; Index/Mode/Topics buttons: cyan border + text on hover, no fill; dropdown items: cyan text on hover
- **Star rendering** – always filled glyph `★`, colour controls state (grey/gold); no layout shift between states
- **Typography** – 0.9rem throughout index and meta lines, 0.8rem buttons, `letter-spacing: 0.1em` everywhere; index question text 1.0rem
- **Result screen** – Try Again button styled like toolbar buttons; `letter-spacing: 0.1em` on score display
- **Footer links** – permanently cyan, no hover effect
- **Score display** – format `correct / wrong`, no ✓/✗ symbols; 50/50 shown in grey

### Fixes

- Dead `btnFavMode` references removed from `toggleIndexFav`, `toggleFavCurrent`, `clearStorage`
- `wrongAnswered` and `wrongSet` state variables removed (populated but never read)
- Dead `setMode()` function removed
- Dead `screen-overview` / `.ov-*` CSS and `@media print` block removed
- `from collections import Counter` moved to module-level imports in generator
- `getModeLabel()` function declaration restored after refactor breakage

### Removed

- Topics line from header (was redundant with Topics dropdown)

### Breaking changes

- JSON requires `"lang"` field (`"de"` or `"en"`). Files without it are skipped with an error.
- Keyboard: Enter no longer confirms answers (use Space instead).

---

## [1.1.1] – 2026-02-26

### Features

- Batch processing: script now processes all JSON files in `sources/` automatically
- Auto-generated `num` and `label` – no longer required in JSON source files
- Output filename derived from quiz title (kebab-case)
- `topic` replaces `source` field

### Fixes

- Topics dropdown was counting 0 (JS filter updated)
- Hint toggle added to keyboard bar
- Consistent key order in JSON format and documentation
- German comment removed from template

### Breaking changes

- JSON format changed: `num`, `label`, `source` are no longer valid fields. Use `topic` instead.

---

## [1.0.0] – 2026-02-25

Initial release of one-file-quiz.

A self-contained, single-file quiz tool built with vanilla HTML, CSS and JavaScript.
No backend, no dependencies, no installation. Generate a quiz from a JSON source file
and open it in any browser.

Includes a Python generator script, two demo question sets, and full documentation.
