import os

dir_path = r'C:\Users\박준성\Documents\Test\github_pages2\github_pages'
for file in ['data.js', 'rss-data.js']:
    path = os.path.join(dir_path, file)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(path, 'r', encoding='euc-kr') as f:
            content = f.read()
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
