import os
import glob

template_dir = r'c:\Users\ayush\Downloads\Final Year Project\templates'
for filepath in glob.glob(os.path.join(template_dir, '**/*.html'), recursive=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'Smart Resume Screening' in content:
        new_content = content.replace('Smart Resume Screening', 'Smart Resume Screening')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")
