# Folder Structure Generator

Generate full directory hierarchies instantly by pasting a tree diagram into your terminal.

### Quick Start (No Installation Required)

Run this command to start the generator immediately:

**Windows (PowerShell):**

```powershell
curl.exe -sL https://tinyurl.com/generate-structure -o gen.py; python gen.py
```

**macOS / Linux:**

```bash
curl -sL https://tinyurl.com/generate-structure | python3
```

**How to use:**

1.  Open a terminal/powershell and navigate to the parent directory where you want your project created.
2.  Run the command.
3.  Paste your tree structure (e.g., from a prompt or documentation).
4.  Hit **Enter** twice (or type `END` on a new line) to build.

-----

### Terminal Workflow

When you run the command, the process follows this logic:

1.  **Prompt:**
    `PASTE STRUCTURE BELOW (Hit Enter twice or type 'END' to finish):`
2.  **User Input (Example):**
    ```text
    my-app/
    ├── src/
    │   └── main.py
    └── README.md
    ```
3.  **Action:** Hit **Enter** twice.
4.  **Output:**
    `Created: my-app/`
    `Path: C:\Users\Username\Documents\my-app`

-----

### Features

  * **Instant Scaffolding**: Detects the root folder name automatically from the first line of your paste.
  * **Robust Parser**: Handles standard tree characters (`├`, `│`, `└`) and 4-space indentation.
  * **Zero Friction**: No cloning or external dependencies required.
  * **Smart Cleanup**: Automatically replaces existing folders of the same name for a fresh build.
  * **Cross-Platform**: Compatible with Windows, macOS, and Linux.

-----

### Advanced Configuration

#### Create a Terminal Shortcut (Alias)

To use the tool anytime by typing `mktree`:

**Windows (PowerShell Profile):**

```powershell
function mktree { 
    curl.exe -sL https://tinyurl.com/generate-structure -o $env:TEMP\gen.py
    python $env:TEMP\gen.py
}
```

**macOS / Linux:**

```bash
alias mktree="curl -sL https://tinyurl.com/generate-structure | python3"
```

-----

### Troubleshooting

  * **Pasting issues on Windows**: If the terminal buffer cuts off your paste, ensure you type `END` on a new line after pasting.
  * **Permission Denied**: Ensure you have write permissions for the directory where you are running the script.
  * **Python Version**: Requires **Python 3.6+**.

**Developed by [iantolentino](https://www.google.com/search?q=https://github.com/iantolentino)**
