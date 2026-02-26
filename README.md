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
├── sources/                  # Your question files go here
│   ├── python_basics.json    # Demo
│   └── git_basics.json       # Demo
└── quizzes/                  # Generated quizzes land here
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

The script processes all JSON files in `sources/` automatically and writes the finished HTML files to `quizzes/`. Open any of them in a browser.

---

## Creating a quiz with AI

The fastest way to create a question set is to hand it off to an AI:

> Create a questions JSON for one-file-quiz based on the following topic: **[your topic]**.  
> Use `python-basics.json` in the `sources/` folder as reference for the structure.  
> Each question needs: `text`, `topic`, `answers` (array), `correct` (array of 1-based indices). Optionally `code` for a code block.  
> In question text, wrap keywords or code references in backticks for inline highlighting, e.g. `"What does `git init` do?"`

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
      "text": "What does `git init` do?",
      "topic": "basics",
      "answers": ["Downloads a repo", "Initializes a local Git repo", "Commits staged changes", "Creates a branch"],
      "correct": [2]
    },
    {
      "text": "What will this print?",
      "code": "x = [1, 2, 3]\nprint(x[-1])",
      "topic": "basics",
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
| `text` | The question text – wrap keywords in backticks for inline highlighting |
| `topic` | Groups questions into topics (used for the Topics dropdown) |
| `answers` | Array of answer strings |
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