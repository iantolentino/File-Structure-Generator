## File Structure Generator

This CLI utility converts a plain-text tree structure (copied from a prompt or documentation) into actual folders and files on your local machine. It automatically detects the root project name from the input and creates the directory hierarchy instantly.

-----

### Quick Start

To run the generator without installing anything, use the following command in your terminal:

**Windows (PowerShell):**

```powershell
curl.exe -sL https://tinyurl.com/generate-structure -o gen.py; python gen.py
```

**macOS / Linux:**

```bash
curl -sL https://tinyurl.com/generate-structure | python3
```

-----

### Usage Instructions

1.  Run the command provided above.
2.  Paste your folder structure directly into the terminal.
3.  Press **Enter** twice or type **END** on a new line to finish.
4.  The tool will automatically create the root directory and all sub-folders/files.

**Example Input:**

```text
my-web-app/
├── src/
│   ├── index.html
│   └── styles.css
└── README.md
```

-----

### Technical Features

  * **Auto-Root Detection:** The tool identifies the first line of your paste as the project root and avoids nested duplicate folders.
  * **Intelligent Parsing:** Handles various tree characters (├, └, │) and indentation levels (4-space standard).
  * **Automatic Overwrite:** If a folder with the same name exists, it will be replaced to ensure a clean setup.
  * **No Dependencies:** Uses standard Python libraries (os, shutil, traceback).

-----

### Links

  * **Source Script:** [https://raw.githubusercontent.com/iantolentino/File-Structure-Generator/main/generator.py](https://www.google.com/search?q=https://raw.githubusercontent.com/iantolentino/File-Structure-Generator/main/generator.py)
  * **Short Link:** [https://tinyurl.com/generate-structure](https://tinyurl.com/generate-structure)
