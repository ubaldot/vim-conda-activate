# Conda-activate
Activate Conda virtual environments in Vim.


## Introduction
Conda-activate picks the inheritance of
[vim-conda](https://github.com/cjrh/vim-conda) by providing the same features
in a Vim9 fashion.  It further accommodates changes that `conda` experienced
throughout the years.
The plugin has been tested on **Conda 23.3.1**.

Conda-Activate set various environment variables such as `$CONDA_DEFAULT_ENV,
$CONDA_PREFIX` and `$PATH`, set the internal `sys.path` and set the
`pythonthreehome` and `pythonthreedll` options.

>**Note**
>
> The plugin appear to work on MacOSX Ventura, but has not been tested on
> Linux and  Windows.
> If someone want to give it a shot on such OS:s I would be very grateful.


## Requirements
You need *conda* and *Vim9*.<br>

You also need  your `python` environment set properly.
Be sure that you get `1` in response to  `:echo has('python3')` and
 `Hello World` in response to `:python3 print('Hello World')`.

If it won't happen, then you have to set the `pythonthreedll` and
`pythonthreehome` options in Vim.
See `:h pythonthreedll` and `:h pythonthreehome`.

## Usage
This plugin has one command `CondaActivate` that take one optional argument:
```
:CondaActivate # Show a popup menu
:CondaActivate myenv # Activate myenv without popup menu
```

## Credits
Thanks to [vim-conda](https://github.com/cjrh/vim-conda) that paved the way.
I would have never done this plugin without reading (and learning)
from [vim-conda](https://github.com/cjrh/vim-conda) source code.


## Contributing
Feel free to send a PR if have any improvement ideas.


## License
Same as Vim.
