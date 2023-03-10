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

def move(file, dst):
    new_file = pkgdir.joinpath(*file.parts[2:])
    new_file.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(file, new_file)

for pkg in repos:
    url = baseurl + pkg["repo"] + '.git'
    print(f'Cloning {url}')
    pkgdir = Path(pkg["name"])
    tmp_pkgdir = tmp / pkg["name"]
    git.Repo.clone_from(url, tmp_pkgdir)
    markdowns = tmp_pkgdir.glob('**/*.md')
    
    
    for md in markdowns:
        config_yaml = md.parent / '_config.yaml'
        config_yaml = config_yaml if config_yaml.exists() else md.parent / '_config.yml'
        if config_yaml.exists():
            move(config_yaml, pkgdir)
        move(md, pkgdir)
        shutil.rmtree(pkgdir / md.parts[1], ignore_errors=True)
    shutil.rmtree(tmp, ignore_errors=True)