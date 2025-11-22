import os
import re
from pathlib import Path

def parse_folder_structure(text_input):
    """
    Parse the pasted text into a folder structure
    Supports both tree-like format and simple path lists
    """
    lines = text_input.strip().split('\n')
    structure = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Clean up the line - remove tree characters
        clean_line = re.sub(r'[│├└──]\s*', '', line)
        clean_line = clean_line.strip()
        
        if not clean_line:
            continue
            
        # Check if it's a directory (ends with / or has no extension)
        if clean_line.endswith('/') or '.' not in clean_line.split('/')[-1]:
            # It's a directory
            path_parts = clean_line.rstrip('/').split('/')
        else:
            # It's a file
            path_parts = clean_line.split('/')
        
        # Build the nested structure
        current_level = structure
        for i, part in enumerate(path_parts):
            if i == len(path_parts) - 1:
                # Last part - file or empty directory
                if '.' in part:  # Likely a file
                    current_level[part] = ""  # Empty content for now
                else:
                    if part not in current_level:
                        current_level[part] = {}
            else:
                # Intermediate directory
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]
    
    return structure

def create_structure(base_path, structure):
    """
    Recursively create the folder and file structure
    """
    for name, content in structure.items():
        full_path = os.path.join(base_path, name)
        
        if isinstance(content, dict):  # It's a folder
            os.makedirs(full_path, exist_ok=True)
            print(f"📁 Created folder: {full_path}")
            create_structure(full_path, content)
        else:  # It's a file
            # Create parent directories if they don't exist
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content or '')
            print(f"📄 Created file: {full_path}")

def display_welcome():
    """
    Display welcome message and instructions
    """
    print("=" * 60)
    print("🎯 FOLDER STRUCTURE GENERATOR")
    print("=" * 60)
    print("\n📋 INSTRUCTIONS:")
    print("1. Paste your folder structure below")
    print("2. You can use either format:")
    print("   - Tree format:")
    print("     project/")
    print("     ├── src/")
    print("     │   ├── main.py")
    print("     │   └── utils/")
    print("     └── README.md")
    print("   - Simple paths:")
    print("     project/src/main.py")
    print("     project/src/utils/")
    print("     project/README.md")
    print("3. Press Enter twice to finish pasting")
    print("=" * 60)

def get_user_input():
    """
    Get folder structure input from user with multi-line support
    """
    print("\n📝 Paste your folder structure (Press Enter twice when done):")
    print("─" * 50)
    
    lines = []
    while True:
        try:
            line = input()
            if line == '' and lines and lines[-1] == '':
                break
            lines.append(line)
        except EOFError:
            break
    
    # Remove the last empty line
    if lines and lines[-1] == '':
        lines.pop()
    
    return '\n'.join(lines)

def main():
    """
    Main function to run the folder structure generator
    """
    display_welcome()
    
    # Get the folder structure from user
    folder_structure_text = get_user_input()
    
    if not folder_structure_text.strip():
        print("❌ No folder structure provided. Exiting.")
        return
    
    # Get main folder name
    print("\n📁 Enter the main folder name (or press Enter for 'my_project'):")
    main_folder = input().strip()
    if not main_folder:
        main_folder = "my_project"
    
    # Parse the structure
    print("\n⏳ Parsing folder structure...")
    try:
        structure = parse_folder_structure(folder_structure_text)
        
        if not structure:
            print("❌ Could not parse any valid folder structure.")
            return
        
        # Create the main folder
        if os.path.exists(main_folder):
            print(f"\n⚠️  Folder '{main_folder}' already exists.")
            overwrite = input("Do you want to overwrite it? (y/N): ").strip().lower()
            if overwrite != 'y':
                print("❌ Operation cancelled.")
                return
            # Remove existing folder
            import shutil
            shutil.rmtree(main_folder)
        
        # Create the structure
        print(f"\n🚀 Creating folder structure in '{main_folder}'...")
        print("─" * 50)
        
        create_structure(main_folder, structure)
        
        print("─" * 50)
        print(f"✅ Successfully created folder structure in '{main_folder}'!")
        print(f"📊 Summary:")
        print(f"   Location: {os.path.abspath(main_folder)}")
        
        # Count files and folders
        file_count = 0
        folder_count = 0
        for root, dirs, files in os.walk(main_folder):
            folder_count += len(dirs)
            file_count += len(files)
        
        print(f"   Folders created: {folder_count}")
        print(f"   Files created: {file_count}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("Please check your input format and try again.")

def create_example():
    """
    Optional: Create an example to demonstrate the program
    """
    example_structure = """project/
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
└── requirements.txt"""
    
    print("\n💡 EXAMPLE: Try pasting this structure to test:")
    print("─" * 40)
    print(example_structure)
    print("─" * 40)

if __name__ == "__main__":
    # Show example first
    create_example()
    
    # Run the main program
    main()
    
    # Keep console open
    input("\nPress Enter to exit...")