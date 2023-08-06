














# Building distribution
https://packaging.python.org/en/latest/tutorials/packaging-projects/


requires: 
python3 -m pip install --upgrade build

...which installs tomli, pep517, build

python -m build

...which outputs files to dist/ (in .gitignore)

```shell
python3 -m pip install --upgrade twine
python3 -m twine upload --repository pypi dist/*
```
