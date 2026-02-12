from pathlib import Path
import curses
import sys

import pytest


TESTS_DIR = Path(__file__).parent / "tests"


def discover_test_files() -> list[Path]:
    patterns = ("test_*.py", "*_test.py")
    found: dict[Path, None] = {}
    for pattern in patterns:
        for file_path in TESTS_DIR.glob(pattern):
            if file_path.is_file():
                found[file_path] = None
    return sorted(found.keys(), key=lambda p: p.name.lower())


def selector_ui(stdscr, items: list[Path]) -> list[Path]:
    curses.curs_set(0)
    stdscr.keypad(True)
    current_index = 0
    selected = [False] * len(items)

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        help_text = "Arrows: move | Space: select | Enter: run | q: quit"
        stdscr.addnstr(0, 0, help_text, width - 1)

        visible_rows = max(1, height - 2)
        start = 0
        if current_index >= visible_rows:
            start = current_index - visible_rows + 1
        end = min(len(items), start + visible_rows)

        for row, idx in enumerate(range(start, end), start=1):
            mark = "x" if selected[idx] else " "
            line = f"[{mark}] {items[idx].name}"
            if idx == current_index:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addnstr(row, 0, line, width - 1)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addnstr(row, 0, line, width - 1)

        stdscr.refresh()
        key = stdscr.getch()

        if key in (curses.KEY_UP, ord("k")) and current_index > 0:
            current_index -= 1
        elif key in (curses.KEY_DOWN, ord("j")) and current_index < len(items) - 1:
            current_index += 1
        elif key == ord(" "):
            selected[current_index] = not selected[current_index]
        elif key in (10, 13, curses.KEY_ENTER):
            return [item for item, is_selected in zip(items, selected) if is_selected]
        elif key in (ord("q"), 27):
            return []


def choose_files_interactively(files: list[Path]) -> list[Path]:
    if not files:
        return []
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        return files
    return curses.wrapper(selector_ui, files)


if __name__ == "__main__":
    test_files = discover_test_files()
    if not test_files:
        print(f"No test files found in {TESTS_DIR}")
        raise SystemExit(1)

    chosen = choose_files_interactively(test_files)
    if not chosen:
        print("No tests selected. Exit.")
        raise SystemExit(0)

    args = ["-v", "--html=report.html", "--self-contained-html"]
    args.extend(str(path) for path in chosen)
    raise SystemExit(pytest.main(args))
