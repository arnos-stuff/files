import json
from pathlib import Path

packages = json.load(open('packages.json'))
baseurl = packages['baseurl']
repos = packages['repositories']
indexes = packages['indexes']

groupByLang = lambda data, cat: filter(lambda arr: arr["lang"] == cat, data)
getIndex = lambda indexes, idx: list(filter(lambda arr: arr["name"] == idx, indexes)).pop()
langs = set(map(lambda arr: arr["lang"], repos))
## Write markdown file index
intro = Path('intro.md').read_text()
with open('README.md', 'w') as f:
    f.write(intro)
    for lang in langs:
        f.write(f'## {lang.capitalize()}\n\n')
        f.write(f'| Package | Description | Link to homepage | Package |  \n')
        f.write(f'| ------- | -------- | ---- | ---- |  \n')
        
        for pkg in groupByLang(repos, lang):
            pkg_index = getIndex(indexes, pkg["index"])
            pkg_index_url = pkg_index["prefix"] + pkg["name"]
            f.write(f'| {pkg["name"]} | {pkg["description"]} | [{pkg["name"]} description]({pkg["name"]}/README.md) | [package index]({pkg_index_url})|  \n')

    f.write('\n')