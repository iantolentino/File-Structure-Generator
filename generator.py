import os
import shutil
import traceback

def calculate_tree_depth(line):
    for i, char in enumerate(line):
        if char in ['├', '└']:
            return i // 4 + 1
    if line.strip().startswith('│'):
        for i, char in enumerate(line):
            if char not in ['│', ' ']:
                return i // 4 + 1
    for i, char in enumerate(line):
        if char not in [' ', '│', '├', '└', '─']:
            return 0 if i == 0 else i // 4
    return 0

def extract_clean_name(line):
    cleaned = line.rstrip()
    name_start = 0
    while name_start < len(cleaned) and cleaned[name_start] in [' ', '│', '├', '└', '─']:
        name_start += 1
    if name_start >= len(cleaned):
        return ""
    return cleaned[name_start:].strip('─ ')

def parse_tree_structure_robust(text_input):
    lines = [l for l in text_input.strip().split('\n') if l.strip()]
    
    # Auto-detect root folder from the first line
    root_line = lines[0]
    root_name = extract_clean_name(root_line).rstrip('/')
    
    # If the first line looks like a branch, use a default root
    if any(c in root_line for c in ['├', '└', '│']):
        root_name = "project"
        start_index = 0
    else:
        start_index = 1

    operations = [{
        'action': 'CREATE_FOLDER',
        'path': f'/{root_name}/',
        'depth': 0
    }]
    
    folder_stack = [(0, f'/{root_name}/')]
    
    for line in lines[start_index:]:
        depth = calculate_tree_depth(line)
        name = extract_clean_name(line)
        if not name: continue
        
        is_folder = name.endswith('/') or ('.' not in name.split('/')[-1])
        clean_name = name.rstrip('/')
        
        while folder_stack and folder_stack[-1][0] >= depth:
            folder_stack.pop()
        
        parent_path = folder_stack[-1][1] if folder_stack else f'/{root_name}/'
        full_path = f"{parent_path.rstrip('/')}/{clean_name}"
        
        if is_folder:
            full_path += '/'
            folder_stack.append((depth, full_path))
            
        operations.append({
            'action': 'CREATE_FOLDER' if is_folder else 'CREATE_FILE',
            'path': full_path
        })
    
    return root_name, operations

def main():
    print("🎯 PASTE STRUCTURE BELOW (Hit Enter twice or type 'END' to finish):")
    print("-" * 50)
    
    lines = []
    while True:
        try:
            line = input()
            if line.strip().upper() == 'END' or (line == '' and lines and lines[-1] == ''):
                break
            lines.append(line)
        except EOFError:
            break
            
    text = '\n'.join(lines).strip()
    if not text:
        print("❌ No structure detected."); return

    try:
        root_name, operations = parse_tree_structure_robust(text)
        
        # Immediate Creation
        if os.path.exists(root_name):
            shutil.rmtree(root_name)
            
        for op in operations:
            rel_path = op['path'].lstrip('/')
            full_path = os.path.join(os.getcwd(), rel_path.rstrip('/'))
            
            if op['action'] == 'CREATE_FOLDER':
                os.makedirs(full_path, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write('')
        
        print(f"\n✅ Created: {root_name}/")
        print(f"📍 Path: {os.path.abspath(root_name)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
