import os
import re
from pathlib import Path

def count_vertical_bars(line):
    """Count the number of vertical bars (│) at the start of the line"""
    count = 0
    for char in line:
        if char == '│':
            count += 1
        elif char != ' ':
            break
    return count

def extract_name(line):
    """Extract the name by removing all tree characters"""
    # Remove trailing whitespace first
    cleaned = line.rstrip()
    # Tree characters to remove from the beginning
    tree_chars = ['│', ' ', '├', '─', '└', '┌', '┐', '┴', '┤', '┼', '┬']
    
    # Remove tree characters from the start
    while cleaned and cleaned[0] in tree_chars:
        cleaned = cleaned[1:]
    
    # Also remove any remaining leading/trailing spaces and tree indicators
    cleaned = cleaned.strip()
    
    # Remove any leading/trailing dashes or spaces
    cleaned = cleaned.strip('─ ')
    
    return cleaned

def parse_tree_structure_corrected(text_input):
    """
    Parse the pasted text into a proper folder structure using the specified algorithm
    """
    lines = text_input.strip().split('\n')
    
    # Stack to track current folders, starting with root
    folder_stack = [{'name': '', 'path': '', 'type': 'folder', 'children': []}]
    
    # List to store all creation operations
    operations = []
    
    # Process each line
    for line in lines:
        if not line.strip():
            continue
        
        # Count vertical bars for depth level
        depth = count_vertical_bars(line)
        
        # Extract name
        name = extract_name(line)
        
        if not name:
            continue
        
        # Determine if it's a folder (ends with /) or file
        is_folder = name.endswith('/')
        clean_name = name[:-1] if is_folder else name
        
        # Maintain stack based on depth
        # Pop until stack size is depth + 1 (current level)
        while len(folder_stack) > depth + 1:
            folder_stack.pop()
        
        # Get current parent
        current_parent = folder_stack[depth]
        
        # Build path
        if current_parent['path']:
            if current_parent['path'].endswith('/'):
                full_path = f"{current_parent['path']}{clean_name}"
            else:
                full_path = f"{current_parent['path']}/{clean_name}"
        else:
            full_path = f"/{clean_name}" if clean_name else "/"
        
        # For folders, ensure path ends with /
        if is_folder:
            full_path = full_path.rstrip('/') + '/'
        
        if is_folder:
            # Create folder
            new_folder = {
                'name': clean_name,
                'path': full_path,
                'type': 'folder',
                'children': []
            }
            
            # Add to parent's children
            current_parent['children'].append(new_folder)
            
            # Push to stack
            folder_stack.append(new_folder)
            
            # Add to operations
            operations.append({
                'action': 'CREATE_FOLDER',
                'name': clean_name,
                'path': full_path,
                'parentPath': current_parent['path']
            })
        else:
            # Create file
            new_file = {
                'name': clean_name,
                'path': full_path,
                'type': 'file'
            }
            
            # Add to parent's children
            current_parent['children'].append(new_file)
            
            # Add to operations
            operations.append({
                'action': 'CREATE_FILE',
                'name': clean_name,
                'path': full_path,
                'parentPath': current_parent['path']
            })
    
    return {
        'structure': folder_stack[0],
        'operations': operations
    }

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

def main_enhanced():
    """
    Enhanced main function using the corrected parser
    """
    print("=" * 60)
    print("🎯 FOLDER STRUCTURE GENERATOR (Enhanced Parser)")
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
    
    # Parse the structure using the corrected algorithm
    print("\n⏳ Parsing folder structure...")
    try:
        result = parse_tree_structure_corrected(folder_structure_text)
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

# Update the existing parse_tree_structure function to use the corrected version
def parse_tree_structure(text_input):
    """Wrapper for compatibility with existing code"""
    result = parse_tree_structure_corrected(text_input)
    return result['structure']

if __name__ == "__main__":
    # Run the enhanced version
    main_enhanced()
    
    # Keep console open
    input("\nPress Enter to exit...")
