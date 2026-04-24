import os
import subprocess
import sys

REPO_URL = "https://github.com/iantolentino/File-Structure-Generator.git"
FOLDER_NAME = "File-Structure-Generator"

def main():
    print("Cloning Project Generator...")

    # Clone repo
    if os.path.exists(FOLDER_NAME):
        print("Repo already exists, pulling latest changes...")
        subprocess.run(["git", "-C", FOLDER_NAME, "pull"])
    else:
        subprocess.run(["git", "clone", REPO_URL])

    os.chdir(FOLDER_NAME)

    print("Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."])

    print("Running CLI...\n")

    try:
        from project_gen import cli
        cli.main()
    except Exception as e:
        print("Failed to run CLI:")
        print(e)
        print("\nCheck if cli.py exists and has main() function.")

if __name__ == "__main__":
    main()
