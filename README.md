# Conda-activate
Activate Conda virtual environments in Vim.

<p align="center">
<img src="/Conda.gif" width="60%" height="60%">
</p>

## Introduction
Conda-activate picks the inheritance of
[vim-conda](https://github.com/cjrh/vim-conda) by providing the same features
in a Vim9 fashion.  It further accommodates changes that `conda` experienced
throughout the years.
The plugin has been tested on **Conda 23.3.1**.

Conda-Activate set various environment variables such as `$CONDA_DEFAULT_ENV,
$CONDA_PREFIX`, `$PATH`, etc., set the internal `sys.path` and set the
`pythonthreehome` and `pythonthreedll` options.

### For Windows users.
Be sure to start vim (or gvim) from an *Anaconda* or an *Anaconda powershell*
prompt.
If you start vim/gvim by double clicking on their icons or from an ordinary
`cmd.exe` or `powershell` shell without activate any environment, then `conda`
won't be initialized and the plugin will not work.

If you really want to open vim/gvim through a double clickable icon, then
consider to create a batch file like the following:

```
@echo off
call C:\Users\yt75534\Miniconda3\condabin\activate.bat C:\Users\yt75534\Miniconda3\envs\myenv
gvim
```

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
