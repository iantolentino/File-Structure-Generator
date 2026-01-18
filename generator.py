import os
import re
from pathlib import Path

def calculate_tree_depth(line):
    """
    Calculate depth based on the position of tree characters.
    Each level is indicated by 4 characters of indentation.
    """
    # Find the position of the first tree branch character (├ or └)
    for i, char in enumerate(line):
        if char in ['├', '└']:
            # Depth = position / 4 (since each level is 4 chars)
            return i // 4 + 1
     
    # If no ├ or └ found, check if it's a continuation line (starts with │)
    if line.strip().startswith('│'):
        # Find the position after │
        for i, char in enumerate(line):
            if char not in ['│', ' ']:
                return i // 4 + 1
    
    # If line starts with text (root or direct child of root)
    for i, char in enumerate(line):
        if char not in [' ', '│', '├', '└', '─']:
            if i == 0:
                return 0  # Root
            else:
                return i // 4
    
    return 0

def extract_clean_name(line):
    """
    Extract the clean name by removing all tree characters and dashes.
    """
    # Remove trailing whitespace
    cleaned = line.rstrip()
    
    # Find where the actual name starts (after tree characters)
    name_start = 0
    while name_start < len(cleaned) and cleaned[name_start] in [' ', '│', '├', '└', '─']:
        name_start += 1
    
    if name_start >= len(cleaned):
        return ""
    
    name = cleaned[name_start:]
    
    # Remove any leading/trailing dashes or spaces
    name = name.strip('─ ')
    
    return name

def parse_tree_structure_robust(text_input):
    """
    Robust parser for tree structures using proper depth calculation.
    """
    lines = text_input.strip().split('\n')
    
    # Find the root folder (first non-empty line without leading tree chars)
    root_name = None
    for line in lines:
        if line.strip() and not any(c in line[0] for c in ['│', '├', '└', ' ']):
            root_name = line.strip().rstrip('/')
            break
    
    if not root_name:
        root_name = "project"
    
    # Initialize operations list and folder stack
    operations = []
    operations.append({
        'action': 'CREATE_FOLDER',
        'name': root_name,
        'path': f'/{root_name}/',
        'parentPath': '/'
    })
    
    # Stack to track parent folders at each depth level
    # Each item: (depth, folder_path)
    folder_stack = [(0, f'/{root_name}/')]
    
    # Process each line
    for line in lines:
        if not line.strip():
            continue
        
        # Skip the root line (already processed)
        if line.strip() == root_name or line.strip() == f"{root_name}/":
            continue
        
        # Calculate depth
        depth = calculate_tree_depth(line)
        
        # Extract clean name
        name = extract_clean_name(line)
        if not name:
            continue
        
        # Check if it's a folder
        is_folder = name.endswith('/') or ('.' not in name.split('/')[-1])
        clean_name = name.rstrip('/')
        
        # Find the correct parent based on depth
        # Pop from stack until we find a parent at depth-1
        while folder_stack and folder_stack[-1][0] >= depth:
            folder_stack.pop()
        
        if not folder_stack:
            # This shouldn't happen, but just in case
            folder_stack = [(0, f'/{root_name}/')]
        
        # Get parent path
        parent_depth, parent_path = folder_stack[-1]
        
        # Build the full path
        if parent_path.endswith('/'):
            full_path = f"{parent_path}{clean_name}"
        else:
            full_path = f"{parent_path}/{clean_name}"
        
        if is_folder:
            full_path = full_path.rstrip('/') + '/'
        
        # Add to operations
        operation = {
            'action': 'CREATE_FOLDER' if is_folder else 'CREATE_FILE',
            'name': clean_name,
            'path': full_path,
            'parentPath': parent_path
        }
        operations.append(operation)
        
        # If it's a folder, push it onto the stack for its children
        if is_folder:
            folder_stack.append((depth, full_path))
    
    return {
        'structure': {'name': root_name, 'path': f'/{root_name}/', 'type': 'folder'},
        'operations': operations
    }

def debug_tree_parsing(text_input):
    """
    Debug function to show how each line is parsed.
    """
    lines = text_input.strip().split('\n')
    
    print("\n🔍 DEBUG PARSING:")
    print("=" * 60)
    
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        
        depth = calculate_tree_depth(line)
        name = extract_clean_name(line)
        is_folder = name.endswith('/') or ('.' not in name.split('/')[-1]) if name else False
        
        print(f"Line {i:2}: '{line}'")
        print(f"       Depth: {depth}, Name: '{name}', Is folder: {is_folder}")
    
    print("=" * 60)

def create_structure_from_operations(base_path, operations):
    """
    Create folder and file structure from operations list
    """
    # Sort operations: folders first, then files
    folder_ops = [op for op in operations if op['action'] == 'CREATE_FOLDER']
    file_ops = [op for op in operations if op['action'] == 'CREATE_FILE']
    
    all_ops = folder_ops + file_ops
    
    for op in all_ops:
        # Convert path to relative path from base
        rel_path = op['path'].lstrip('/')
        if rel_path.endswith('/'):
            rel_path = rel_path.rstrip('/')
        
        full_path = os.path.join(base_path, rel_path)
        
        if op['action'] == 'CREATE_FOLDER':
            os.makedirs(full_path, exist_ok=True)
            print(f"📁 Created folder: {full_path}")
        else:
            # Ensure parent directory exists
            parent_dir = os.path.dirname(full_path)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write('')  # Create empty file
            print(f"📄 Created file: {full_path}")

def display_operations(operations):
    """Display the operations in a readable format"""
    print("\n📋 Operations to be performed:")
    print("-" * 60)
    
    folder_ops = [op for op in operations if op['action'] == 'CREATE_FOLDER']
    file_ops = [op for op in operations if op['action'] == 'CREATE_FILE']
    
    if folder_ops:
        print("\n📁 Folders:")
        for op in folder_ops:
            print(f"  {op['action']}: {op['path']} (parent: {op['parentPath'] or 'root'})")
    
    if file_ops:
        print("\n📄 Files:")
        for op in file_ops:
            print(f"  {op['action']}: {op['path']} (parent: {op['parentPath'] or 'root'})")
    
    print(f"\n📊 Total: {len(folder_ops)} folders, {len(file_ops)} files")
    print("-" * 60)

def main_robust():
    """
    Main function using the robust tree parser
    """
    print("=" * 60)
    print("🎯 FOLDER STRUCTURE GENERATOR (Robust Tree Parser)")
    print("=" * 60)
    
    # Get the folder structure from user
    print("\n📝 Paste your folder structure (using tree format):")
    print("Example:")
    print("project/")
    print("├── src/")
    print("│   ├── main.py")
    print("│   └── utils/")
    print("│       └── helpers.py")
    print("└── README.md")
    print("-" * 50)
    
    lines = []
    while True:
        try:
            line = input()
            if line == '' and lines and lines[-1] == '':
                break
            lines.append(line)
        except EOFError:
            break
    
    folder_structure_text = '\n'.join(lines)
    
    if not folder_structure_text.strip():
        print("❌ No folder structure provided. Exiting.")
        return
    
    # Get main folder name
    print("\n📁 Enter the main folder name (or press Enter for 'my_project'):")
    main_folder = input().strip()
    if not main_folder:
        main_folder = "my_project"
    
    # Optional: show debug info
    print("\n🔍 Show debug parsing info? (y/N):")
    show_debug = input().strip().lower()
    
    if show_debug == 'y':
        debug_tree_parsing(folder_structure_text)
    
    # Parse the structure using the robust algorithm
    print("\n⏳ Parsing folder structure...")
    try:
        result = parse_tree_structure_robust(folder_structure_text)
        operations = result['operations']
        
        if not operations:
            print("❌ Could not parse any valid folder structure.")
            return
        
        # Display operations
        display_operations(operations)
        
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
        print("-" * 50)
        
        create_structure_from_operations(main_folder, operations)
        
        print("-" * 50)
        print(f"✅ Successfully created folder structure in '{main_folder}'!")
        print(f"📊 Summary:")
        print(f"   Location: {os.path.abspath(main_folder)}")
        
        # Count files and folders
        file_count = len([op for op in operations if op['action'] == 'CREATE_FILE'])
        folder_count = len([op for op in operations if op['action'] == 'CREATE_FOLDER'])
        
        print(f"   Folders created: {folder_count}")
        print(f"   Files created: {file_count}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        print("Please check your input format and try again.")

# Alternative: Simplified depth calculation for compatibility
def parse_tree_depth_simple(line):
    """
    Simplified depth calculation: count groups of 4-space indentation
    """
    # Count leading spaces
    leading_spaces = len(line) - len(line.lstrip(' '))
    
    # Count tree characters that indicate depth
    tree_chars = 0
    for char in line[:min(leading_spaces + 4, len(line))]:
        if char in ['├', '└']:
            tree_chars += 1
    
    # Each tree character adds one level, each 4 spaces adds one level
    return (leading_spaces // 4) + tree_chars

# Legacy function for backward compatibility
def parse_tree_structure(text_input):
    """Wrapper for compatibility with existing code"""
    result = parse_tree_structure_robust(text_input)
    return result['structure']

# Legacy functions (kept for reference)
def count_vertical_bars(line):
    """Legacy function - kept for compatibility"""
    return calculate_tree_depth(line)

def extract_name(line):
    """Legacy function - kept for compatibility"""
    return extract_clean_name(line)

def parse_tree_structure_corrected(text_input):
    """Legacy function - kept for compatibility"""
    return parse_tree_structure_robust(text_input)

def main_enhanced():
    """Legacy main function - kept for compatibility"""
    main_robust()

if __name__ == "__main__":
    # Run the robust version
    main_robust()
    
    # Keep console open
    input("\nPress Enter to exit...")
