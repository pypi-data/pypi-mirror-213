# wbpTextedit

Text editor plugin for Workbench applications.

This plugin provides document templates to create, view and edit 
the following file types:

- Plain text (*.txt)
- Python scripts (*.py, *.pyw)
- ini-style configuration files (*.ini, *.cfg)
- XML text files (*.xml, *.xsd)

## Installation

```shell
pip install wbpTextedit
```

Installing this plugin registers an entry point 
in the group "*wbbase.plugin*" named "*textedit*".

To use the plugin in your application, 
add it to your *application.yaml* file as follows:
```yaml
AppName: myApp
Plugins:
- Name: textedit
```
## Documentation

For details read the [Documentation](https://workbench2.gitlab.io/workbench-plugins/wbptextedit).