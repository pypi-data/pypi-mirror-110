# dvol

Docker Volume mapping control; container access made easy!

to install:

```
brew install flare576/scripts/dvol
```

# Dev note: Deployment
```
# Bump dvol/__init__.py Version
rm -rf dist
pip3 uninstall -y dvol
python3 -m build
pip3 install dist/dvol-*.tar.gz
dvol -v && python3 -m twine upload dist/*
```

