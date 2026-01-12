# 📁 Folder Structure Generator

A powerful Python tool that automatically generates folder structures from tree diagrams or simple path lists. Perfect for quickly scaffolding projects, creating documentation examples, or setting up consistent directory layouts.

## ✨ Features

- **🌳 Tree Diagram Parser**: Parse visual tree structures (with ├, │, └ characters)
- **📝 Path List Parser**: Parse simple path lists (one path per line)
- **🔍 Smart Parsing**: Automatically detects folder vs file based on naming patterns
- **📊 Progress Display**: Real-time feedback on created folders and files
- **🔄 Overwrite Protection**: Asks before overwriting existing directories
- **📈 Statistics**: Shows count of created folders and files
- **🎯 Cross-Platform**: Works on Windows, macOS, and Linux

## 📋 Prerequisites

- Python 3.6 or higher
- No external dependencies required (uses only standard library)

## 🚀 Installation

1. **Clone or download** the script:
   ```bash
   git clone <repository-url>
   ```

2. **Navigate to the script directory**:
   ```bash
   cd folder-structure-generator
   ```

3. **Make the script executable** (optional, Linux/macOS):
   ```bash
   chmod +x folder_generator.py
   ```

## 📖 Usage

### Basic Usage

Run the script and follow the interactive prompts:

```bash
python folder_generator.py
```

### Interactive Mode

1. **Run the script**:
   ```bash
   python folder_generator.py
   ```

2. **Choose input format**:
   ```
   🔧 Choose input format:
   1. Tree format (with ├, │, └ characters)
   2. Simple paths (one path per line)
   ```

3. **Paste your structure**:
   - For **Tree Format**:
     ```text
     project/
     ├── src/
     │   ├── main.py
     │   └── utils/
     │       └── helpers.py
     └── README.md
     ```
   
   - For **Simple Paths**:
     ```text
     project/src/main.py
     project/src/utils/helpers.py
     project/README.md
     ```

4. **Enter folder name** (default: `my_project`)

5. **Confirm creation** if folder exists

### Command Line Arguments (Optional Enhancement)

```bash
# Create structure from file
python folder_generator.py --input structure.txt

# Specify output directory
python folder_generator.py --input structure.txt --output myapp

# Skip confirmation prompts
python folder_generator.py --input structure.txt --force

# Show debug information
python folder_generator.py --debug
```

## 📝 Input Formats

### Format 1: Tree Diagram (Recommended)

Use standard tree diagram notation with Unicode box-drawing characters:

```text
project/
├── src/
│   ├── __init__.py
│   ├── main.py
│   └── modules/
│       ├── auth.py
│       └── database.py
├── tests/
│   ├── test_main.py
│   └── test_modules/
├── docs/
│   ├── api.md
│   └── guide.md
├── config/
│   └── settings.yaml
└── README.md
```

**Supported Tree Characters**:
- `├──` : Branch with more items below
- `└──` : Last branch in current level
- `│`   : Vertical line connecting branches
- `─`   : Horizontal line

### Format 2: Simple Paths

List each file and folder path on a new line:

```text
project/
project/src/
project/src/__init__.py
project/src/main.py
project/src/modules/
project/src/modules/auth.py
project/src/modules/database.py
project/tests/
project/tests/test_main.py
project/tests/test_modules/
project/docs/
project/docs/api.md
project/docs/guide.md
project/config/
project/config/settings.yaml
project/README.md
```

**Note**: Folders should end with `/` or be listed before their contents.

## 🎯 Examples

### Example 1: Web Application Structure

```bash
python folder_generator.py
```

**Paste this structure**:
```text
webapp/
├── public/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── src/
│   ├── components/
│   │   ├── Header.jsx
│   │   └── Footer.jsx
│   ├── pages/
│   │   ├── Home.jsx
│   │   └── About.jsx
│   └── App.jsx
├── package.json
└── README.md
```

### Example 2: Python Package Structure

```bash
python folder_generator.py
```

**Paste this structure**:
```text
mypackage/
├── mypackage/
│   ├── __init__.py
│   ├── core.py
│   ├── utils.py
│   └── helpers/
│       ├── __init__.py
│       └── validator.py
├── tests/
│   ├── test_core.py
│   └── test_utils.py
├── docs/
│   └── index.md
├── setup.py
├── requirements.txt
└── .gitignore
```

## 🔧 Advanced Usage

### Creating Structures Programmatically

```python
from folder_generator import parse_tree_structure_robust, create_structure_from_operations

tree_structure = """myapp/
├── src/
│   └── main.py
└── config.json"""

result = parse_tree_structure_robust(tree_structure)
create_structure_from_operations("output_folder", result['operations'])
```

### Customizing File Content

Modify the `create_structure_from_operations` function to add default content to created files:

```python
def create_structure_with_content(base_path, operations, file_templates=None):
    """
    Create structure with predefined file content
    """
    file_templates = file_templates or {}
    
    for op in operations:
        rel_path = op['path'].lstrip('/')
        if rel_path.endswith('/'):
            rel_path = rel_path.rstrip('/')
        
        full_path = os.path.join(base_path, rel_path)
        
        if op['action'] == 'CREATE_FOLDER':
            os.makedirs(full_path, exist_ok=True)
        else:
            parent_dir = os.path.dirname(full_path)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)
            
            # Use template if available, otherwise create empty file
            content = file_templates.get(op['name'], '')
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
```

## 🐛 Troubleshooting

### Common Issues

1. **"No folder structure provided"**
   - Make sure you're pasting the structure correctly
   - Press Enter twice after pasting to finish

2. **Incorrect folder hierarchy**
   - Ensure tree characters are properly aligned
   - Use consistent indentation (4 spaces recommended)

3. **Permission errors**
   - Run with appropriate permissions for the target directory
   - Check if directory is open in another program

4. **Unicode characters not displaying**
   - Ensure terminal supports UTF-8 encoding
   - Try running in a different terminal (VS Code, PowerShell, etc.)

### Debug Mode

Enable debug mode to see how the parser interprets each line:

```bash
python folder_generator.py
```

When asked: "Show debug parsing info? (y/N):" press `y`

## 📁 Output Structure

The tool creates:
- All specified folders (with proper nesting)
- Empty files with correct extensions
- Maintains the exact hierarchy from your input

**Example Output**:
```
📁 Created folder: my_project
📁 Created folder: my_project/src
📄 Created file: my_project/src/main.py
📁 Created folder: my_project/src/utils
📄 Created file: my_project/src/utils/helpers.py
📄 Created file: my_project/README.md
```

## 🔄 Updating Existing Structures

The tool will:
1. Detect if the target folder already exists
2. Ask for confirmation before overwriting
3. Completely remove existing folder if confirmed
4. Create fresh structure from your input

## 📊 Performance

- **Fast**: Creates hundreds of files/folders in seconds
- **Memory Efficient**: Processes structures line by line
- **Reliable**: Robust error handling and validation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Development Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by various project scaffolding tools
- Uses Python's standard library for maximum compatibility
- Unicode tree characters from box-drawing character set

## 📞 Support

For issues, questions, or feature requests:
1. Check the troubleshooting section
2. Review existing issues
3. Create a new issue with:
   - Input structure that caused the problem
   - Expected vs actual behavior
   - Python version and operating system

---

**Happy Scaffolding! 🚀**
