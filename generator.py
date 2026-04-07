new

import os
import re
import shutil
import traceback
from pathlib import Path 

def calculate_tree_depth(line):
    """
    Calculate depth based on the position of tree characters.
    Each level is indicated by 4 characters of indentation.
    """
    for i, char in enumerate(line):
        if char in ['├', '└']:
            return i // 4 + 1
     
    if line.strip().startswith('│'):
        for i, char in enumerate(line):
            if char not in ['│', ' ']:
                return i // 4 + 1
    
    for i, char in enumerate(line):
        if char not in [' ', '│', '├', '└', '─']:
            if i == 0:
                return 0 
            else:
                return i // 4
    return 0

def extract_clean_name(line):
    """
    Extract the clean name by removing all tree characters and dashes.
    """
    cleaned = line.rstrip()
    name_start = 0
    while name_start < len(cleaned) and cleaned[name_start] in [' ', '│', '├', '└', '─']:
        name_start += 1
    
    if name_start >= len(cleaned):
        return ""
    
    name = cleaned[name_start:]
    return name.strip('─ ')

def parse_tree_structure_robust(text_input):
    """
    Robust parser for tree structures using proper depth calculation.
    """
    lines = text_input.strip().split('\n')
    root_name = None
    for line in lines:
        if line.strip() and not any(c in line[0] for c in ['│', '├', '└', ' ']):
            root_name = line.strip().rstrip('/')
            break
    
    if not root_name:
        root_name = "project"
    
    operations = []
    operations.append({
        'action': 'CREATE_FOLDER',
        'name': root_name,
        'path': f'/{root_name}/',
        'parentPath': '/'
    })
    
    folder_stack = [(0, f'/{root_name}/')]
    
    for line in lines:
        if not line.strip():
            continue
        if line.strip() == root_name or line.strip() == f"{root_name}/":
            continue
        
        depth = calculate_tree_depth(line)
        name = extract_clean_name(line)
        if not name:
            continue
        
        is_folder = name.endswith('/') or ('.' not in name.split('/')[-1])
        clean_name = name.rstrip('/')
        
        while folder_stack and folder_stack[-1][0] >= depth:
            folder_stack.pop()
        
        if not folder_stack:
            folder_stack = [(0, f'/{root_name}/')]
        
        parent_depth, parent_path = folder_stack[-1]
        
        full_path = f"{parent_path.rstrip('/')}/{clean_name}"
        if is_folder:
            full_path = full_path.rstrip('/') + '/'
        
        operation = {
            'action': 'CREATE_FOLDER' if is_folder else 'CREATE_FILE',
            'name': clean_name,
            'path': full_path,
            'parentPath': parent_path
        }
        operations.append(operation)
        
        if is_folder:
            folder_stack.append((depth, full_path))
    
    return {
        'structure': {'name': root_name, 'path': f'/{root_name}/', 'type': 'folder'},
        'operations': operations
    }

def debug_tree_parsing(text_input):
    lines = text_input.strip().split('\n')
    print("\n🔍 DEBUG PARSING:")
    print("=" * 60)
    for i, line in enumerate(lines):
        if not line.strip(): continue
        depth = calculate_tree_depth(line)
        name = extract_clean_name(line)
        is_folder = name.endswith('/') or ('.' not in name.split('/')[-1]) if name else False
        print(f"Line {i:2}: '{line}' | Depth: {depth}, Name: '{name}', Folder: {is_folder}")
    print("=" * 60)

def create_structure_from_operations(base_path, operations):
    folder_ops = [op for op in operations if op['action'] == 'CREATE_FOLDER']
    file_ops = [op for op in operations if op['action'] == 'CREATE_FILE']
    
    for op in folder_ops + file_ops:
        rel_path = op['path'].lstrip('/')
        full_path = os.path.join(base_path, rel_path.rstrip('/'))
        
        if op['action'] == 'CREATE_FOLDER':
            os.makedirs(full_path, exist_ok=True)
            print(f"📁 Created folder: {full_path}")
        else:
            parent_dir = os.path.dirname(full_path)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write('')
            print(f"📄 Created file: {full_path}")

def main_robust():
    print("=" * 60)
    print("🎯 FOLDER STRUCTURE GENERATOR")
    print("=" * 60)
    print("\n📝 Paste your tree structure.")
    print("👉 IMPORTANT: Type 'END' on a new line when you are finished pasting.")
    print("-" * 50)
    
    lines = []
    while True:
        try:
            line = input()
            if line.strip().upper() == 'END':
                break
            lines.append(line)
        except EOFError:
            break
    
    folder_structure_text = '\n'.join(lines)
    if not folder_structure_text.strip():
        print("❌ No structure provided.")
        return
    
    print("\n📁 Main folder name (Enter for 'my_project'):")
    main_folder = input().strip() or "my_project"
    
    try:
        result = parse_tree_structure_robust(folder_structure_text)
        operations = result['operations']
        
        if os.path.exists(main_folder):
            print(f"\n⚠️ '{main_folder}' exists. Overwrite? (y/N):")
            if input().strip().lower() == 'y':
                shutil.rmtree(main_folder)
            else:
                print("❌ Cancelled."); return

        print(f"\n🚀 Creating structure in '{main_folder}'...")
        create_structure_from_operations(main_folder, operations)
        print(f"\n✅ Done! Location: {os.path.abspath(main_folder)}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main_robust()
    input("\nPress Enter to exit...")
