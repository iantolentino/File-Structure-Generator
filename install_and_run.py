import os
import subprocess
import sys

REPO_URL = "https://github.com/iantolentino/File-Structure-Generator.git"
FOLDER = "File-Structure-Generator"

def main():
    print("Cloning repository...")

    if os.path.exists(FOLDER):
        print("Updating existing repo...")
        subprocess.run(["git", "-C", FOLDER, "pull"], check=False)
    else:
        subprocess.run(["git", "clone", REPO_URL], check=True)

    os.chdir(FOLDER)

    print("Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], check=True)

    print("Running CLI...\n")

    # IMPORTANT: run as module (avoids import path issues)
    subprocess.run([sys.executable, "-m", "project_gen.cli"])

if __name__ == "__main__":
    main()
