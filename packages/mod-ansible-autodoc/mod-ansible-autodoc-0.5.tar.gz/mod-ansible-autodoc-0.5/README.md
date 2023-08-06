# Ansible Autodoc Version

A spin of ansible-autodoc that only documents variables

## Install
```sh
pip3 install mod-ansible-autodoc
```

## How to use?
```sh
mod-ansible-autodoc
```

## Optional Args
There are 4 optional args, one per markdown file:

1. --todo-title
2. --actions-title
3. --tags-title
4. --variables-title

The value of an argument has to be wrapped around ''. Example:
```sh
mod-ansible-autodoc --todo-title '## IMPROVEMENTS FILE'
```
