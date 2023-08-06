# wbpUItools

UI tools plugin for [Workbench](https://pypi.org/project/wbBase/) applications.

This plugin provides some useful functions for user interaction
in Python scripts.

## Installation

```shell
pip install wbpUItools
```

Installing this plugin registers an entry point 
in the group "*wbbase.plugin*" named "*uitools*".

To use the plugin in your application, 
add it to your *application.yml* file as follows:
```yaml
AppName: myApp
Plugins:
- Name: uitools
```

## Documentation

For details read the [Documentation](https://workbench2.gitlab.io/workbench-plugins/wbpUItools).