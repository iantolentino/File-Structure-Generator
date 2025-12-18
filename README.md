# Folder Structure Generator
## 📋 Overview

The **Folder Structure Generator** is a Python CLI program that automatically creates folder structures and files from text input. Simply paste your desired folder structure, and the program will generate all the folders and empty files for you.

## 🚀 Quick Start

### Prerequisites
- Python 3.6 or higher
- No additional packages required  

### How to Use 

1. **Run the program:**
   ```bash
   python generator.py
   ```

2. **Follow the prompts:**
   - Choose your input format (Tree or Simple paths)
   - Paste your folder structure
   - Enter a main folder name
   - Confirm if overwriting existing folder

3. **The program will automatically create all folders and files!**

## 📝 Input Formats

### Format 1: Tree Structure (Recommended)
Use tree characters (├, │, └, ──) to represent the hierarchy:

```
project/
├── src/
│   ├── main.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py
│   └── config/
├── tests/
│   └── test_main.py
├── docs/
│   └── README.md
└── requirements.txt
```

### Format 2: Simple Paths
Use forward slashes to represent paths:

```
project/src/main.py
project/src/utils/__init__.py
project/src/utils/helpers.py
project/tests/test_main.py
project/docs/README.md
project/requirements.txt
```

## 🎯 Features

- **Dual Parser Support**: Choose between tree format or simple paths
- **Smart File Detection**: Automatically detects files vs folders
- **Overwrite Protection**: Asks before overwriting existing folders
- **Progress Tracking**: Shows real-time creation progress
- **Error Handling**: Provides helpful error messages
- **Summary Report**: Shows total files and folders created

## 💡 Examples

### Example 1: Python Project
```
my_app/
├── src/
│   ├── __init__.py
│   ├── main.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── tests/
│   └── test_main.py
├── docs/
│   └── API.md
└── requirements.txt
```

### Example 2: Web Project
```
website/
├── index.html
├── css/
│   ├── style.css
│   └── responsive.css
├── js/
│   ├── app.js
│   └── utils.js
├── images/
│   ├── logo.png
│   └── background.jpg
└── assets/
    └── fonts/
```

### Example 3: React Project
```
react-app/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── Header/
│   │   │   ├── Header.jsx
│   │   │   └── Header.css
│   │   └── Footer/
│   │       ├── Footer.jsx
│   │       └── Footer.css
│   ├── pages/
│   │   ├── Home.jsx
│   │   └── About.jsx
│   ├── utils/
│   │   └── api.js
│   └── App.js
├── package.json
└── README.md
```

## 🔧 Troubleshooting

### Common Issues

1. **Files not placed in correct folders?**
   - Use the Tree format for complex hierarchies
   - Ensure proper indentation in tree format
   - Check that file names include extensions (.py, .js, etc.)

2. **Parser not detecting files correctly?**
   - Make sure files have extensions
   - Use forward slashes (/) in paths, not backslashes (\)

3. **Permission errors?**
   - Run the program in a directory where you have write permissions
   - Avoid system-protected directories

### Tips for Best Results

- **Use Tree Format** for complex nested structures
- **Include file extensions** for accurate file detection
- **Test with the example** first to ensure it works in your environment
- **Check the parsed structure** preview before creation

## 📁 Output Structure

The program creates:
- **Empty folders** with proper hierarchy
- **Empty files** with correct names and extensions
- **All parent directories** automatically

## 🛠️ Technical Details

### Supported Formats
- Tree diagrams with Unicode characters (├, │, └, ──)
- Simple path notation with forward slashes
- Mixed formats (some tree, some paths)

### File Detection
The program detects files based on:
- File extensions (.py, .js, .html, etc.)
- Common root files (README, LICENSE, etc.)
- Presence of dots in names (except leading dots for hidden files)

### Error Handling
- Invalid input format detection
- File permission errors
- Existing folder conflicts
- Malformed path handling

## 🤝 Contributing

Feel free to modify the code for your specific needs! The program is designed to be easily customizable.

### Potential Enhancements
- Add support for file templates with content
- Include Git repository initialization
- Add support for different file encodings
- Create GUI version

## 📄 License

This is a free tool for developers to quickly bootstrap project structures.

---

**Happy Coding!** 🎉
