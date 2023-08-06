# wbpNamespace

Namespace plugin for [Workbench](https://pypi.org/project/wbBase/) applications

## Installation

```shell
pip install wbpNamespace
```

Installing this plugin registers an entry point 
in the group "*wbbase.plugin*" named "*namespace*".

To use the plugin in your application, 
add it to your *application.yml* file as follows:
```yaml
AppName: myApp
Plugins:
- Name: namespace
```

## Documentation

For details read the [Documentation](https://workbench2.gitlab.io/workbench-plugins/wbpnamespace/).