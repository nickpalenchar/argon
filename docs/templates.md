# Defining an argon template.

A template has the following structure:

* **src** - name of the directory that contains the actual templates. _Required_
* **template.yaml** - A yaml file containing optional values and hints.

## template.yaml

Has the following structure

```yaml
name: string # name of the template. (Default: parent directory's name)
description: Short (<120 chars) description of the bundle
help: 'Full details of the bundle and how to use it. To be display in the same mannor as `man` pages. Cannot use with `helpFile`. Set a map of `file: filename` to use a file name in the bundle's root instead.'
values: map # TODO (Default: Will prompt on every missing value)
``` 

