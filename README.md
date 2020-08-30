# ARGON - a DIY generator for files and projects

(!)[https://img.shields.io/badge/-WIP-red]

## Motivation

Many a times in programming will there be some "scaffolding" needed for various projects, which usually consists of lots of same text and a little bit of different text. Mostly it's for python cli's I make. While I could copy and paste everything and then do a few replaces, it's much more fun to automate.


## Stack structure

Okay it's simple, the current root is hardcoded in /usr/local/templates/ (to be changed). Every directory is a **stack**. (For califynig purposes, we are defining a stack as a file or series of files/directories to generate based on given values).

A stack has **3** parts:

* `MANIFEST.yaml` (optional) - Has `help: description of the cli` as its only value. Used for later. 
* `values.yaml` (optional) - Has lists of values and helpful descripton as to what they could be. Will use later.
* src (required) - this is the directory that **actually contains the files you want generated**


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

(whitespace is optional for enclosing template tokens--I like `<% foo %>` when its in files, ond `<%foo%> for directory names, cause directories with spaces in their names, although legal, are very annoying.)


## Generating files

Right now, its `python3 argon.py name-of-stack`. You can't provide values yet cause I'm out of time right now. You'll have to edit the source code on line 25.

(Or just wait till the project is actually stable)


## Really Big TODOS:

* process for providing values for templates
* prompt for a value if its missing
* reading the values.yml file to provide hints and stuff
