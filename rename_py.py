import os
import glob

root_dir = r'c:\Users\ayush\Downloads\Final Year Project'
for filepath in glob.glob(os.path.join(root_dir, '**/*.py'), recursive=True):
    if 'venv' in filepath or '.git' in filepath:
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'Smart Resume Screening' in content:
        new_content = content.replace('Smart Resume Screening', 'Smart Resume Screening')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")
