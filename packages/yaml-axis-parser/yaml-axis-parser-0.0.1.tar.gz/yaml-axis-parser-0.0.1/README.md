# yaml-axis-parser

A simple command line tool to output the combinations for a yaml axis file used by [yaml-axis-plugin](https://plugins.jenkins.io/yaml-axis/).

## Instructions

### Installation
```shell
pip install yaml-axis-parser
```

### Usage
```shell
yaml-axis-parser path/to/axis.yaml
yaml-axis-parser --exclude-key exclude path/to/axis.yaml
```

```
usage: yaml-axis-parser [-h] [--exclude-key EXCLUDE_KEY] file

positional arguments:
  file                  The yaml axis file

optional arguments:
  -h, --help            show this help message and exit
  --exclude-key EXCLUDE_KEY, -e EXCLUDE_KEY
                        The exclude key. Defaults to "exclude"
```