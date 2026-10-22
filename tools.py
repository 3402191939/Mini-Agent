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

if __name__=="__main__":
    print("directory: ")
    print(list_files())
    print("\nREADME content: ")
    print(read_file("README.md"))