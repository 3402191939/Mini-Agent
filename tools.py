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

def read_file(path: str) -> str:
    """
    Read a text file in UTF-8 encoding.
    """
    file = resolve_path(path)
    return file.read_text(encoding="utf-8")

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