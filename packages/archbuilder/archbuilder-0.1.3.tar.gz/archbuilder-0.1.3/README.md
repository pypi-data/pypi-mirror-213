
# Archbuilder

Archbuilder is a tool that aims to speed up the setting up of projects by creating the project directories and files from user-defined templates.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Archbuilder.
```bash
  pip install archbuilder
```
    
## Usage

##### 1. By using a python script
```python
# Import archbuilder
from builder import Builder
from template import Template

# Create a template from a json file
template = Template('sass.json')

# Create the project tree from the template
project = Builder('sass', template)
project.build()
```

##### 2. By using the command-line
Invoke archbuilder to create your project. Pass the name of the project as the first argument and the path to the json file as the second argument
```bash
archbuilder sass sass.json
```

## Contributing

Contributions are always welcome!

For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.
## License

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
