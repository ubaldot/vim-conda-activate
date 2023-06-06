# Conda-activate
Activate Conda virtual environments in Vim.

<p align="center">
<img src="/Conda.gif" width="60%" height="60%">
</p>

## Introduction
*Conda-activate* picks the inheritance of
[vim-conda](https://github.com/cjrh/vim-conda) by providing the same features
in a Vim9 fashion.  It further accommodates changes that `conda` experienced
throughout the years.
This plugin has been tested on **Conda 23.3.1**.

*Conda-activate* set various environment variables such as `$CONDA_DEFAULT_ENV`,
 `$CONDA_PREFIX`, `$PATH`, etc., and set the
`pythonthreehome` and `pythonthreedll` options.

~~The internal `sys.path` used by Vim is also set.~~
The internal `sys.path` is not changed, see issue #4.
However, you can fix it by starting Vim from a certain virtual
environment or by adding something like the following line:

```
autocmd VimEnter * :CondaActivate myenv
```

in your `.vimrc`.


## Requirements
You need *conda* and *Vim9*.<br>

You also need  your `python` environment set properly.
Be sure that you get `1` in response to  `:echo has('python3')` and
 `Hello World` in response to `:python3 print('Hello World')`.

<!-- If it won't happen, then you have to set the `pythonthreedll` and -->
<!-- `pythonthreehome` options in Vim. -->
<!-- See `:h pythonthreedll` and `:h pythonthreehome`.<br><br> -->


>**Note for Windows users**.<br>
>Be sure to start vim (or gvim) from a *\*conda* or a *\*conda powershell*
>prompt.<br>
>If you start *vim* or *gvim* from an ordinary
>`cmd.exe` or `powershell` shell where no `conda` virtual
>environment is activated, then this plugin will not work.
>
>The same happens if you start *vim/gvim* by double-clicking on their icons.
>Most likely they will start without any *conda* initialization.
>If you want to open vim/gvim through clickable icon, then
>consider to create a batch file with a content similar to the following:
>
```
@echo off
call C:\Users\yourname\Miniconda3\condabin\activate.bat C:\Users\yourname\Miniconda3\envs\myenv
gvim
```
>
>Such a batch file activate a virtual environment first, and then
>start gvim. At this point, you can freely change environment inside Vim through
>*vim-conda-activate*.
>
>Finally, in the list of all the available virtual environments, those named
>like `Miniconda3`, `Anaconda`, etc. represent the `base` environment.


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
Feel free to send a PR if have any improvement ideas.<br>
For more info check `:h condaactivate.txt`.


## License
BSD-3 Clause.
