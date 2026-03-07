# Changelog

All notable changes to one-file-quiz are documented here.

---

## [1.6.0] – 2026-03-07

### Features

- **Stats screen** – accessible via a Stats button in the info row. Shows a top 10 highscore list and a full attempt history (up to 100 entries) per mode. Modes are selected via a dropdown styled like the topics menu, with tier badge (best run), mode name, and attempt count per entry. Tracked modes: All, Exam, Random, and per-topic runs.
- **Result screen history** – after each session the result screen now shows the top 10 and the last 10 attempts for the current mode directly below the score. Top 5 ranks are coloured by tier (Platinum → Legendary → Epic → Rare → Common). The current attempt is highlighted with a cyan accent. Time column is cyan throughout.
- **Import / Export** – Export downloads the full localStorage state as a JSON file. Import reads it back and restores all progress, favourites, learn time, and history. Buttons live in the index toolbar alongside Reset and PDF.
- **Exam mode overhaul** – no answer highlights after checking, auto-advance to next question (no Next button), fav star and `#N` hidden during exam.
- **Wrong answer review** – the result screen lists all incorrectly answered questions with full answer options. Correct answers are green, the selected wrong answer is red, missed required answers are shown in red, remaining options are neutral.

### UI

- **Info row** – the mode label (e.g. "Alle", topic name) is now built inside `renderModeButtons()` using the same JS grid as the toolbar, guaranteeing true centre alignment in all cases.
- **Stats mode dropdown** – replaces the previous flat button row. Same grid layout as the topics dropdown: tier badge | mode name | attempt count.
- **Rank columns** – no `#` prefix, numbers right-aligned in a fixed `2ch` column, gap before date. Ranks 7+ are grey in the result screen top 10; ranks 7+ are grey in the stats screen top 10.
- **Sparkle performance** – `refreshPlatinumSparkles()` skips all elements inside `#screen-index`. No sparkle timers are started for index rows.

### Fix

- **Score sort** – index sort by Ergebnis now sorts ascending on first click (lowest net first = worst tier at top, useful for targeted review) and descending on second click (best tier at top). Tiebreaker within equal net: fewest wrong answers first (positive group), most wrong answers first (negative group).
- **Missed answer colour** – answers that were required but not selected now render red (not green) in the wrong answer review list.
- **Dead JS reference** – removed `resElapsed.textContent` call after the elapsed time element was removed from the result screen.

### New UI strings

`UI_BTN_RESET`, `UI_BTN_EXPORT`, `UI_BTN_IMPORT`, `UI_BTN_STATS`, `UI_WRONG_QUESTIONS`, `UI_STATS_HIGHSCORE`, `UI_STATS_HISTORY`, `UI_STATS_NODATA`, `UI_IMPORT_OK`, `UI_IMPORT_ERR`

---

## [1.5.0] – 2026-03-01

### Features

- **Platinum tier** – fifth quality tier at net score ≥ 50, above Legendary. Base colour is a muted gold (`#e8c97a`). A slow animated sweep (5.5 s) passes a brighter gold highlight across the text. Floating sparkle particles (`✦`/`✧`) in warm gold spawn at random positions around the element and fade out – deliberately sparse and non-distracting.
- **Topic label in tier colour** – when a topic mode is active, the mode label below the toolbar reflects the topic's weakest-link tier (same logic as the topic menu badge). Updates live after each answered question. Platinum topics get the full sweep and sparkle treatment.
- **Tier visuals applied consistently** – Platinum sweep, sparkles, and colour apply in all four places a tier can appear: question number (`#N`), score column in the index, topic menu badge, and the mode label.

### UI

- `#N` question number now uses class-based tier assignment instead of inline colour so `background-clip: text` animations work correctly.

### Fix

- Sparkle spawner refactored from a single global timer to a per-element `Map`. Each render function stops all active timers before replacing `innerHTML`, eliminating detached-node timer accumulation that caused performance degradation.

---

## [1.4.1] – 2026-03-01

### UI

- **Index alignment fix** – star and question number now span both grid rows (row 1+2) and sit vertically centered alongside the question text and topic label. Score column follows the same pattern. Previously star, number, and score were anchored to row 1 only, causing misalignment on multi-line questions.
- **Expand button relocated** – ▼/▲ moved from column 1 row 2 to column 3 row 2, sitting left-aligned next to the topic label. Column 1 is now exclusively owned by the star.

---

## [1.4.0] – 2026-03-01

### Features

- **Expandable answers in index** – each index row now has a toggle button (▼/▲) in the favourite column. Click to reveal all answer options for that question with correct answers highlighted in green and wrong ones dimmed. Useful for quick review without leaving the index.
- **Attempt counter in score column** – the score column now shows `correct / wrong` side by side in a single line. Correct count uses the tier colour, wrong count is red when non-zero and grey when zero.
- **PDF export fix** – question number and topic are now correctly included in the PDF output header (`#42 · Fi Buchhaltung`). Previously both were missing.

### UI

- **Toolbar restructured** – layout is now a CSS grid with `1fr auto 1fr` columns. Mode button sits exactly in the center regardless of Index/Topics button widths. Learn timer lives in the left cell, exam timer in the right cell.
- **Mode label row** – Richtig/Falsch/Gesamt removed from the quiz view. The row below the toolbar now shows only the current mode or topic name, centered. Stats are still shown on the result screen.
- **Exam timer moved** – countdown is now in the toolbar between the Mode button and Topics, labelled with the localised "Remaining"/"Verbleibend" prefix.
- **Letter-spacing reduced to 0** across all monospace elements. The `ONE-FILE-QUIZ` header tag keeps `0.1em` as it is uppercase.
- **Reset button** – "Verlauf löschen" / "Clear history" renamed to "Reset" in both languages.

---

## [1.3.1] – 2026-02-28

### Features

- **Exam timer colours** – traffic-light colour scheme based on remaining time. Above 50 % green, at ≤ 50 % gold, at ≤ 25 % red.
- **Timer auto-end** – when the countdown reaches zero the quiz automatically calls `showResult()`. Unanswered questions count as wrong but are not written to localStorage.
- **Result screen keyboard** – `Space` now triggers Try Again on the result screen.

---

## [1.3.0] – 2026-02-28

### Features

- **Quality tier system** – four tiers based on net score (correct minus wrong). Tiers apply to the score column in the index and the `#N` question number in the quiz panel.

  | Tier | Net score | Colour |
  |---|---|---|
  | Common | 1–4 | `#1eff00` green |
  | Rare | 5–9 | `#0070dd` blue |
  | Epic | 10–14 | `#a335ee` purple |
  | Legendary | ≥ 15 | `#ff8000` orange, pulsing glow |

- **Topic menu badge** – weakest-link net score badge per topic. Only shown when every question in the topic is individually net-positive.
- **Two-row index layout** – row 1: star · number · text. Row 2: topic label right-aligned.
- **Score column split** – correct (tier colour) and wrong (muted red) shown separately.
- **Question number coloured by tier** – `#N` reflects live tier state.

### UI polish

- Error colour changed from orange to muted red to avoid conflict with Legendary gold
- Stats row numbers softened to `#a6b8c8`
- Topic label fix for multi-word topic names
- 50/50 state renders white instead of grey

---

## [1.2.1] – 2026-02-27

### UI polish

- q-meta restructured: star left, correct answer count center, `#N` right
- Hints row layout fixed for longer UI strings
- `qOrigNum` label removed

---

## [1.2.0] – 2026-02-27

### Features

- Favourites system with star icon, Favourites mode, index column
- Sortable index columns
- Keyboard: `1–0` for answers, `Space` = Check/Next, `Enter` = toggle favourite
- Language support via `"lang"` field in JSON

### Breaking changes

- JSON requires `"lang"` field. Files without it are skipped.
- `Enter` no longer confirms answers (use `Space`).

---

## [1.1.1] – 2026-02-26

### Features

- Batch processing of all JSON files in `sources/`
- `num` and `label` auto-generated; `topic` replaces `source`

### Breaking changes

- `num`, `label`, `source` fields no longer valid.

---

## [1.0.0] – 2026-02-25

Initial release.