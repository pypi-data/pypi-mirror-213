# aichopen-tools
Repository containing tools used by the AI-Team

- JsonLoader: tool to load and dump json into files 

- LoggerFactory: tool to create a preconfigured logger using the singleton pattern 


## Make package publicly pip installable 
### Generate the distribution archives
```bash
python3 -m pip install --upgrade build
python3 -m build
```

### Upload to TestPyPI
```bash
python3 -m pip install --upgrade twine
python3 -m twine upload --repository testpypi dist/*
```

## Installation
### Local 
First install
```bash
pip install .
```

If you have an existing install, and want to ensure package and dependencies are updated
```bash
pip install --upgrade .
```
or pip uninstall aichopen-tools

### Remote
First add your ssh key on GitHub and then pip install the repository as shown below:

```bash
pip install git+https://git@github.com/echOpen-factory/aichopen-tools.git
```


## Usage 
    from aichopen_tools.json_loader import JsonLoader

    from aichopen_tools.logger import LoggerFactory
    

## Additional
You can find examples of issue and pull requests templates in the directory .github