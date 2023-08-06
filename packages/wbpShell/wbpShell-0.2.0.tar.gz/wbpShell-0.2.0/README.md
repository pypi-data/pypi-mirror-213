# wbpShell

Shell plugin for [Workbench](https://pypi.org/project/wbBase/) applications

## Installation

```shell
pip install wbpShell
```

Installing this plugin registers an entry point 
in the group "*wbbase.plugin*" named "*shell*".

To use the plugin in your application, 
add it to your *application.yml* file as follows:
```yaml
AppName: myApp
Plugins:
- Name: shell
```

## Documentation

For details read the [Documentation](https://workbench2.gitlab.io/workbench-plugins/wbpshell/).