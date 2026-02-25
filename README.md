# one-file-quiz

A self-contained, single-file quiz tool. No backend, no dependencies, no installation required. Generate a quiz from a JSON source file and open it in any browser.

![one-file-quiz interface](https://raw.githubusercontent.com/lokthok/one-file-quiz/main/preview.png)

---

## Features

- Single HTML file per quiz – share it, email it, open it offline
- Multiple choice with single and multi-select support
- Code block rendering for programming questions
- Study modes: All · Exam (timed) · Random · Mistakes
- Topic filtering via dropdown
- Progress tracking with localStorage
- Index view with search and progress indicators
- PDF export
- Clean dark UI, no external dependencies

---

## Project structure

```
one-file-quiz/
├── template.html            # Quiz engine – do not edit
├── one_file_quiz.py         # Generator script
├── sources/                 # Your question files go here
│   ├── python-basics.json   # Demo
│   └── git-basics.json      # Demo
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

The script lists all JSON files in `sources/`, asks you to pick one, and writes the finished HTML to `quizzes/`. Open it in any browser.

---

## Creating a quiz with AI

The fastest way to create a question set is to hand it off to an AI:

> Create a questions JSON for one-file-quiz based on the following topic: **[your topic]**.  
> Use `python-basics.json` in the `sources/` folder as reference for the structure.  
> Each question needs: `num`, `text`, `code` (empty string if none), `source`, `label`, `answers` (array), `correct` (array of 1-based indices).  
> In question text, wrap keywords or code references in backticks for inline highlighting, e.g. `"What does \`git init\` do?"`

Save the result as a `.json` file in `sources/` and run the generator.

---

## JSON format

```json
{
  "title": "Git Basics",
  "random": 5,
  "exam_count": 10,
  "exam_minutes": 20,
  "questions": [
    {
      "num": 1,
      "text": "What does git init do?",
      "code": "",
      "source": "basics",
      "label": "Basics · 1 / 4",
      "answers": ["Downloads a repo", "Initializes a local Git repo", "Commits staged changes", "Creates a branch"],
      "correct": [2]
    },
    {
      "num": 2,
      "text": "What will this print?",
      "code": "x = [1, 2, 3]\nprint(x[-1])",
      "source": "basics",
      "label": "Basics · 2 / 4",
      "answers": ["1", "3", "IndexError", "-1"],
      "correct": [2]
    }
  ]
}
```

| Field | Description |
|---|---|
| `title` | Displayed as the quiz heading |
| `random` | Number of questions in Random mode |
| `exam_count` | Number of questions in Exam mode |
| `exam_minutes` | Time limit for Exam mode |
| `source` | Groups questions into topics (used for the Topics dropdown) |
| `label` | Shown in the question header, e.g. `Basics 2 / 7` |
| `correct` | 1-based indices of correct answers – supports multiple |
| `code` | Optional code block, multiline via `\n` |

---

## Study modes

| Mode | Description |
|---|---|
| **All** | Every question in the set, shuffled |
| **Exam** | Fixed question count, countdown timer |
| **Random** | Small random subset, good for quick review |
| **Mistakes** | Questions you got wrong more often than right |
| **Topics** | Filter by topic via dropdown |

---

## Credits

Created by [lokthok](https://github.com/lokthok) · Built with [Claude Sonnet 4.6](https://claude.ai)

---

## License

MIT