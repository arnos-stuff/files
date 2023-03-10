import requests
import shutil
import json
import git

from pathlib import Path

packages = json.load(open('packages.json'))

baseurl = packages['baseurl']
repos = packages['repositories']
indexes = packages['indexes']
tmp = Path('tmp')
tmp.mkdir(exist_ok=True)

for pkg in repos:
    url = baseurl + pkg["repo"] + '.git'
    print(f'Cloning {url}')
    pkgdir = Path(pkg["name"])
    tmp_pkgdir = tmp / pkg["name"]
    git.Repo.clone_from(url, tmp_pkgdir)
    markdowns = tmp_pkgdir.glob('**/*.md')
    
    
    for md in markdowns:
        new_md = pkgdir.joinpath(*md.parts[2:])
        new_md.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(md, new_md)
        shutil.rmtree(pkgdir / md.parts[1], ignore_errors=True)
    shutil.rmtree(tmp, ignore_errors=True)