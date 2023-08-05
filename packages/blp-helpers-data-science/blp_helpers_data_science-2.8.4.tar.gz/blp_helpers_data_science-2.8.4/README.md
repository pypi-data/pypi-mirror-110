# What it has
Helpers I use for Data Science projects

# Additional info
* https://pypi.org/project/blp-helpers-data-science/
* https://github.com/leugh/helpers_data_science
# How to use it
```python
pip install blp-helpers-data-science
```

# How to develop it
1. Update CHANGELOG.md
2. Update setup.py
3. Update setuptools wheel and twine:
```python
pip install --user --upgrade setuptools wheel
pip install --user --upgrade twine
```
4. Create distributuion packages
```python
python setup.py sdist bdist_wheel
```
5. Upload pypi
```python
python -m twine upload dist/*
```
> Source: https://widdowquinn.github.io/coding/update-pypi-package/
