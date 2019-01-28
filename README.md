## junit2html plugin
This is a plugin to nosetests. convert nosetests report to html

### Installation
```bash
pip install git+https://github.com/AhmedHanafy725/junit2html_plugin
```
### Usage:
`--with-html` used to enable the plugin.

`--html-testsuite-name` used for testsuite name would display in html. (Default: Nosetests)

`--html-file` used for output file name. (Default: nosetests.html)
#### Example:
```bash
nosetests --with-html --html-testsuite-name="Just Try" --html-file="Try.html" /your/path
```
### Screenshots:
![image](/images/try.png)

