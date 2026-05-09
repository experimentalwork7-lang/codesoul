import os

def read_file(filepath):
    if not os.path.exists(filepath):
        return None, f"File '{filepath}' not found."
    with open(filepath, 'r') as f:
        lines = f.readlines()
    return lines, None

def show_file(filepath):
    lines, error = read_file(filepath)
    if error:
        return error
    result = f"\n--- {filepath} ---\n"
    for i, line in enumerate(lines, 1):
        result += f"{i:3}  {line}"
    result += "\n-------------------\n"
    return result

def edit_line(filepath, line_number, new_content):
    lines, error = read_file(filepath)
    if error:
        return error
    if line_number < 1 or line_number > len(lines):
        return f"Line {line_number} doesn't exist. File has {len(lines)} lines."
    old = lines[line_number - 1].rstrip()
    lines[line_number - 1] = new_content + '\n'
    with open(filepath, 'w') as f:
        f.writelines(lines)
    return f"Line {line_number} changed.\nOld: {old}\nNew: {new_content}"

def find_and_replace(filepath, find_text, replace_text):
    lines, error = read_file(filepath)
    if error:
        return error
    count = 0
    for i, line in enumerate(lines):
        if find_text in line:
            lines[i] = line.replace(find_text, replace_text)
            count += 1
    if count == 0:
        return f"'{find_text}' not found in {filepath}"
    with open(filepath, 'w') as f:
        f.writelines(lines)
    return f"Replaced '{find_text}' with '{replace_text}' in {count} line(s)."