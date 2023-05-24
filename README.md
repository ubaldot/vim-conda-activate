# Conda-activate
Activate conda environments in vim.

## Introduction
Conda-activate pick the inheritance of
[vim-conda](https://github.com/cjrh/vim-conda) by providing the same features
but in a Vim9 fashion. In-fact, this plugin is entirely written in Vim9
language and it accommodates the changes that `conda` experienced through the
years, like the renaming `root` to `base`, the different behavior of `conda
deactivate` and so on and so forth.

This plugin set `$CONDA_DEFAULT_ENV` and `$PATH`
environment variables in response to conda virtual environment change.
That's all.


## Requirements
You need `conda` and Vim9.

You need to be sure that your `python` environment is set properly.
To verify it, be sure that the command `:echo has('python3')` returns `1` and
that the command `:python3 print('Hello world')` returns `'Hello world'`.

If it does not work, then you most likely have to set the `pythonthreedll` and
`pythonthreehome` options in Vim.
See `:h pythonthreedll` and `:h pythonthreehome`.

## Usage
This plugin has only two commands:
```
:CondaChangeEnv # Show a popup menu
:CondaActivate <env> # Activate <env> without popup menu
```

## Contributing
Feel free to send a PR if have any improvement ideas.

## License
Same as Vim.
