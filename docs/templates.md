# Defining an argon stack for templating

A template has the following structure:

* **src** - name of the directory that contains the actual templates. _Required_
* **stack.yaml** - A yaml file containing optional values and hints.

## template.yaml

Has the following structure

```yaml
summary: Short (<120 chars) description of the bundle
help: 'Full details of the bundle and how to use it. To be display in the same manner as `man` pages. Cannot use with `helpFile`. Set a map of `file: filename` to use a file name in the bundle's root instead.'
helpFile: 'relative path to the full help description. Usually "help.txt"
values: map # TODO (Default: Will prompt on every missing value)
``` 

