# Conda-activate
Activate Conda virtual environments in vim.


## Introduction
Conda-activate picks the inheritance of
[vim-conda](https://github.com/cjrh/vim-conda) by providing the same features
in a Vim9 fashion.  It further accommodates changes that `conda` experienced
throughout the years.

This plugin set various environment variables such as `$CONDA_DEFAULT_ENV,
$CONDA_PREFIX` and `$PATH`, set the internal `sys.path` and the
`pythonthreehome` and `pythonthreedll` options.

>**Note**
>
> The plugin appear to work on MacOSX Ventura, but has not been tested on
> Linux and  Windows.
> If someone want to give it a shot on such OS:s I would be very grateful.


## Requirements
You need `conda` and Vim9.<br>

You also need  your `python` environment set properly.
Be sure that you get `1` in response to  `:echo has('python3')` and
 `Hello World` in response to `:python3 print('Hello world')`.

If it won't happen, then you have to set the `pythonthreedll` and
`pythonthreehome` options in Vim.
See `:h pythonthreedll` and `:h pythonthreehome`.

## Usage
This plugin has one command `CondaActivate` that take one optional argument:
```
:CondaActivate # Show a popup menu
:CondaActivate myenv # Activate myenv without popup menu
```

## Contributing
Feel free to send a PR if have any improvement ideas.

## License
Same as Vim.
