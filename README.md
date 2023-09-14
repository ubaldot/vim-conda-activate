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
> Vim shall be started from an activated virtual environment.
> Don't start Vim from the *base* environment or from a shell where `conda`
> has not been initialized!
> To be safe, you may consider to add the following
> in your *.basrc/.zshrc/whatever*:
>```
>conda activate myenv
>```
> or to create a `.bat` file with something like the following content:
>```
>@echo off
>call C:\Users\yourname\Miniconda3\condabin\activate.bat C:\Users\yourname\Miniconda3\envs\myenv
>gvim
>```
>
> if you are a Windows user.
> For such users, names like `Miniconda3`, `Anaconda`, etc. in the
> list of available virtual environments represent the `base` environment.
>
> Make sure that the version of Python installed in the virtual environment you use to start Vim (In Windows, it might be the `base` environment in default)
> matches the version of Python used to compile Vim to avoid error like https://github.com/ubaldot/vim-conda-activate/issues/9


## Usage
This plugin has one command `CondaActivate` that takes one (optional) argument:
```
:CondaActivate # Show a popup menu
:CondaActivate myenv # Activate myenv without popup menu
```

It further exposes an *autocommand-event* named `CondaEnvActivated` that
you can use to perform other actions just after you activated a virtual
environment.
Here is a simple example on how to use it:
```
autocmd! User CondaEnvActivated :echom $"{$CONDA_DEFAULT_ENV} activated."
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
