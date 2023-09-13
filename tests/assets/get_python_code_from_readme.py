from typing import List

README_FILE = "README.md"
OUTPUT_FILE = "readme_copilot.py"
PYTHON_LINE_START = "```python"
PYTHON_LINE_END = "```"
BLACKLISTED_PYTHON_LINES = [
    '    openai_api_key="your-openai-api-key",',
]


def get_readme_lines() -> List[str]:
    result = []
    with open(README_FILE, "r", encoding="utf-8") as file:
        for line in file:
            result.append(line.replace("\n", ""))
    return result


def get_python_snippet(readme: List[str]) -> List[str]:
    result = []
    started = False
    for line in readme:
        if started and not line.startswith(PYTHON_LINE_END):
            result.append(line)

        if line.startswith(PYTHON_LINE_START):
            started = True
        elif line.startswith(PYTHON_LINE_END):
            started = False
    return result


def write_python_lines(python_lines: List[str]) -> None:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        for line in python_lines:
            if line not in BLACKLISTED_PYTHON_LINES:
                file.write(line + "\n")


def main():
    readme = get_readme_lines()
    python_lines = get_python_snippet(readme)
    write_python_lines(python_lines)


if __name__ == '__main__':
    main()
