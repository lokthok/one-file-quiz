#!/usr/bin/env python3
"""
one-file-quiz generator

Reads a JSON file from the sources/ folder and generates a quiz HTML.
Use questions.template.json (next to this script) as reference for the format.

JSON structure:
{
  "title": "My Quiz",
  "lang": "en",
  "random": 10,
  "exam_count": 20,
  "exam_minutes": 60,
  "questions": [
    {
      "topic": "basics",
      "text": "Question text",
      "code": "optional code block\nmultiline supported",
      "answers": ["Answer A", "Answer B", "Answer C", "Answer D"],
      "correct": [1]
    }
  ]
}
"""

import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

__version__ = "1.5.0"

# =============================================================================
# UI strings – add more languages here
# =============================================================================
UI_STRINGS = {
    "en": {
        "LANG_CODE":          "en",
        "UI_STUDY_TIME":      "Study time",
        "UI_TOTAL":           "Total",
        "UI_CORRECT":         "Correct",
        "UI_WRONG":           "Wrong",
        "UI_REMAINING":       "Remaining",
        "UI_FAV_TITLE":       "Toggle favorite",
        "UI_QUESTION":        "Question",
        "UI_CORRECT_ANSWER":  "correct answer",
        "UI_CORRECT_ANSWERS": "correct answers",
        "UI_BTN_CHECK":       "Check",
        "UI_BTN_NEXT":        "Next \u2192",
        "UI_HINT_SELECT":     "select answer",
        "UI_HINT_CHECK":      "Check / Next",
        "UI_HINT_FAV":        "favorite",
        "UI_SHOW_HINT":       "Hints",
        "UI_SEARCH_PLACEHOLDER": "Search questions\u2026",
        "UI_SORT_FAV":        "Sort by favorites",
        "UI_SORT_QUESTION":   "Question",
        "UI_SORT_TOPIC":      "Topic",
        "UI_SORT_SCORE":      "Score",
        "UI_BTN_INDEX":       "Index",
        "UI_MODE_EXAM":       "Exam",
        "UI_MODE_ALL":        "All",
        "UI_MODE_RANDOM":     "Random",
        "UI_MODE_MISTAKES":   "Mistakes",
        "UI_MODE_FAV":        "Favorites",
        "UI_BTN_TOPICS":      "Topics",
        "UI_RESULT_LABEL":    "Result",
        "UI_BTN_TRYAGAIN":    "Try again",
        "UI_FEEDBACK_CORRECT": "Correct",
        "UI_FEEDBACK_WRONG":  "Wrong",
        "UI_PDF_TITLE":       "Question list",
        "UI_PDF_QUESTIONS":   "questions",
        "UI_GENERATED":       "generated",
        "UI_CONFIRM_CLEAR":   "Reset all progress, study time and favorites?",
        "UI_BTN_CLEAR":       "Clear history",
        "UI_BTN_MODE_MENU":   "Mode",
    },
    "de": {
        "LANG_CODE":          "de",
        "UI_STUDY_TIME":      "Lernzeit",
        "UI_TOTAL":           "Gesamt",
        "UI_CORRECT":         "Richtig",
        "UI_WRONG":           "Falsch",
        "UI_REMAINING":       "Verbleibend",
        "UI_FAV_TITLE":       "Favorit umschalten",
        "UI_QUESTION":        "Frage",
        "UI_CORRECT_ANSWER":  "richtige Antwort",
        "UI_CORRECT_ANSWERS": "richtige Antworten",
        "UI_BTN_CHECK":       "Pr\u00fcfen",
        "UI_BTN_NEXT":        "Weiter \u2192",
        "UI_HINT_SELECT":     "Antwort w\u00e4hlen",
        "UI_HINT_CHECK":      "Pr\u00fcfen / Weiter",
        "UI_HINT_FAV":        "Favorit",
        "UI_SHOW_HINT":       "Hinweise",
        "UI_SEARCH_PLACEHOLDER": "Fragen durchsuchen\u2026",
        "UI_SORT_FAV":        "Nach Favoriten sortieren",
        "UI_SORT_QUESTION":   "Frage",
        "UI_SORT_TOPIC":      "Thema",
        "UI_SORT_SCORE":      "Ergebnis",
        "UI_BTN_INDEX":       "Index",
        "UI_MODE_EXAM":       "Pr\u00fcfung",
        "UI_MODE_ALL":        "Alle",
        "UI_MODE_RANDOM":     "Zufall",
        "UI_MODE_MISTAKES":   "Fehler",
        "UI_MODE_FAV":        "Favoriten",
        "UI_BTN_TOPICS":      "Themen",
        "UI_RESULT_LABEL":    "Ergebnis",
        "UI_BTN_TRYAGAIN":    "Nochmal",
        "UI_FEEDBACK_CORRECT": "Richtig",
        "UI_FEEDBACK_WRONG":  "Falsch",
        "UI_PDF_TITLE":       "Fragenliste",
        "UI_PDF_QUESTIONS":   "Fragen",
        "UI_GENERATED":       "erstellt",
        "UI_CONFIRM_CLEAR":   "Gesamten Fortschritt, Lernzeit und Favoriten zur\u00fccksetzen?",
        "UI_BTN_CLEAR":       "Verlauf l\u00f6schen",
        "UI_BTN_MODE_MENU":   "Modus",
    },
}

SUPPORTED_LANGS = list(UI_STRINGS.keys())


def separator(title=""):
    width = 60
    if title:
        pad = (width - len(title) - 2) // 2
        print(f"\n{'─' * pad} {title} {'─' * (width - pad - len(title) - 2)}")
    else:
        print(f"\n{'─' * width}")


def find_all_json():
    script_dir = Path(__file__).parent
    sources_dir = script_dir / "sources"

    if not sources_dir.exists():
        sources_dir.mkdir()
        print(f"\n  Created folder: sources/")
        print(f"  Place your JSON files there and run the script again.")
        sys.exit(0)

    files = sorted(sources_dir.glob("*.json"))

    if not files:
        print(f"\n  No JSON files found in sources/")
        sys.exit(1)

    return files


def read_json(json_path):
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    errors = []
    questions = []

    # Validate lang field
    lang = data.get("lang", "").strip().lower()
    if not lang:
        errors.append(f"Missing required field: \"lang\" (supported: {', '.join(SUPPORTED_LANGS)})")
        return data, questions, errors
    if lang not in UI_STRINGS:
        errors.append(f"Unsupported lang \"{lang}\" – supported: {', '.join(SUPPORTED_LANGS)}")
        return data, questions, errors

    for idx, q in enumerate(data.get("questions", []), 1):
        text    = q.get("text", "").strip()
        code    = q.get("code", "").strip()
        topic   = q.get("topic", "").strip()
        answers = q.get("answers", [])
        correct = q.get("correct", [])

        if not text:
            errors.append(f"Question {idx}: empty text")
            continue
        if not answers:
            errors.append(f"Question {idx}: no answers")
            continue
        if not correct:
            errors.append(f"Question {idx}: no correct answer")
            continue

        built_answers = [
            {"text": a, "correct": (i in correct)}
            for i, a in enumerate(answers, 1)
        ]

        entry = {"text": text, "answers": built_answers, "topic": topic}
        if code:
            entry["code"] = code

        questions.append(entry)

    return data, questions, errors


def build_config(data, questions):
    title        = data.get("title", "Quiz")
    lang         = data.get("lang", "en").strip().lower()
    random_count = int(data.get("random", 10))
    exam_count   = int(data.get("exam_count", 20))
    exam_minutes = int(data.get("exam_minutes", 60))

    default_key = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    storage_key = f"ofq_{default_key.replace('-', '_')}"

    topic_counts = Counter(q["topic"] for q in questions)
    topic_idx = {}
    for i, q in enumerate(questions, 1):
        q["num"] = i
        t = q["topic"]
        topic_idx[t] = topic_idx.get(t, 0) + 1
        t_label = t.replace("_", " ").replace("-", " ").title()
        q["label"] = f"{t_label} {topic_idx[t]} / {topic_counts[t]}"

    seen = {}
    for q in questions:
        k = q["topic"]
        if k and k not in seen:
            seen[k] = k.replace("_", " ").replace("-", " ").title()
    topics = [{"key": k, "label": l} for k, l in seen.items()]

    d = date.today()
    generated = f"{d.day:02d}-{d.month:02d}-{d.year}"

    return {
        "title":       title,
        "lang":        lang,
        "slug":        default_key,
        "topics":      topics,
        "randomCount": random_count,
        "examCount":   exam_count,
        "examMinutes": exam_minutes,
        "storageKey":  storage_key,
        "generated":   generated,
        "questions":   questions,
    }


def build_html(config):
    script_dir = Path(__file__).parent
    template_path = script_dir / "template.html"

    if not template_path.exists():
        print(f"\n  Template not found: {template_path}")
        print("  Make sure template.html is in the same folder as this script.")
        sys.exit(1)

    with open(template_path, encoding="utf-8") as f:
        template = f.read()

    # ── Inject QUIZ_CONFIG data block ──────────────────────────────────────────
    lines = ["const QUIZ_CONFIG = {"]
    lines.append(f"  title: {json.dumps(config['title'], ensure_ascii=False)},")
    lines.append(f"  topics: {json.dumps(config['topics'], ensure_ascii=False)},")
    lines.append(f"  randomCount: {config['randomCount']},")
    lines.append(f"  examCount: {config['examCount']},")
    lines.append(f"  examMinutes: {config['examMinutes']},")
    lines.append(f"  storageKey: {json.dumps(config['storageKey'])},")
    lines.append(f"  generated: {json.dumps(config['generated'])},")
    lines.append("  questions: " + json.dumps(config['questions'], ensure_ascii=False, indent=4))
    lines.append("};")

    new_block    = "\n".join(lines)
    start_marker = "const QUIZ_CONFIG = {"
    end_marker   = "\n// =============================================================================\n// DO NOT EDIT BELOW"

    start_idx = template.find(start_marker)
    end_idx   = template.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("\n  Could not locate QUIZ_CONFIG in template. Is template.html up to date?")
        sys.exit(1)

    html = template[:start_idx] + new_block + "\n" + template[end_idx:]

    # ── Replace UI string placeholders ────────────────────────────────────────
    lang    = config["lang"]
    strings = UI_STRINGS[lang]
    for key, value in strings.items():
        html = html.replace("{{" + key + "}}", value)

    return html


def write_output(html, config, json_path):
    default_name = config["slug"] + ".html"

    out_dir = json_path.parent.parent / "quizzes"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / default_name

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    return out_path


def main():
    print("\n┌───────────────────────────────────┐")
    print(f"│   one-file-quiz generator {__version__}   │")
    print("└───────────────────────────────────┘")

    files = find_all_json()
    print(f"\n  Found {len(files)} source file(s)\n")

    generated = []
    skipped   = []

    for json_path in files:
        separator(json_path.stem)
        data, questions, errors = read_json(json_path)

        if errors:
            print(f"  ⚠ {len(errors)} error(s) – skipping:")
            for e in errors:
                print(f"    • {e}")
            skipped.append(json_path.name)
            continue

        config   = build_config(data, questions)
        html     = build_html(config)
        out_path = write_output(html, config, json_path)

        print(f"  ✓ {len(questions)} questions · Lang: {config['lang']} · Topics: {', '.join(t['label'] for t in config['topics'])}")
        print(f"  → {out_path.name}")
        generated.append(out_path.name)

    separator()
    print(f"\n  {len(generated)} quiz(zes) generated")
    for name in generated:
        print(f"    ✓ {name}")
    if skipped:
        print(f"\n  {len(skipped)} skipped due to errors:")
        for name in skipped:
            print(f"    ✗ {name}")
    print()


if __name__ == "__main__":
    main()