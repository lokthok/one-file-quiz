#!/usr/bin/env python3
"""
one-file-quiz generator

Reads a JSON file from the sources/ folder and generates a quiz HTML.
Use questions.template.json (next to this script) as reference for the format.

JSON structure:
{
  "title": "My Quiz",
  "random": 10,
  "exam_count": 20,
  "exam_minutes": 60,
  "questions": [
    {
      "num": 1,
      "text": "Question text",
      "code": "optional code block\nmultiline supported",
      "source": "topic_key",
      "label": "Topic · 1 / 5",
      "answers": ["Answer A", "Answer B", "Answer C", "Answer D"],
      "correct": [1]
    }
  ]
}
"""

import json
import re
import sys
from datetime import date
from pathlib import Path


def separator(title=""):
    width = 60
    if title:
        pad = (width - len(title) - 2) // 2
        print(f"\n{'─' * pad} {title} {'─' * (width - pad - len(title) - 2)}")
    else:
        print(f"\n{'─' * width}")


def ask(prompt, default=None):
    hint = f" [{default}]" if default is not None else ""
    val = input(f"  {prompt}{hint}: ").strip()
    return val if val else (default or "")


def find_json():
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

    print(f"\n  Available quizzes:\n")
    for i, f in enumerate(files, 1):
        print(f"    {i}.  {f.stem}")

    print()
    while True:
        raw = ask("Select a file (number)", "1")
        try:
            idx = int(raw) - 1
            if 0 <= idx < len(files):
                print(f"  ✓ {files[idx].name}")
                return files[idx]
        except ValueError:
            pass
        print("    Invalid selection.")


def read_json(json_path):
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    errors = []
    questions = []

    for q in data.get("questions", []):
        num     = q.get("num")
        text    = q.get("text", "").strip()
        code    = q.get("code", "").strip()
        source  = q.get("source", "").strip()
        label   = q.get("label", "").strip()
        answers = q.get("answers", [])
        correct = q.get("correct", [])

        if not text:
            errors.append(f"Question {num}: empty text")
            continue
        if not answers:
            errors.append(f"Question {num}: no answers")
            continue
        if not correct:
            errors.append(f"Question {num}: no correct answer")
            continue

        built_answers = [
            {"text": a, "correct": (i in correct)}
            for i, a in enumerate(answers, 1)
        ]

        entry = {"num": num, "text": text, "answers": built_answers,
                 "label": label, "source": source}
        if code:
            entry["code"] = code

        questions.append(entry)

    return data, questions, errors


def build_config(data, questions):
    title        = data.get("title", "Quiz")
    random_count = int(data.get("random", 10))
    exam_count   = int(data.get("exam_count", 20))
    exam_minutes = int(data.get("exam_minutes", 60))

    default_key = re.sub(r"[^a-z0-9]", "_", title.lower()).strip("_")
    storage_key = f"ofq_{re.sub(r'_+', '_', default_key)}"

    seen = {}
    for q in questions:
        k = q["source"]
        if k and k not in seen:
            seen[k] = k.replace("_", " ").replace("-", " ").title()
    topics = [{"key": k, "label": l} for k, l in seen.items()]

    d = date.today()
    generated = f"{d.day:02d}-{d.month:02d}-{d.year}"

    return {
        "title":       title,
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

    new_block = "\n".join(lines)
    start_marker = "const QUIZ_CONFIG = {"
    end_marker   = "\n// =============================================================================\n// DO NOT EDIT BELOW"

    start_idx = template.find(start_marker)
    end_idx   = template.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("\n  Could not locate QUIZ_CONFIG in template. Is template.html up to date?")
        sys.exit(1)

    return template[:start_idx] + new_block + "\n" + template[end_idx:]


def write_output(html, config, json_path):
    default_name = re.sub(r"[^a-z0-9]", "-", config["title"].lower()).strip("-")
    default_name = re.sub(r"-+", "-", default_name) + ".html"

    out_dir = json_path.parent.parent / "quizzes"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / default_name

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    return out_path


def main():
    print("\n┌─────────────────────────────────┐")
    print("│     one-file-quiz generator     │")
    print("└─────────────────────────────────┘")

    json_path = find_json()

    separator("Reading")
    data, questions, errors = read_json(json_path)

    if errors:
        print(f"\n  ⚠ {len(errors)} error(s):")
        for e in errors:
            print(f"    • {e}")
        if ask("Continue anyway? (y/n)", "y").lower() != "y":
            sys.exit(1)

    config = build_config(data, questions)
    print(f"  ✓ {len(questions)} questions")
    print(f"  ✓ Topics: {', '.join(t['label'] for t in config['topics'])}")

    html     = build_html(config)
    out_path = write_output(html, config, json_path)

    separator()
    print(f"\n  ✓ {out_path.name}")
    print(f"    {out_path}\n")


if __name__ == "__main__":
    main()