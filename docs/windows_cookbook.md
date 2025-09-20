# Windows Command Cookbook (Anaconda Prompt, CMD)

## Open repo & env
conda activate trading
cd C:\Users\lucas\trading-system

## Create/edit files
notepad path\to\file.py

## Run quality gates & tests
pre-commit run -a
pytest -q

## Git basics
git status
git add <files>
git commit -m "message"
git push

## Create folders and empty files
mkdir src\pkg
type NUL > src\pkg\__init__.py

## Common fixes
# If pre-commit complains about unstaged config:
git add .pre-commit-config.yaml

# If pytest can't find modules, ensure pytest.ini includes:
# [pytest]
# pythonpath = src
