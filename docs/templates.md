# Defining an argon template.

A template has the following structure:

* **src** - name of the directory that contains the actual templates. _Required_
* **template.yaml** - A yaml file containing optional values and hints.

## template.yaml

Has the following structure

```yaml
name: string # name of the template. (Default: parent directory's name)
values: map # TODO (Default: Will prompt on every missing value)
``` 

