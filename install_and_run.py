import os
import sys
import subprocess
import tempfile
from pathlib import Path


def main():
    print("Installing Project Generator...")

    # Install dependencies
    subprocess.check_call([
        sys.executable, "-m", "pip", "install",
        "questionary", "Jinja2", "colorama", "pyyaml",
        "fastapi", "uvicorn", "python-multipart",
        "--quiet"
    ])

    # Create temp directory
    temp_dir = Path(tempfile.mkdtemp())

    # Create project_gen package
    project_gen_dir = temp_dir / "project_gen"
    project_gen_dir.mkdir()

    templates_dir = project_gen_dir / "templates" / "web"
    templates_dir.mkdir(parents=True)

    web_templates_dir = project_gen_dir / "web_templates"
    web_templates_dir.mkdir()

    # FIX: must be __init__.py (not init.py)
    (project_gen_dir / "__init__.py").write_text("")

    # utils.py
    (project_gen_dir / "utils.py").write_text('''import subprocess
import time
from pathlib import Path

def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        try:
            path.unlink()
            time.sleep(0.1)
        except PermissionError:
            pass

    for attempt in range(5):
        try:
            path.write_text(content, encoding="utf-8")
            return
        except PermissionError:
            time.sleep(0.3)

    try:
        if path.exists():
            path.unlink()
        path.write_text(content, encoding="utf-8")
    except:
        pass


def init_git_repo(target_dir: Path):
    try:
        subprocess.run(
            ["git", "init"],
            cwd=target_dir,
            capture_output=True,
            check=True,
            timeout=10
        )

        gitignore = target_dir / ".gitignore"
        if not gitignore.exists():
            gitignore.write_text(
                "__pycache__/\\n*.pyc\\n.env\\nnode_modules/\\ndist/\\nbuild/\\n",
                encoding="utf-8"
            )

        print("  Git repository initialized")
        return True

    except:
        print("  Git not available - skipped")
        return False
''')

    # structure_maker.py
    (project_gen_dir / "structure_maker.py").write_text('''def calculate_tree_depth(line):
    for i, char in enumerate(line):
        if char in ['\\u251c', '\\u2514']:
            return i // 4 + 1
    if line.strip().startswith('\\u2502'):
        for i, char in enumerate(line):
            if char not in ['\\u2502', ' ']:
                return i // 4 + 1
    for i, char in enumerate(line):
        if char not in [' ', '\\u2502', '\\u251c', '\\u2514', '\\u2500']:
            return 0 if i == 0 else i // 4
    return 0


def extract_clean_name(line):
    cleaned = line.rstrip()
    name_start = 0
    while name_start < len(cleaned) and cleaned[name_start] in [' ', '\\u2502', '\\u251c', '\\u2514', '\\u2500']:
        name_start += 1
    if name_start >= len(cleaned):
        return ""
    return cleaned[name_start:].strip('\\u2500 ')


def parse_tree_structure(text_input):
    lines = [l for l in text_input.strip().split('\\n') if l.strip()]
    root_line = lines[0]
    root_name = extract_clean_name(root_line).rstrip('/')

    if any(c in root_line for c in ['\\u251c', '\\u2514', '\\u2502']):
        root_name = "project"
        start_index = 0
    else:
        start_index = 1

    operations = [{'action': 'CREATE_FOLDER', 'path': root_name, 'depth': 0}]
    folder_stack = [(0, root_name)]

    for line in lines[start_index:]:
        depth = calculate_tree_depth(line)
        name = extract_clean_name(line)

        if not name:
            continue

        is_folder = name.endswith('/') or ('.' not in name.split('/')[-1])
        clean_name = name.rstrip('/')

        while folder_stack and folder_stack[-1][0] >= depth:
            folder_stack.pop()

        parent_path = folder_stack[-1][1] if folder_stack else root_name
        full_path = f"{parent_path}/{clean_name}"

        if is_folder:
            folder_stack.append((depth, full_path))

        operations.append({
            'action': 'CREATE_FOLDER' if is_folder else 'CREATE_FILE',
            'path': full_path
        })

    return root_name, operations
''')

    # prompts.py
    (project_gen_dir / "prompts.py").write_text('''import questionary

PLATFORMS = ["Web", "Desktop", "Hybrid"]

def gather_project_options():
    platform = questionary.select(
        "Select platform:",
        choices=PLATFORMS
    ).ask()

    return {
        "platform": platform,
        "category": "default",
        "colors": ["#3B82F6", "#10B981"],
        "style": "Modern",
        "scope": "Scalable app"
    }
''')

    # 🔥 IMPORTANT: ensure Python sees this package
    sys.path.insert(0, str(temp_dir))

    # Minimal setup.py
    (temp_dir / "setup.py").write_text('''from setuptools import setup, find_packages

setup(
    name="project-gen-temp",
    version="0.1.0",
    packages=find_packages(),
)
''')

    # Install package
    subprocess.check_call([
        sys.executable, "-m", "pip", "install",
        str(temp_dir), "--quiet", "--no-deps"
    ])

    # 🚨 This will fail if cli.py is missing
    try:
        from project_gen import cli
        cli.main()
    except Exception as e:
        print("CLI not found or failed to run:", e)
        print("Make sure cli.py exists in your repo.")


if __name__ == "__main__":
    main()
