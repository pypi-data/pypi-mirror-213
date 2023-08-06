# wbpFonttools

FontTools plugin for [Workbench](https://pypi.org/project/wbBase/) applications.

This plugin provides Workbench document templates for the following font formats:
- OpenType-TTF Font
- OpenType-OTF Font
- OpenType-WOFF WebFont
- OpenType-WOFF-2 WebFont

As well as a document view to view and edit fonts in these formats. 


## Installation

```shell
pip install wbpFonttools
```

Installing this plugin registers an entry point 
in the group "*wbbase.plugin*" named "*fonttools*".

To use the plugin in your application, 
add it to your *application.yml* file as follows:
```yaml
AppName: myApp
Plugins:
- Name: fonttools
```

## Documentation

For details read the [Documentation](https://workbench2.gitlab.io/workbench-plugins/wbpfonttools).