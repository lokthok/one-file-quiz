# Changelog

All notable changes to one-file-quiz are documented here.

---

## [1.3.0] – 2026-02-28

### Features

- **Quality tier system** – question progress is now visualised using four tiers inspired by MMO item quality. The tier is determined by the *net score* (correct minus wrong answers) of each question, not by the raw correct count. Tiers apply to the score column in the index and the question number `#N` in the quiz panel.

  | Tier | Net score | Colour |
  |---|---|---|
  | Common | 1–4 | `#1eff00` green |
  | Rare | 5–9 | `#0070dd` blue |
  | Epic | 10–14 | `#a335ee` purple |
  | Legendary | ≥ 15 | `#ff8000` orange, pulsing glow |

  A question degrades if wrong answers accumulate and close the gap. Tiers are always live.

- **Topic menu badge** – each topic entry now shows a net-score badge in a dedicated left column. The badge displays `min(p.r − p.f)` across all questions in the topic — the weakest link determines the tier. The badge only appears when *every* question in the topic is individually net-positive. If any question is neutral, negative or unanswered the badge shows a grey dash. The menu re-renders from live localStorage data each time it is opened.

- **Two-row index layout** – each index entry now spans two rows. Row 1: star · number · question text. Row 2: topic label (right-aligned, bleeds left into the text column). Score column spans both rows, centred.

- **Score column split** – correct count (top, tier colour) and wrong count (bottom, muted red) are now displayed as separate values instead of `correct / wrong`. If wrong count is zero it is omitted.

- **Question number coloured by tier** – `#N` in the quiz panel reflects the same tier logic as the index. Unbeantwortet: grey. 50/50: white. Net positive: tier colour with Legendary pulsing animation.

### UI polish

- **Error colour** changed from `#ff8c00` (orange) to `#e05c6e` (muted red) to eliminate the visual conflict with Legendary gold
- **Stats row numbers** softened from `var(--text)` to `#a6b8c8` to reduce contrast aggressiveness
- **Topic label fix** – index was showing only the first word of multi-word topic names; now resolves the full label from `QUIZ_CONFIG.topics`
- **50/50 state** – questions with equal correct and wrong counts now render white (neutral, not a quality tier) rather than grey

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