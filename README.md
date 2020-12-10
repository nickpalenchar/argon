# ARGON - a DIY generator for files and projects

![wip](https://img.shields.io/badge/-WIP-red)

## Motivation

Many a times in programming will there be some "scaffolding" needed for various projects, which usually consists of lots of same text and a little bit of different text. Argon lets you create a bundle of templates (called a 
) and generate different values into them! 

This is mostly for python cli's I make. While I could copy and paste everything and then do a few replaces, it's much more fun to automate.


## Stack structure

Okay it's simple, the current root is hardcoded in /usr/local/templates/ (to be changed). Every directory is a **stack**. (For califynig purposes, we are defining a stack as a file or series of files/directories to generate based on given values).

A stack has **2** parts:

* `stack.yaml` (optional) - Sets metadata used by argon to determine things like name and required values.
* src (required) - this is the directory that **actually contains the files you want generated**

### stack.yaml values

All fields are optional.

```yaml
name: string # name that identifies stack to argon. Used with `argon new <name>`
values:
  - someName: someDescription # shortform, if `someName` is found in template, `someDescription` is printed as help text when prompting for a value
  - name: someName # longform. someName is the name of the value in the template
    description: someDescription # when matching someName, someDescription is printed as help text
    default: defaultValue # if user gives no input, use this instead
```

When fields are omitted, argon will determine names based on the contents of the stack.

* `name`: uses the top-level directory as the name
* `values`: dynamically prompts values based on what is found in the templates at runtime. Descriptions are blank

## Templating syntax

Enclose variables you want replace with `<%` and `%>`. You could have a text file like this:

```
Hello, <% name %>!
```

And if you generated with name set to 'Nick', you would get:

```
hello, Nick!
```

### Works on files AND directories!

It looks weird, but you could make a directory named `<%foo%>`, and the entire directory would be named the value of foo on generation.

(whitespace is optional for enclosing template tokens--I like `<% foo %>` when its in files, and `<%foo%> for directory names, cause directories with spaces in their names, although legal, are very annoying.)


## Installing

From source, you can run `pip3 install path/to/argon`


# Configuration

`.argonconfig.yaml` for customizing the cli beheivor

## Environment variables

`ARGON_CONFIG` - path to an `.argonconfig.yaml` file. **This overrides all other .argonconfig.yaml files**. Generally, it's used for testing


## Really Big TODOS:

* ~process for providing values for templates~
* ~prompt for a value if its missing~
* reading the stack.yml file to provide hints and stuff
* more documentation
