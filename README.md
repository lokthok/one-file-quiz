# one-file-quiz

A self-contained, single-file quiz tool. No backend, no dependencies, no installation required. Generate a quiz from a JSON source file and open it in any browser.

![one-file-quiz interface](https://raw.githubusercontent.com/lokthok/one-file-quiz/main/preview.png)

---

## Features

- Single HTML file per quiz – share it, email it, open it offline
- Multiple choice with single and multi-select support
- Code block rendering for programming questions
- Study modes: All · Exam (timed) · Random · Mistakes · Favourites · Topics
- Favourites – star any question during the quiz or in the index to build custom sets
- Topic filtering via dropdown with live progress badges
- Index with search, sortable columns, per-question quality tiers and expandable answer reveal
- Quality tier system – tracks how well you *really* know each question
- Stats screen – top 10 highscore and full attempt history per mode
- Result screen history – top 10 and last 10 attempts shown after every session
- Wrong answer review – full answer breakdown for every missed question after each session
- Export / Import – save and restore all progress, favourites, and history as JSON
- Progress tracking with localStorage
- PDF export
- Multilingual UI – set `"lang": "de"` or `"lang": "en"` in your JSON
- Clean dark UI, no external dependencies

---

## Project structure

```
one-file-quiz/
├── template.html            # Quiz engine – do not edit
├── one_file_quiz.py         # Generator script
├── sources/                 # Your question files go here
│   ├── python_basics.json   # Demo (English)
│   └── git_basics.json      # Demo (German)
└── quizzes/                 # Generated quizzes land here
    ├── python-basics.html
    └── git-basics.html
```

---

## Quickstart

**Requirements:** Python 3.x

```bash
git clone https://github.com/lokthok/one-file-quiz.git
cd one-file-quiz
python3 one_file_quiz.py
```

The script processes all JSON files in `sources/` and writes finished HTML files to `quizzes/`. Open any of them in any browser.

---

## Quality tier system

Getting a question right once means nothing. Real learning comes from repetition – answering correctly again and again, even after getting it wrong in between. The quality tier system makes this visible.

Each question tracks a **net score**: correct answers minus wrong answers. The tier is determined by this net value, not by the raw correct count. Getting a question wrong pulls the tier back down.

| Tier | Net score | Colour |
|---|---|---|
| Common | 1–4 | green |
| Rare | 5–9 | blue |
| Epic | 10–14 | purple |
| Legendary | ≥ 15 | orange with glow |
| Platinum | ≥ 50 | muted gold with animated bright-gold sweep and sparkle particles |

Tiers are visible in several places:

**Index** – the score column shows `correct / wrong` inline, coloured by tier. A ▼ button expands the full answer list for that question – correct answers in green, wrong ones dimmed.

**Question panel** – the `#N` question number takes on the tier colour so you know at a glance how well you know the current question before you answer. Platinum questions get a slow gold shimmer with a bright sweep and floating sparkle particles.

**Topic label** – when a topic mode is active, the mode label reflects the topic's weakest-link tier and updates live after each answered question.

**Topic menu** – each topic entry shows a badge with the lowest net score across all its questions. A topic only earns a badge when *every* question in it is individually net-positive. One weak question keeps the whole topic at a dash.

**Stats and result history** – top ranks are coloured by tier. Rank 1 is Platinum, rank 2 Legendary, and so on down to rank 5/6 as Common.

---

## Stats and history

Every completed run in All, Exam, Random, and per-topic modes is recorded in localStorage (up to 100 entries per mode).

**Result screen** – immediately after finishing, the result screen shows a top 10 highscore list and the 10 most recent attempts for the current mode. The current attempt is highlighted. Time is shown in cyan. Top ranks are coloured by tier.

**Stats screen** – accessible via the Stats button in the toolbar. Select a mode from the dropdown to view its full top 10 and complete attempt history.

**Export / Import** – use the Export button in the index toolbar to download all localStorage data as a JSON file. Use Import to restore it on any device or browser.

---

## Creating a quiz with AI

The fastest way to create a question set is to hand it off to an AI:

> Create a questions JSON for one-file-quiz based on the following topic: **[your topic]**.  
> Use `python_basics.json` in the `sources/` folder as reference for the structure.  
> Each question needs: `text`, `topic`, `answers` (array), `correct` (array of 1-based indices). Optionally `code` for a code block.  
> In question text, wrap keywords or code references in backticks for inline highlighting, e.g. `"What does \`git init\` do?"`

Save the result as a `.json` file in `sources/` and run the generator.

---

## JSON format

```json
{
  "title": "Python Basics",
  "lang": "en",
  "random": 5,
  "exam_count": 10,
  "exam_minutes": 20,
  "questions": [
    {
      "topic": "basics",
      "text": "What does the `//` operator do in Python?",
      "answers": ["Writes a comment", "Floor division", "Calculates the remainder", "Regular division"],
      "correct": [2]
    },
    {
      "topic": "datatypes",
      "text": "What will this print?",
      "code": "my_list = [1, 2, 3]\nmy_list.append(4)\nprint(my_list)",
      "answers": ["[1, 2, 3]", "[1, 2, 3, 4]", "Error", "[4, 1, 2, 3]"],
      "correct": [2]
    }
  ]
}
```

| Field | Required | Description |
|---|---|---|
| `title` | ✓ | Displayed as the quiz heading |
| `lang` | ✓ | UI language: `"en"` or `"de"`. All button labels, feedback text and UI strings are replaced at build time by the generator — no runtime switching, no mixed-language output. Add new languages by extending `UI_STRINGS` in `one_file_quiz.py`. |
| `random` | | Number of questions in Random mode |
| `exam_count` | | Number of questions in Exam mode |
| `exam_minutes` | | Time limit for Exam mode |
| `topic` | | Groups questions (used for Topics dropdown) |
| `text` | ✓ | Question text – wrap keywords in backticks for inline highlighting |
| `code` | | Optional code block, multiline via `\n` |
| `answers` | ✓ | Array of answer strings |
| `correct` | ✓ | 1-based indices of correct answers – supports multiple |

---

## Study modes

| Mode | Description |
|---|---|
| **All** | Every question in the set, shuffled |
| **Exam** | Fixed question count, countdown timer, no answer feedback during run |
| **Random** | Small random subset, good for quick review |
| **Mistakes** | Questions you got wrong more often than right |
| **Favourites** | Only questions you starred |
| **Topics** | Filter by topic via dropdown |

---

## Keyboard shortcuts

| Key | Action |
|---|---|
| `1`–`9`, `0` | Select answer 1–10 |
| `Space` | Check answer / Next question / Try again (result screen) |
| `Enter` | Toggle favourite on current question |

---

## Credits

Created by [lokthok](https://github.com/lokthok) · Built with [Claude Sonnet 4.6](https://claude.ai)

---

## License

MIT