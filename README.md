# Conda-activate
Activate Conda virtual environments in vim.

## Introduction
Conda-activate pick the inheritance of
[vim-conda](https://github.com/cjrh/vim-conda) by providing the same features
in a Vim9 fashion. It further accommodates changes that `conda` experienced
through the years, like the renaming `root` to `base`, the behavioral change
of `conda deactivate` and so on and so forth.

This plugin set `$CONDA_DEFAULT_ENV, $CONDA_PREFIX` and `$PATH`
environment variables in response to Conda virtual environment change.
That's all.


## Requirements
You need `conda` and Vim9.<br>

You also need to be sure that your `python` environment is set properly.
Be sure that you get `1` in response to  `:echo has('python3')` and
that you get `Hello World` in response to `:python3 print('Hello world')`.

If it won't happen, then you have to set the `pythonthreedll` and
`pythonthreehome` options in Vim.
See `:h pythonthreedll` and `:h pythonthreehome`.

## Usage
This plugin has two commands:
```
:CondaChangeEnv # Show a popup menu
:CondaActivate myenv # Activate myenv without popup menu
```
which, I think, are self-explanatory.

## Contributing
Feel free to send a PR if have any improvement ideas.

## License
Same as Vim.
