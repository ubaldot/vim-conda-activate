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


*Conda-activate* sets various environment variables such as
`$CONDA_DEFAULT_ENV`,
 `$CONDA_PREFIX`, `$PATH`, etc., and set the
`pythonthreehome` and `pythonthreedll` options.

The internal `sys.path` used by Vim is also set.

This plugin has been tested on **Conda 23.3.1** and it work-ish on such a release. 
Work-ish means that there could be some use-cases where it performs poorly.


## Requirements
You need *conda* and *Vim9*.<br>

You also need  your `python` environment set properly.
Be sure that you get `1` in response to  `:echo has('python3')` and
 `Hello World` in response to `:python3 print('Hello World')`.<br><br>

<!-- If it won't happen, then you have to set the `pythonthreedll` and -->
<!-- `pythonthreehome` options in Vim. -->
<!-- See `:h pythonthreedll` and `:h pythonthreehome`.<br><br> -->


>**Warning**<br><br>
> Avoid starting Vim from the *base* environment or from a shell where `conda`
> has not been initialized.
> To avoid starting from the `base` environment you may consider 
> to add the following:
```
conda activate myenv
```
> in your .basrc/.zshrc/whatever or to create a `.bat` file like the
> following:
```
@echo off
call C:\Users\yourname\Miniconda3\condabin\activate.bat C:\Users\yourname\Miniconda3\envs\myenv
gvim
```
> if you are a Windows user.
>
>Finally, only for Windows users, names
>like `Miniconda3`, `Anaconda`, etc. in the
>list of available virtual environments represent the `base` environment.


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
