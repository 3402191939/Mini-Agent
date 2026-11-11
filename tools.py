from pathlib import Path

# This tool can only access folder "sanbox"
ROOT = (Path(__file__).parent / "sandbox").resolve()

def resolve_path(relative_path: str) -> Path:
    """
    Resolve a relative path to an absolute path and check access scope.
    """
    path = (ROOT / relative_path).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError("Access to paths outside the sandbox is not allowed.")
    return path

def list_files(path: str = ".") -> list[str]:
    """
    List the direct files in the given directory and end with "/"
    """
    directory = resolve_path(path)
    return [
        item.name + ("/" if item.is_dir() else "")
        for item in sorted(directory.iterdir())
    ]

def read_file(path: str, start_line: int = 1, end_line: int | None = None) -> str:
    """
    Read specified lines from a file and max 100 lines, starting from 1.
    """
    if type(start_line) is not int or start_line < 1:
        raise ValueError("start_line must be an integer greater than 0.")

    if end_line is not None:
        if type(end_line) is not int or end_line < start_line:
            raise ValueError("end_line must be an integer greater than or equal to start_line.")
    
    file = resolve_path(path)
    lines = file.read_text(encoding="utf-8").splitlines()
    total_lines = len(lines)

    if total_lines == 0:
        return f"file: {path}\ntotal lines: 0, file is empty."

    if start_line > total_lines:
        raise ValueError(f"start_line is out of bounds, total lines is {total_lines}")

    # Read 100 lines by default and return 100 lines at most even the range is larger.
    if end_line is None:
        end_line = start_line + 99
    actual_end = min(end_line, start_line + 99, total_lines)

    selected = [
        f"{number}: {lines[number - 1]}"
        for number in range(start_line, actual_end + 1)
    ]

    header = (
        f"file: {path}\n"
        f"total lines: {total_lines}, return this turn:{start_line}-{actual_end}\n"
    )

    return header + "\n".join(selected)

def search_code(keyword: str, path: str = ".") -> list[dict]:
    """
    Search for a keyword in specified directory recursively, max 20 results.
    """
    if not isinstance(keyword, str) or not keyword.strip():
        raise ValueError("keyword must be a non-empty string.")
    directory = resolve_path(path)
    if not directory.is_dir():
        raise ValueError("path must be a directory.")

    results = []
    allowed_suffixes = {".py", ".md", ".txt", ".json"}
    for file in sorted(directory.rglob("*")):
        # except directories and files with disallowed suffixes
        if not file.is_file() or file.suffix.lower() not in allowed_suffixes:
            continue

        # skip links that point outside the specified directory
        resolved_file = file.resolve()
        if not resolved_file.is_relative_to(ROOT):
            continue

        try:
            content = resolved_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        for line_number, line in enumerate(content.splitlines(), start=1):
            if keyword in line:
                results.append({
                    "path": file.relative_to(ROOT).as_posix(),
                    "line": line_number,
                    "text": line,
                })
                if len(results) >= 20:
                    return results
    return results

if __name__=="__main__":
    print("directory: ")
    print(list_files())
    print("\nREADME content: ")
    print(read_file("README.md"))