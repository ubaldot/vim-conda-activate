# Conda-activate
Activate Conda environments in vim.

## Introduction
Conda-activate pick the inheritance of
[vim-conda](https://github.com/cjrh/vim-conda) by providing the same features
in a Vim9 fashion. It further accommodates changes that `conda` experienced
through the years, like the renaming `root` to `base`, the behavioral change
of `conda deactivate` and so on and so forth.

This plugin set `$CONDA_DEFAULT_ENV` and `$PATH`
environment variables in response to Conda virtual environment change.
That's all.


## Requirements
You need `conda` and Vim9 and you need to be sure that your `python`
environment is set properly.
To verify it, be sure that the command `:echo has('python3')` return `1` and
that the command `:python3 print('Hello world')` return `'Hello world'`.

If that won't happen, then you most likely have to set the `pythonthreedll` and
`pythonthreehome` options in Vim.
See `:h pythonthreedll` and `:h pythonthreehome`.

## Usage
This plugin has two commands:
```
:CondaChangeEnv # Show a popup menu
:CondaActivate myenv # Activate myenv without popup menu
```
The second is handy if you want to start Vim from a certain virtual
environment. For example, you can add the following to your `.vimrc`

```
augroup CondaActivate
    autocmd!
    autocmd VimEnter * <Cmd>CondaActivate myenv
augroup END
```


## Contributing
Feel free to send a PR if have any improvement ideas.

## License
Same as Vim.
